"""Offline ESM-family protein representation inference.

Molecularis owns input validation, local model verification, batching, output
limits and result provenance. Model weights are supplied separately by the
operator; this module never downloads weights or executes remote model code.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWYXBZUO")
_DEFAULT_MAX_MODEL_BYTES = 20 * 1024 * 1024 * 1024


def _model_digest(directory: Path, *, max_bytes: int) -> tuple[str, int, int]:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("model_path must be a local directory, not a symlink")
    files = sorted(
        (path for path in directory.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(directory).as_posix(),
    )
    if not files:
        raise ValueError("model_path contains no model files")
    digest = hashlib.sha256()
    total = 0
    for path in files:
        if path.is_symlink():
            raise ValueError("model directory must not contain symbolic links")
        relative = path.relative_to(directory).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("model files exceed max_model_bytes")
                digest.update(chunk)
    return digest.hexdigest(), total, len(files)


def run_esm_embeddings(
    sequences: list[str],
    model_path: str | Path,
    *,
    expected_model_sha256: str,
    batch_size: int = 1,
    device: str = "cpu",
    max_residues_per_sequence: int = 2048,
    max_total_residues: int = 8192,
    max_model_bytes: int = _DEFAULT_MAX_MODEL_BYTES,
    include_per_residue: bool = True,
) -> dict[str, object]:
    """Compute ESM token representations from a verified local model directory.

    Returns per-residue and mean-pooled representations. Special tokens and
    padding are excluded from pooling. The model must be a compatible ESM-family
    checkpoint saved in Transformers format.
    """
    if not isinstance(expected_model_sha256, str) or len(expected_model_sha256) != 64:
        raise ValueError("expected_model_sha256 must be a SHA-256 hex digest")
    if any(char not in "0123456789abcdef" for char in expected_model_sha256):
        raise ValueError("expected_model_sha256 must be lowercase SHA-256 hex")
    if not isinstance(sequences, list) or not sequences or len(sequences) > 256:
        raise ValueError("sequences must contain between 1 and 256 entries")
    if isinstance(batch_size, bool) or not isinstance(batch_size, int) or not 1 <= batch_size <= 16:
        raise ValueError("batch_size must be between 1 and 16")
    if device not in {"cpu", "cuda"}:
        raise ValueError("device must be cpu or cuda")
    for name, value, minimum, maximum in (
        ("max_residues_per_sequence", max_residues_per_sequence, 1, 4096),
        ("max_total_residues", max_total_residues, 1, 32768),
        ("max_model_bytes", max_model_bytes, 1, 100 * 1024**3),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
            raise ValueError(f"{name} is outside its supported bounds")

    normalized: list[str] = []
    total_residues = 0
    for index, sequence in enumerate(sequences):
        if not isinstance(sequence, str):
            raise TypeError(f"sequences[{index}] must be text")
        value = "".join(sequence.split()).upper()
        if not value or set(value) - _AMINO_ACIDS:
            raise ValueError(f"sequences[{index}] contains unsupported amino-acid symbols")
        if len(value) > max_residues_per_sequence:
            raise ValueError(f"sequences[{index}] exceeds max_residues_per_sequence")
        total_residues += len(value)
        normalized.append(value)
    if total_residues > max_total_residues:
        raise ValueError("total residues exceed max_total_residues")

    raw_path = Path(model_path).expanduser()
    if raw_path.is_symlink():
        raise ValueError("model_path must not be a symbolic link")
    path = raw_path.resolve(strict=True)
    model_hash, model_bytes, model_files = _model_digest(path, max_bytes=max_model_bytes)
    if model_hash != expected_model_sha256:
        raise ValueError("ESM model directory digest does not match expected_model_sha256")

    try:
        import torch  # type: ignore[import-not-found]
        from transformers import AutoModel, AutoTokenizer  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "ESM inference requires the approved PyTorch and Transformers runtime profile"
        ) from error
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable in this runtime")

    tokenizer = AutoTokenizer.from_pretrained(
        str(path), local_files_only=True, trust_remote_code=False,
    )
    model = AutoModel.from_pretrained(
        str(path), local_files_only=True, trust_remote_code=False,
    )
    model_type = str(getattr(model.config, "model_type", ""))
    if model_type != "esm":
        raise ValueError("The supplied checkpoint is not a Transformers ESM model")
    model.eval()
    model.to(device)
    configured_limit = int(getattr(model.config, "max_position_embeddings", 0) or 0)
    results: list[dict[str, object]] = []
    with torch.inference_mode():
        for offset in range(0, len(normalized), batch_size):
            batch = normalized[offset:offset + batch_size]
            encoded = tokenizer(
                [" ".join(sequence) for sequence in batch], return_tensors="pt", padding=True, truncation=False,
                add_special_tokens=True,
            )
            input_ids = encoded["input_ids"]
            attention = encoded["attention_mask"]
            if configured_limit and input_ids.shape[1] > configured_limit:
                raise ValueError("tokenized sequence exceeds model positional limit")
            encoded = {key: value.to(device) for key, value in encoded.items()}
            output = model(**encoded)
            hidden = output.last_hidden_state.detach().to("cpu", dtype=torch.float32)
            masks = attention.to("cpu")
            for local_index, sequence in enumerate(batch):
                token_mask = masks[local_index].bool()
                special_mask = torch.tensor(
                    tokenizer.get_special_tokens_mask(
                        input_ids[local_index].tolist(), already_has_special_tokens=True,
                    ), dtype=torch.bool,
                )
                if special_mask.numel() != token_mask.numel():
                    raise RuntimeError("Tokenizer special-token mask length mismatch")
                residue_mask = token_mask & ~special_mask
                residue_vectors = hidden[local_index][residue_mask]
                if residue_vectors.shape[0] != len(sequence):
                    raise RuntimeError("ESM output residue count does not match input sequence")
                mean_vector = residue_vectors.mean(dim=0)
                item: dict[str, object] = {
                    "sequence_index": offset + local_index,
                    "sequence_sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
                    "length": len(sequence),
                    "mean_embedding": mean_vector.tolist(),
                }
                if include_per_residue:
                    item["per_residue_embeddings"] = residue_vectors.tolist()
                results.append(item)
    return {
        "schema": "molecularis.esm-embeddings.v1",
        "engine": "ESM",
        "model": {
            "path": str(path),
            "model_type": model_type,
            "model_name": str(getattr(model.config, "_name_or_path", path.name)),
            "sha256": model_hash,
            "bytes": model_bytes,
            "files": model_files,
        },
        "runtime": {
            "torch_version": str(torch.__version__),
            "transformers_version": __import__("transformers").__version__,
            "device": device,
            "batch_size": batch_size,
        },
        "outputs": results,
        "scientific_validation": "not_assessed",
        "limitations": [
            "Requires operator-supplied, locally cached ESM checkpoint in Transformers format.",
            "Embeddings are model representations, not calibrated functional or clinical predictions.",
            "Model checkpoint licence and provenance must be reviewed by the operator.",
        ],
    }

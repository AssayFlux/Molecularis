"""Molecularis-owned, allow-listed Samtools/BCFtools operations via pysam.

The adapter deliberately exposes a small set of fixed operations rather than an
arbitrary command/argument endpoint. It never invokes a shell, never downloads
references, and records the exact local reference digest for normalization.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


DEFAULT_MAX_INPUT_BYTES = 32 * 1024 * 1024 * 1024
DEFAULT_MAX_OUTPUT_BYTES = 8 * 1024 * 1024 * 1024


def _pysam() -> Any:
    try:
        import pysam  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "Samtools/BCFtools operations require an approved pinned pysam/HTSlib profile"
        ) from error
    return pysam


def _sha256(path: Path, *, max_bytes: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                raise ValueError(f"{path.name} exceeds configured byte limit")
            digest.update(chunk)
    return digest.hexdigest(), size


def _input(path: str | Path, *, max_bytes: int) -> tuple[Path, str, int]:
    source = Path(path).expanduser().resolve(strict=True)
    if not source.is_file():
        raise ValueError("Input must be a regular file")
    digest, size = _sha256(source, max_bytes=max_bytes)
    return source, digest, size


def _output(path: str | Path, source: Path) -> Path:
    target = Path(path).expanduser().resolve()
    if target == source or target.exists():
        raise ValueError("Output must be a new path distinct from the input")
    if not target.parent.is_dir():
        raise ValueError("Output parent directory must already exist")
    return target


def _finish(
    output: Path, *, engine: str, version: str, operation: str,
    input_sha256: str, input_bytes: int, max_output_bytes: int,
    parameters: dict[str, object], reference: dict[str, object] | None = None,
) -> dict[str, object]:
    if not output.is_file():
        raise RuntimeError(f"{engine} did not create the declared output file")
    output_sha256, output_bytes = _sha256(output, max_bytes=max_output_bytes)
    if output_bytes == 0:
        raise RuntimeError(f"{engine} created an empty output file")
    result: dict[str, object] = {
        "schema": "molecularis.genomics-tool-result.v1",
        "engine": engine,
        "version": version,
        "operation": operation,
        "input": {"sha256": input_sha256, "bytes": input_bytes},
        "output": {"path": str(output), "sha256": output_sha256, "bytes": output_bytes},
        "parameters": parameters,
        "execution_status": "completed",
        "scientific_validation": "not_assessed",
    }
    if reference is not None:
        result["reference"] = reference
    return result


def _threads(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 64:
        raise ValueError("threads must be an integer between 1 and 64")
    return value


def samtools_view(
    input_path: str | Path, output_path: str | Path, *,
    output_format: str = "bam", threads: int = 1,
    reference_fasta: str | Path | None = None,
    max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES,
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES,
) -> dict[str, object]:
    """Convert SAM/BAM/CRAM to SAM/BAM/CRAM with an explicit output format."""
    source, input_hash, input_size = _input(input_path, max_bytes=max_input_bytes)
    target = _output(output_path, source)
    thread_count = _threads(threads)
    if output_format not in {"sam", "bam", "cram"}:
        raise ValueError("output_format must be sam, bam or cram")
    if output_format == "cram" and reference_fasta is None:
        raise ValueError("CRAM output requires an explicit local reference FASTA")
    reference: dict[str, object] | None = None
    args = ["-o", str(target), "-@", str(thread_count)]
    args.extend({"sam": ["-h"], "bam": ["-b"], "cram": ["-C"]}[output_format])
    if reference_fasta is not None:
        ref, ref_hash, ref_size = _input(reference_fasta, max_bytes=max_input_bytes)
        args.extend(["-T", str(ref)])
        reference = {"path": str(ref), "sha256": ref_hash, "bytes": ref_size}
    args.append(str(source))
    pysam = _pysam()
    pysam.samtools.view(*args, catch_stdout=False)
    return _finish(
        target, engine="samtools", version=str(getattr(pysam, "__samtools_version__", "unknown")),
        operation="view", input_sha256=input_hash, input_bytes=input_size,
        max_output_bytes=max_output_bytes,
        parameters={"output_format": output_format, "threads": thread_count},
        reference=reference,
    )


def samtools_sort(
    input_path: str | Path, output_path: str | Path, *, threads: int = 1,
    max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES,
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES,
) -> dict[str, object]:
    """Coordinate-sort an alignment file to a new output path."""
    source, input_hash, input_size = _input(input_path, max_bytes=max_input_bytes)
    target = _output(output_path, source)
    thread_count = _threads(threads)
    pysam = _pysam()
    pysam.samtools.sort("-@", str(thread_count), "-o", str(target), str(source), catch_stdout=False)
    return _finish(
        target, engine="samtools", version=str(getattr(pysam, "__samtools_version__", "unknown")),
        operation="sort", input_sha256=input_hash, input_bytes=input_size,
        max_output_bytes=max_output_bytes, parameters={"threads": thread_count},
    )


def samtools_index(
    input_path: str | Path, *, threads: int = 1,
    max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES,
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES,
) -> dict[str, object]:
    """Create an index beside a BAM/CRAM file and return its digest."""
    source, input_hash, input_size = _input(input_path, max_bytes=max_input_bytes)
    if source.suffix.lower() not in {".bam", ".cram"}:
        raise ValueError("samtools index accepts BAM or CRAM inputs")
    thread_count = _threads(threads)
    pysam = _pysam()
    pysam.samtools.index("-@", str(thread_count), str(source), catch_stdout=False)
    candidates = (Path(str(source) + ".bai"), source.with_suffix(".bai"),
                  Path(str(source) + ".crai"), source.with_suffix(".crai"))
    index = next((item for item in candidates if item.is_file()), None)
    if index is None:
        raise RuntimeError("samtools index did not create a recognized index")
    index_hash, index_size = _sha256(index, max_bytes=max_output_bytes)
    return {
        "schema": "molecularis.genomics-tool-result.v1",
        "engine": "samtools",
        "version": str(getattr(pysam, "__samtools_version__", "unknown")),
        "operation": "index",
        "input": {"sha256": input_hash, "bytes": input_size},
        "output": {"path": str(index), "sha256": index_hash, "bytes": index_size},
        "parameters": {"threads": thread_count},
        "execution_status": "completed",
        "scientific_validation": "not_assessed",
    }


def samtools_flagstat(
    input_path: str | Path, *, max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES,
) -> dict[str, object]:
    """Return Samtools flagstat text for a bounded alignment file."""
    source, input_hash, input_size = _input(input_path, max_bytes=max_input_bytes)
    pysam = _pysam()
    report = pysam.samtools.flagstat(str(source))
    if not isinstance(report, str) or not report.strip():
        raise RuntimeError("samtools flagstat returned no report")
    return {
        "schema": "molecularis.samtools-flagstat.v1",
        "engine": "samtools",
        "version": str(getattr(pysam, "__samtools_version__", "unknown")),
        "input": {"sha256": input_hash, "bytes": input_size},
        "report": report,
        "scientific_validation": "not_assessed",
    }


def bcftools_normalize(
    input_path: str | Path, reference_fasta: str | Path, output_path: str | Path, *,
    split_multiallelic: bool = True, threads: int = 1,
    max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES,
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES,
) -> dict[str, object]:
    """Reference-check and normalize VCF/BCF with explicit local reference provenance."""
    source, input_hash, input_size = _input(input_path, max_bytes=max_input_bytes)
    reference_path, reference_hash, reference_size = _input(
        reference_fasta, max_bytes=max_input_bytes,
    )
    target = _output(output_path, source)
    if target == reference_path:
        raise ValueError("Output cannot overwrite the reference FASTA")
    thread_count = _threads(threads)
    args = ["-f", str(reference_path), "-Oz", "-o", str(target), "--threads", str(thread_count)]
    if split_multiallelic:
        args.extend(["-m", "-any"])
    args.append(str(source))
    pysam = _pysam()
    pysam.bcftools.norm(*args, catch_stdout=False)
    return _finish(
        target, engine="bcftools", version=str(getattr(pysam, "__bcftools_version__", "unknown")),
        operation="norm", input_sha256=input_hash, input_bytes=input_size,
        max_output_bytes=max_output_bytes,
        parameters={"split_multiallelic": split_multiallelic, "threads": thread_count,
                    "output_format": "bgzf-vcf"},
        reference={"path": str(reference_path), "sha256": reference_hash,
                   "bytes": reference_size},
    )

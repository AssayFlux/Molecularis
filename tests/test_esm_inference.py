from __future__ import annotations

from pathlib import Path

import pytest

from molecularis.esm_inference import _model_digest, run_esm_embeddings


def test_model_digest_is_stable_and_content_sensitive(tmp_path: Path) -> None:
    model = tmp_path / "model"
    model.mkdir()
    (model / "config.json").write_text('{"model_type":"esm"}')
    first, size, count = _model_digest(model, max_bytes=1024)
    assert size > 0 and count == 1
    assert _model_digest(model, max_bytes=1024)[0] == first
    (model / "weights.bin").write_bytes(b"weights")
    second, _, _ = _model_digest(model, max_bytes=1024)
    assert second != first


def test_esm_rejects_bad_model_digest_before_loading_runtime(tmp_path: Path) -> None:
    model = tmp_path / "model"
    model.mkdir()
    (model / "config.json").write_text('{"model_type":"esm"}')
    with pytest.raises(ValueError, match="digest"):
        run_esm_embeddings(
            ["ACDE"], model, expected_model_sha256="0" * 64,
        )


@pytest.mark.parametrize("sequence", ["", "ACD*", "ACD-"])
def test_esm_rejects_invalid_sequences(tmp_path: Path, sequence: str) -> None:
    model = tmp_path / "model"
    model.mkdir()
    (model / "config.json").write_text("{}")
    digest = _model_digest(model, max_bytes=1024)[0]
    with pytest.raises(ValueError, match="sequence"):
        run_esm_embeddings([sequence], model, expected_model_sha256=digest)

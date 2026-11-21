from __future__ import annotations

import io
import json

import pytest

from molecularis.galaxy import GalaxyClient


class Response:
    def __init__(self, payload: object):
        self.data = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size: int = -1) -> bytes:
        return self.data if size < 0 else self.data[:size]


class Opener:
    def __init__(self, *payloads: object):
        self.payloads = list(payloads)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        return Response(self.payloads.pop(0))


def test_galaxy_client_sends_api_key_only_as_header_and_creates_history() -> None:
    opener = Opener({"id": "history-1", "name": "test"})
    client = GalaxyClient("https://galaxy.example.org", "secret-key", opener=opener)
    result = client.create_history("test")
    request, timeout = opener.requests[0]
    assert result == {"history_id": "history-1", "name": "test"}
    assert request.get_header("X-api-key") == "secret-key"
    assert "secret-key" not in request.full_url
    assert timeout == 30.0


def test_galaxy_client_invokes_workflow_and_returns_provenance() -> None:
    opener = Opener({"id": "inv-1", "state": "new"},
                    {"id": "inv-1", "state": "ok", "outputs": {"out": ["dataset-1"]}})
    client = GalaxyClient("https://galaxy.example.org", "key", opener=opener)
    submitted = client.invoke_workflow("workflow-1", "history-1", {"input-1": {"id": "dataset-1"}})
    result = client.get_invocation("workflow-1", submitted["invocation_id"])
    assert submitted["state"] == "new"
    assert result["state"] == "ok"
    assert result["outputs"] == {"out": ["dataset-1"]}
    assert result["provenance"]["retrieved_via"] == "Galaxy REST API"


def test_galaxy_client_rejects_non_tls_remote_server_and_unsafe_ids() -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        GalaxyClient("http://galaxy.example.org", "key")
    client = GalaxyClient("https://galaxy.example.org", "key", opener=Opener())
    with pytest.raises(ValueError, match="workflow_id"):
        client.invoke_workflow("../other", "history-1", {"input-1": {}})
    with pytest.raises(ValueError, match="inputs"):
        client.invoke_workflow("workflow-1", "history-1", {})


def test_galaxy_client_rejects_redirects_and_oversized_responses() -> None:
    from urllib.error import HTTPError

    class RedirectingOpener:
        def open(self, request, timeout):
            raise HTTPError(request.full_url, 302, "redirect", {}, io.BytesIO(b""))

    client = GalaxyClient("https://galaxy.example.org", "key", opener=RedirectingOpener())
    with pytest.raises(RuntimeError, match="HTTP 302"):
        client.create_history("test")

    class LargeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, size=-1):
            return b"x" * size

    class LargeOpener:
        def open(self, request, timeout):
            return LargeResponse()

    client = GalaxyClient("https://galaxy.example.org", "key",
                          max_response_bytes=10, opener=LargeOpener())
    with pytest.raises(RuntimeError, match="exceeds"):
        client.create_history("test")


def test_galaxy_upload_records_file_digest_and_dataset_id(tmp_path) -> None:
    source = tmp_path / "reads.fastq"
    source.write_bytes(b"@r1\\nACGT\\n+\\n!!!!\\n")
    opener = Opener([{"id": "dataset-1", "state": "ok"}])
    client = GalaxyClient("https://galaxy.example.org", "key", opener=opener)
    result = client.upload_file("history-1", source, file_type="fastqsanger")
    assert result["dataset_id"] == "dataset-1"
    assert result["size_bytes"] == source.stat().st_size
    assert len(result["sha256"]) == 64
    request, _ = opener.requests[0]
    assert request.get_header("Content-type").startswith("multipart/form-data")
    assert b"reads.fastq" in request.data

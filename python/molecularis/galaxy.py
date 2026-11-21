"""Credential-injected, bounded Galaxy REST client for Molecularis workflows.

The client submits caller-selected workflows to a separately operated Galaxy server.
It does not trust workflow outputs, reinterpret tool results, or claim scientific
validation. API keys are sent only in the x-api-key header and never returned.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,200}$")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str,
                         headers: Any, newurl: str) -> None:
        raise urllib.error.HTTPError(req.full_url, code, "Redirects are disabled", headers, fp)


class GalaxyClient:
    """Small synchronous Galaxy client with explicit limits and provenance."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout_seconds: float = 30.0,
        max_response_bytes: int = 16 * 1024 * 1024,
        opener: Any | None = None,
    ) -> None:
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("base_url must be non-empty")
        parsed = urllib.parse.urlsplit(base_url.strip())
        local_http = parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        if parsed.scheme != "https" and not (parsed.scheme == "http" and local_http):
            raise ValueError("Galaxy base_url must use HTTPS (HTTP is allowed only for loopback tests)")
        if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Galaxy base_url must be an origin/path without credentials, query or fragment")
        if not isinstance(api_key, str) or not api_key.strip() or len(api_key) > 4096:
            raise ValueError("api_key must be non-empty text")
        if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)) or not 0 < timeout_seconds <= 600:
            raise ValueError("timeout_seconds must be in (0, 600]")
        if isinstance(max_response_bytes, bool) or not isinstance(max_response_bytes, int) or not 1 <= max_response_bytes <= 128 * 1024 * 1024:
            raise ValueError("max_response_bytes must be in [1, 128 MiB]")
        self._base = base_url.strip().rstrip("/")
        self._key = api_key
        self._timeout = float(timeout_seconds)
        self._max_response = max_response_bytes
        self._opener = opener or urllib.request.build_opener(_NoRedirect())

    @staticmethod
    def _identifier(value: str, name: str) -> str:
        if not isinstance(value, str) or not _ID.fullmatch(value):
            raise ValueError(f"{name} must be a safe Galaxy identifier")
        return value

    def _request(self, method: str, path: str, payload: bytes | None = None,
                 content_type: str = "application/json") -> Any:
        if not path.startswith("/api/") or "?" in path or "#" in path:
            raise ValueError("Galaxy API path must be a fixed /api/ path without query")
        request = urllib.request.Request(
            self._base + path,
            data=payload,
            headers={"x-api-key": self._key, "Accept": "application/json",
                     "Content-Type": content_type},
            method=method,
        )
        try:
            response = self._opener.open(request, timeout=self._timeout)
            with response:
                raw = response.read(self._max_response + 1)
        except urllib.error.HTTPError as exc:
            # Do not include request headers or the API key in surfaced errors.
            detail = exc.read(min(self._max_response, 4096)).decode("utf-8", "replace")
            raise RuntimeError(f"Galaxy API returned HTTP {exc.code}: {detail[:1000]}") from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"Galaxy API request failed: {type(exc).__name__}") from None
        if len(raw) > self._max_response:
            raise RuntimeError("Galaxy API response exceeds max_response_bytes")
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise RuntimeError("Galaxy API returned a non-JSON response") from None

    def create_history(self, name: str) -> dict[str, Any]:
        if not isinstance(name, str) or not name.strip() or len(name) > 200:
            raise ValueError("history name must be 1..200 characters")
        result = self._request("POST", "/api/histories",
                               json.dumps({"name": name.strip()}).encode())
        if not isinstance(result, dict) or not isinstance(result.get("id"), str):
            raise RuntimeError("Galaxy did not return a history id")
        return {"history_id": self._identifier(result["id"], "history_id"),
                "name": result.get("name", name.strip())}

    def upload_file(self, history_id: str, file_path: str | Path, *,
                    file_type: str = "auto", max_file_bytes: int = 2 * 1024**3) -> dict[str, Any]:
        history = self._identifier(history_id, "history_id")
        if not isinstance(file_type, str) or not re.fullmatch(r"[A-Za-z0-9_.+-]{1,40}", file_type):
            raise ValueError("file_type must be a safe Galaxy datatype name")
        path = Path(file_path).expanduser().resolve(strict=True)
        if not path.is_file() or path.is_symlink():
            raise ValueError("upload input must be a regular non-symlink file")
        size = path.stat().st_size
        if size <= 0 or size > max_file_bytes:
            raise ValueError("upload file size is outside configured bounds")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        boundary = "molecularis-" + os.urandom(16).hex()
        filename = path.name.replace('"', "_").replace("\\r", "_").replace("\\n", "_")
        chunks = [
            f"--{boundary}\\r\\nContent-Disposition: form-data; name=\"history_id\"\\r\\n\\r\\n{history}\\r\\n".encode(),
            f"--{boundary}\\r\\nContent-Disposition: form-data; name=\"tool_id\"\\r\\n\\r\\nupload1\\r\\n".encode(),
            f"--{boundary}\\r\\nContent-Disposition: form-data; name=\"files_0|type\"\\r\\n\\r\\n{file_type}\\r\\n".encode(),
            f"--{boundary}\\r\\nContent-Disposition: form-data; name=\"files_0|file_data\"; filename=\"{filename}\"\\r\\nContent-Type: application/octet-stream\\r\\n\\r\\n".encode(),
        ]
        with path.open("rb") as stream:
            file_bytes = stream.read(max_file_bytes + 1)
        if len(file_bytes) != size:
            raise RuntimeError("upload file changed while being read")
        body = b"".join(chunks) + file_bytes + f"\\r\\n--{boundary}--\\r\\n".encode()
        result = self._request("POST", "/api/tools", body,
                               f"multipart/form-data; boundary={boundary}")
        datasets = result if isinstance(result, list) else [result]
        if not datasets or not isinstance(datasets[0], dict) or not isinstance(datasets[0].get("id"), str):
            raise RuntimeError("Galaxy upload response did not contain a dataset id")
        dataset_id = self._identifier(datasets[0]["id"], "dataset_id")
        return {"dataset_id": dataset_id, "history_id": history, "filename": path.name,
                "size_bytes": size, "sha256": digest.hexdigest(),
                "galaxy_state": datasets[0].get("state", "unknown")}

    def invoke_workflow(self, workflow_id: str, history_id: str,
                        inputs: dict[str, Any], *,
                        parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        workflow = self._identifier(workflow_id, "workflow_id")
        history = self._identifier(history_id, "history_id")
        if not isinstance(inputs, dict) or not inputs or len(inputs) > 500:
            raise ValueError("inputs must be a non-empty mapping of Galaxy workflow input ids")
        if any(not isinstance(key, str) or not _ID.fullmatch(key) for key in inputs):
            raise ValueError("workflow input keys must be safe identifiers")
        if parameters is not None and not isinstance(parameters, dict):
            raise ValueError("parameters must be an object")
        body = {"history_id": history, "inputs": inputs, "parameters": parameters or {}}
        result = self._request("POST", f"/api/workflows/{urllib.parse.quote(workflow, safe='')}/invocations",
                               json.dumps(body, separators=(",", ":"), allow_nan=False).encode())
        if not isinstance(result, dict) or not isinstance(result.get("id"), str):
            raise RuntimeError("Galaxy did not return an invocation id")
        return {"invocation_id": self._identifier(result["id"], "invocation_id"),
                "workflow_id": workflow, "history_id": history,
                "state": result.get("state", "new")}

    def get_invocation(self, workflow_id: str, invocation_id: str) -> dict[str, Any]:
        workflow = self._identifier(workflow_id, "workflow_id")
        invocation = self._identifier(invocation_id, "invocation_id")
        result = self._request(
            "GET", f"/api/workflows/{urllib.parse.quote(workflow, safe='')}/invocations/{urllib.parse.quote(invocation, safe='')}",
        )
        if not isinstance(result, dict):
            raise RuntimeError("Galaxy invocation response must be an object")
        return {"invocation_id": invocation, "workflow_id": workflow,
                "state": result.get("state", "unknown"),
                "outputs": result.get("outputs", {}),
                "output_datasets": result.get("output_datasets", []),
                "provenance": {"server": self._base, "retrieved_via": "Galaxy REST API"}}

    def wait_for_invocation(self, workflow_id: str, invocation_id: str, *,
                            timeout_seconds: float = 3600, poll_seconds: float = 5) -> dict[str, Any]:
        if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)) or not 0 < timeout_seconds <= 86400:
            raise ValueError("timeout_seconds must be in (0, 86400]")
        if isinstance(poll_seconds, bool) or not isinstance(poll_seconds, (int, float)) or not 0.2 <= poll_seconds <= 60:
            raise ValueError("poll_seconds must be in [0.2, 60]")
        deadline = time.monotonic() + timeout_seconds
        while True:
            result = self.get_invocation(workflow_id, invocation_id)
            if result["state"] in {"ok", "error", "failed", "cancelled"}:
                return result
            if time.monotonic() >= deadline:
                return {**result, "state": "timeout", "terminal": False}
            time.sleep(poll_seconds)

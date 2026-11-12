from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import secrets
import shutil
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

DATA_DIR = Path(os.getenv("MOLECULARIS_DATA_DIR", "./astronaut-data")).resolve()
DATASETS = DATA_DIR / "datasets"
MODELS_DIR = Path(os.getenv("MOLECULARIS_MODELS_DIR", str(DATA_DIR / "models"))).resolve()
ARTIFACTS_DIR = DATA_DIR / "artifacts"
DB_PATH = DATA_DIR / "astronaut.sqlite3"
for directory in (DATASETS, MODELS_DIR, ARTIFACTS_DIR):
    directory.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Molecularis Training API",
    version="0.3.0",
    description="Authenticated local dataset and GPU fine-tuning control plane",
)


def connect() -> sqlite3.Connection:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db


def init_db() -> None:
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS datasets(
                id TEXT PRIMARY KEY, name TEXT NOT NULL, filename TEXT NOT NULL,
                path TEXT NOT NULL, sha256 TEXT NOT NULL, bytes INTEGER NOT NULL,
                rows INTEGER NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS jobs(
                id TEXT PRIMARY KEY, dataset_id TEXT NOT NULL, base_model TEXT NOT NULL,
                method TEXT NOT NULL, state TEXT NOT NULL, progress REAL NOT NULL,
                message TEXT NOT NULL, config TEXT NOT NULL, created_at TEXT NOT NULL,
                FOREIGN KEY(dataset_id) REFERENCES datasets(id)
            );
            """
        )


@app.on_event("startup")
def startup() -> None:
    init_db()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("MOLECULARIS_API_KEY", "")
    if not expected:
        raise HTTPException(503, "Training API is locked. Configure MOLECULARIS_API_KEY before use.")
    if not x_api_key or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(401, "Invalid or missing API key.")


def resolve_local_model(model_value: str) -> Path:
    try:
        model_path = Path(model_value).expanduser().resolve(strict=True)
        model_path.relative_to(MODELS_DIR)
    except (OSError, ValueError):
        raise HTTPException(422, "Base model must be an existing local directory inside MOLECULARIS_MODELS_DIR.")
    if not model_path.is_dir():
        raise HTTPException(422, "Base model path must be a local model directory.")
    return model_path


class DatasetInfo(BaseModel):
    id: str
    name: str
    filename: str
    sha256: str
    bytes: int
    rows: int
    created_at: str


class TrainRequest(BaseModel):
    dataset_id: str
    base_model: str = Field(min_length=1, max_length=512)
    method: str = Field(default="lora", pattern="^(lora|qlora)$")
    epochs: int = Field(default=1, ge=1, le=10)
    learning_rate: float = Field(default=0.0002, gt=0, le=0.01)
    rank: int = Field(default=8, ge=1, le=128)
    output_name: str = Field(default="astronaut-adapter", min_length=1, max_length=80)


def validate_jsonl(path: Path) -> int:
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise HTTPException(422, f"Invalid JSON on line {line_no}: {exc.msg}") from exc
            if not isinstance(row, dict) or not any(k in row for k in ("text", "messages", "prompt")):
                raise HTTPException(422, f"Line {line_no} must be an object with text, messages, or prompt")
            count += 1
    if count == 0:
        raise HTTPException(422, "Dataset contains no usable records")
    return count


def job_record(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "dataset_id": row["dataset_id"],
        "base_model": row["base_model"],
        "method": row["method"],
        "state": row["state"],
        "progress": row["progress"],
        "message": row["message"],
        "created_at": row["created_at"],
        "artifact_url": f"/v1/training/jobs/{row['id']}/artifact" if row["state"] == "completed" else None,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "authenticated-local-training-control-plane"}


@app.post("/v1/datasets", response_model=DatasetInfo, dependencies=[Depends(require_api_key)])
async def upload_dataset(file: UploadFile = File(...)) -> DatasetInfo:
    filename = Path(file.filename or "dataset.jsonl").name
    if not filename.lower().endswith(".jsonl"):
        raise HTTPException(415, "Only JSONL datasets are supported in this API version")
    dataset_id = str(uuid.uuid4())
    target = DATASETS / f"{dataset_id}.jsonl"
    digest = hashlib.sha256()
    size = 0
    try:
        with target.open("wb") as out:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > 512 * 1024 * 1024:
                    raise HTTPException(413, "Dataset exceeds 512 MiB limit")
                digest.update(chunk)
                out.write(chunk)
        rows = validate_jsonl(target)
    except Exception:
        target.unlink(missing_ok=True)
        raise
    record = DatasetInfo(
        id=dataset_id,
        name=Path(filename).stem,
        filename=filename,
        sha256=digest.hexdigest(),
        bytes=size,
        rows=rows,
        created_at=now(),
    )
    with connect() as db:
        db.execute(
            "INSERT INTO datasets VALUES(?,?,?,?,?,?,?,?)",
            (record.id, record.name, record.filename, str(target), record.sha256, record.bytes, record.rows, record.created_at),
        )
    return record


@app.get("/v1/datasets", response_model=list[DatasetInfo], dependencies=[Depends(require_api_key)])
def list_datasets() -> list[DatasetInfo]:
    with connect() as db:
        rows = db.execute("SELECT * FROM datasets ORDER BY created_at DESC").fetchall()
    return [
        DatasetInfo(
            id=row["id"], name=row["name"], filename=row["filename"], sha256=row["sha256"],
            bytes=row["bytes"], rows=row["rows"], created_at=row["created_at"],
        )
        for row in rows
    ]


@app.post("/v1/training/jobs", dependencies=[Depends(require_api_key)])
def create_training_job(request: TrainRequest) -> dict[str, Any]:
    model_path = resolve_local_model(request.base_model)
    with connect() as db:
        if db.execute("SELECT id FROM datasets WHERE id=?", (request.dataset_id,)).fetchone() is None:
            raise HTTPException(404, "Dataset not found")
        job_id = str(uuid.uuid4())
        worker_enabled = os.getenv("MOLECULARIS_ENABLE_TRAINING") == "1" and bool(os.getenv("MOLECULARIS_REDIS_URL"))
        state = "blocked"
        message = "Request recorded; GPU training worker is not configured."
        if worker_enabled:
            state = "queued"
            message = "Queued for the configured GPU worker."
        config = request.model_dump()
        config["base_model"] = str(model_path)
        db.execute(
            "INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?)",
            (job_id, request.dataset_id, str(model_path), request.method, state, 0.0, message, json.dumps(config), now()),
        )
    if worker_enabled:
        try:
            from molecularis_api.worker import celery_app
            celery_app.send_task("astronaut.train", args=[job_id], task_id=job_id)
        except Exception as exc:
            state = "blocked"
            message = f"Could not enqueue training job: {type(exc).__name__}"
            with connect() as db:
                db.execute("UPDATE jobs SET state=?,message=? WHERE id=?", (state, message, job_id))
    return {"id": job_id, "state": state, "progress": 0, "message": message}


@app.get("/v1/training/jobs", dependencies=[Depends(require_api_key)])
def list_training_jobs() -> list[dict[str, Any]]:
    with connect() as db:
        rows = db.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
    return [job_record(row) for row in rows]


@app.get("/v1/training/jobs/{job_id}", dependencies=[Depends(require_api_key)])
def get_training_job(job_id: str) -> dict[str, Any]:
    with connect() as db:
        row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "Training job not found")
    return job_record(row)


@app.post("/v1/training/jobs/{job_id}/cancel", dependencies=[Depends(require_api_key)])
def cancel_training_job(job_id: str) -> dict[str, Any]:
    with connect() as db:
        row = db.execute("SELECT state FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "Training job not found")
    if row["state"] in {"completed", "failed", "cancelled"}:
        return {"id": job_id, "state": row["state"], "message": "Job is already terminal."}
    try:
        from molecularis_api.worker import celery_app
        celery_app.control.revoke(job_id, terminate=True, signal="SIGTERM")
    except Exception:
        pass
    with connect() as db:
        db.execute("UPDATE jobs SET state=?,message=? WHERE id=?", ("cancelled", "Cancellation requested.", job_id))
    return {"id": job_id, "state": "cancelled", "message": "Cancellation requested."}


@app.get("/v1/training/jobs/{job_id}/artifact", dependencies=[Depends(require_api_key)])
def download_training_artifact(job_id: str) -> FileResponse:
    with connect() as db:
        row = db.execute("SELECT state FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "Training job not found")
    if row["state"] != "completed":
        raise HTTPException(409, "Training artifact is not ready.")
    job_dir = (ARTIFACTS_DIR / job_id).resolve()
    try:
        job_dir.relative_to(ARTIFACTS_DIR.resolve())
    except ValueError:
        raise HTTPException(400, "Invalid artifact path.")
    if not job_dir.is_dir():
        raise HTTPException(404, "Training artifact directory not found.")
    archive = ARTIFACTS_DIR / f"{job_id}.zip"
    if not archive.exists():
        with ZipFile(archive, "w") as output:
            for path in job_dir.rglob("*"):
                if path.is_file():
                    output.write(path, path.relative_to(job_dir))
    return FileResponse(archive, media_type="application/zip", filename=f"astronaut-training-{job_id}.zip")


@app.get("/v1/system/capabilities")
def capabilities() -> dict[str, Any]:
    return {
        "training_worker_configured": os.getenv("MOLECULARIS_ENABLE_TRAINING") == "1" and bool(os.getenv("MOLECULARIS_REDIS_URL")),
        "torch_installed": importlib.util.find_spec("torch") is not None,
        "transformers_installed": importlib.util.find_spec("transformers") is not None,
        "trl_installed": importlib.util.find_spec("trl") is not None,
        "peft_installed": importlib.util.find_spec("peft") is not None,
    }

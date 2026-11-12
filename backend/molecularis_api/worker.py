from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from celery import Celery

DATA_DIR = Path(os.getenv("MOLECULARIS_DATA_DIR", "./astronaut-data")).resolve()
DB_PATH = DATA_DIR / "astronaut.sqlite3"
ARTIFACTS = DATA_DIR / "artifacts"
REDIS_URL = os.getenv("MOLECULARIS_REDIS_URL", "redis://127.0.0.1:6379/0")
celery_app = Celery("astronaut", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_prefetch_multiplier=1,
)


def update_job(job_id: str, state: str, message: str, progress: float | None = None) -> None:
    with sqlite3.connect(DB_PATH) as db:
        if progress is None:
            db.execute("UPDATE jobs SET state=?, message=? WHERE id=?", (state, message, job_id))
        else:
            db.execute("UPDATE jobs SET state=?, message=?, progress=? WHERE id=?", (state, message, progress, job_id))
        db.commit()


@celery_app.task(name="astronaut.train")
def train_job(job_id: str) -> dict:
    with sqlite3.connect(DB_PATH) as db:
        row = db.execute("SELECT dataset_id, base_model, config FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row is None:
            raise ValueError("Training job not found")
        dataset_id, base_model, config_json = row
        dataset = db.execute("SELECT path FROM datasets WHERE id=?", (dataset_id,)).fetchone()
        if dataset is None:
            raise ValueError("Training dataset not found")
    config = json.loads(config_json)
    update_job(job_id, "running", "GPU worker started training", 0.0)
    try:
        from molecularis_api.trainer import train_lora
        result = train_lora(
            dataset[0],
            base_model,
            config,
            str(ARTIFACTS / job_id),
            progress_callback=lambda progress, message: update_job(job_id, "running", message, progress),
        )
        update_job(job_id, "completed", "Training completed; adapter and manifest saved", 100.0)
        return result
    except Exception as exc:
        update_job(job_id, "failed", f"Training failed: {type(exc).__name__}: {exc}")
        raise

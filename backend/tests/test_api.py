from fastapi.testclient import TestClient
from molecularis_api import main


def make_client(tmp_path, monkeypatch):
    data = tmp_path / "data"
    datasets = data / "datasets"
    models = data / "models"
    datasets.mkdir(parents=True)
    models.mkdir(parents=True)
    (models / "base").mkdir()
    monkeypatch.setattr(main, "DATA_DIR", data)
    monkeypatch.setattr(main, "DATASETS", datasets)
    monkeypatch.setattr(main, "MODELS_DIR", models)
    monkeypatch.setattr(main, "ARTIFACTS_DIR", data / "artifacts")
    monkeypatch.setattr(main, "DB_PATH", data / "test.sqlite3")
    monkeypatch.setenv("MOLECULARIS_API_KEY", "test-secret-key")
    monkeypatch.delenv("MOLECULARIS_ENABLE_TRAINING", raising=False)
    monkeypatch.delenv("MOLECULARIS_REDIS_URL", raising=False)
    main.init_db()
    return TestClient(main.app)


AUTH = {"X-API-Key": "test-secret-key"}


def test_upload_list_and_job_is_blocked_without_worker(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)
    payload = b'{"text":"hello world"}\n{"prompt":"write a test","completion":"assert true"}\n'
    response = client.post("/v1/datasets", files={"file": ("examples.jsonl", payload, "application/jsonl")}, headers=AUTH)
    assert response.status_code == 200
    dataset = response.json()
    assert dataset["rows"] == 2
    assert len(dataset["sha256"]) == 64
    assert client.get("/v1/datasets", headers=AUTH).json()[0]["id"] == dataset["id"]
    job = client.post(
        "/v1/training/jobs",
        json={"dataset_id": dataset["id"], "base_model": str(main.MODELS_DIR / "base")},
        headers=AUTH,
    )
    assert job.status_code == 200
    assert job.json()["state"] == "blocked"
    assert "worker is not configured" in job.json()["message"].lower()
    assert client.get("/v1/training/jobs", headers=AUTH).json()[0]["id"] == job.json()["id"]


def test_api_requires_key(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)
    response = client.get("/v1/datasets")
    assert response.status_code == 401


def test_base_model_must_be_inside_local_models_directory(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)
    payload = b'{"text":"hello"}\n'
    dataset = client.post("/v1/datasets", files={"file": ("examples.jsonl", payload)}, headers=AUTH).json()
    response = client.post(
        "/v1/training/jobs",
        json={"dataset_id": dataset["id"], "base_model": str(tmp_path)},
        headers=AUTH,
    )
    assert response.status_code == 422


def test_invalid_jsonl_is_rejected(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)
    response = client.post("/v1/datasets", files={"file": ("broken.jsonl", b'not-json\n', "application/jsonl")}, headers=AUTH)
    assert response.status_code == 422


def test_non_jsonl_is_rejected(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)
    response = client.post("/v1/datasets", files={"file": ("data.csv", b"a,b\n1,2\n", "text/csv")}, headers=AUTH)
    assert response.status_code == 415

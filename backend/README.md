# Molecularis Training API

Self-hosted control plane for local JSONL dataset registration and optional GPU LoRA/QLoRA training. The API is not a hosted service: run it on your own workstation/server. The Celery worker performs GPU training on a separate machine.

## API development

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export MOLECULARIS_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export MOLECULARIS_DATA_DIR="$PWD/astronaut-data"
mkdir -p "$MOLECULARIS_DATA_DIR/models"
uvicorn molecularis_api.main:app --host 127.0.0.1 --port 8080
```

Place an already-downloaded Hugging Face model directory inside `$MOLECULARIS_DATA_DIR/models`. The API rejects model paths outside that directory and the trainer uses `local_files_only=True`; it does not fetch arbitrary models from the internet.

Authenticated routes require the `X-API-Key` header. `/health` remains public. Never expose the API publicly without TLS, firewalling and a strong API key. Do not expose Redis or the Celery worker to the public internet.

## GPU worker setup

Use a Linux host with a compatible NVIDIA CUDA stack. Install optional ML dependencies:

```bash
pip install -r requirements-training.txt
export MOLECULARIS_DATA_DIR=/srv/astronaut-data
export MOLECULARIS_MODELS_DIR=/srv/astronaut-data/models
export MOLECULARIS_REDIS_URL=redis://127.0.0.1:6379/0
export MOLECULARIS_ENABLE_TRAINING=1
celery -A molecularis_api.worker.celery_app worker --loglevel=INFO --concurrency=1
```

Start Redis and the API with the same data directory, model directory and environment variables. Both processes must see the same dataset and SQLite paths. For multi-worker/production use, replace SQLite with PostgreSQL and use shared object storage.

## Training pipeline

- JSONL records may use `text`, `messages`, or `prompt`/ `completion`.
- The worker supports PEFT LoRA and QLoRA adapters and requires a CUDA GPU.
- The first trainer targets Llama-style `q_proj` and `v_proj` modules. Other architectures need an explicit target-module configuration.
- The API exposes dataset upload/list, training job create/list/status/cancel, capability checks and completed adapter ZIP download.
- Progress is written to SQLite from Hugging Face Trainer callbacks.
- Artifacts are PEFT adapter weights plus a manifest. They are **not** directly importable `.litertlm` files; conversion/merge/export for the Android runtime is a separate step.

## Mobile model export and provenance

The training worker produces PEFT adapter artifacts, not Android-ready LiteRT-LM model files. A compatible external converter must merge/convert the base model and adapter first. After conversion, package the resulting `.litertlm` file and its source adapter provenance:

```bash
python -m molecularis_api.mobile_export \
  --converted-model /path/to/converted.litertlm \
  --adapter-zip /path/to/adapter.zip \
  --metadata-json export-metadata.json \
  --output-dir ./mobile-release
```

The packaging command validates archive paths, records SHA-256 checksums for both source adapter and converted artifact, and writes a compatibility/license/converter manifest. It does not implement model conversion or verify internal LiteRT-LM tensor semantics. The publisher must sign the catalog payload separately; never store its private signing key in the app or repository.

## Security and operations

- API key authentication is mandatory for all dataset and job routes.
- Base models must be local directories under `MOLECULARIS_MODELS_DIR`; the trainer is offline with respect to model downloads.
- Uploads are capped at 512 MiB; app-side JSONL preparation is capped at 20 MiB.
- Run one GPU worker per device initially. Add quotas, TLS, audit logging, retention/cleanup, PostgreSQL, object storage and per-user authorization before multi-user deployment.

## Publisher catalog signing

Install the normal backend requirements, then generate a dedicated Ed25519 keypair:

```bash
python -m molecularis_api.catalog_signing generate-keypair --private-key ./secrets/catalog-private.pem --public-key ./catalog-public-key.base64
python -m molecularis_api.catalog_signing sign --manifest ./mobile-release/manifest.json --base-download-url https://models.example.org/releases --private-key ./secrets/catalog-private.pem --output ./public/catalog.signed.json
```

Keep the private key in a protected offline secret store; never commit it or include it in the Android app. The public-key file contains the Base64 X.509 Ed25519 public key. Configure Android release builds with Gradle properties `MOLECULARIS_CATALOG_URL` and `MOLECULARIS_CATALOG_PUBLIC_KEY` (the Base64 public-key contents), preferably in an untracked local Gradle properties file or protected CI configuration. The signature covers the exact canonical UTF-8 JSON payload. The app never trusts a key supplied by the catalog itself. Key rotation requires a trusted app update.

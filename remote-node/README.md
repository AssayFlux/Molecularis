# Molecularis private research compute worker

This is a dependency-free Node 22 HTTP/TLS front end for the pinned Python AutoDock Vina 1.2.7 runner. It is not a public API and it does not expose molecular-dynamics execution.

## Default safety posture

- Binds to `127.0.0.1:8765`.
- Docking is **disabled** unless `MOLECULARIS_NODE_ALLOW_DOCKING=true`.
- Enabled mode requires a random `MOLECULARIS_NODE_AUTH_TOKEN` of at least 32 characters.
- Non-loopback binding is refused unless both TLS certificate and private-key paths are configured.
- One job at a time; request body limited to 20 MiB; job timeout 15 minutes; result stdout capped at 32 MiB.
- No CORS, cookies, job persistence, arbitrary paths, shell command, or caller-selected executable.
- The Python child receives an allow-listed environment; the Node bearer token is not passed to it.
- Inputs are prepared PDBQT only. The Python runner validates the request schema and output schema, hashes inputs/protocol/engine binary and uses a temporary directory that is removed after execution.
- MD is explicitly disabled at this service boundary. OpenMM remains a separately invoked host API until a trusted system builder, approved force-field parameter set and node resource policy exist.

## Install and run

From the repository root, install the project and pinned docking extra in a dedicated virtual environment:

```sh
python -m pip install -e '.[dev,docking]'
cd remote-node
npm test
MOLECULARIS_NODE_AUTH_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')" \
MOLECULARIS_NODE_ALLOW_DOCKING=false \
node server.mjs
```

The default service remains disabled. To enable research docking, explicitly set `MOLECULARIS_NODE_ALLOW_DOCKING=true` and provide the token through the host's secret manager, not a committed file or shell history. Keep the worker loopback-only unless there is a managed TLS certificate, network firewall, access control, monitoring and security review.

For remote binding, set `MOLECULARIS_NODE_HOST`, `MOLECULARIS_NODE_TLS_CERT` and `MOLECULARIS_NODE_TLS_KEY`. TLS certificate/key files must be readable by the service account. Never expose a plain-HTTP non-loopback listener.

## Endpoints

- `GET /health`: non-sensitive readiness and enabled/disabled status.
- `POST /v1/docking`: bearer-authenticated, owner-authorized research docking request defined by `api/docking-execution.schema.json`.

A successful response conforms to `api/insilico-result.schema.json` and has `validation_status=not_independently_validated`. Scores are not experimental binding free energies or evidence of activity.

## Still required before production node use

The service has not been deployed to or security-tested on a project compute node. The complete Vina binary dependency SBOM/provenance review, host hardening, TLS and firewall configuration, encrypted storage/retention policy, job quotas, monitoring, recovery and independent docking validation remain open. Owner permission to implement the worker does not waive those checks.

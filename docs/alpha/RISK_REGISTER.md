# Alpha Initial Risk Register

| ID | Risk | Impact | Mitigation / exit evidence |
|---|---|---|---|
| R1 | Existing Android architecture and user data are tightly coupled | Data loss or costly rewrite | Source inventory, migration ledger, export/import and parity tests |
| R2 | Current repository contains legacy/partial foundations | False implementation claims | Exact-base audit, tests and evidence classification |
| R3 | Cross-device offline sync conflicts | User data corruption | Immutable artifacts, idempotency, conflict UI and recovery tests |
| R4 | Local node expands attack surface | Host compromise | Rust supervisor, explicit pairing, allowlists, isolation, signed manifests |
| R5 | Notebook/agent arbitrary code execution | Data exfiltration or host compromise | Isolated kernels, quotas, network restrictions and no host secrets |
| R6 | Upstream license/model/data terms differ | Redistribution or use violation | Per-component license and provenance register |
| R7 | Scientific output not sufficiently validated | Misleading research conclusions | Reference benchmarks, uncertainty, independent domain review |
| R8 | Large model/database footprint | Cost and operational burden | Optional profiles, user-selected compute, storage estimates and quotas |
| R9 | GPU/runtime fragmentation | Inconsistent results and support burden | Declared runtime matrix, containers and hardware-specific validation |
| R10 | Cloud/HPC data placement unclear | Privacy/compliance breach | Compute-location disclosure, opt-in transfer and institutional policy |
| R11 | Scope expansion across twelve upstream projects | Schedule and quality degradation | Vertical slices, milestone gates and prioritization |
| R12 | Clinical use inferred from research features | Safety/regulatory risk | Research-only UX, claims review and explicit future authorization gate |

Risk owners and severity scores must be assigned during M0; do not invent named owners.
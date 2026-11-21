# Molecularis platform/software-methods manuscript — working skeleton

> **Status: preparation only. Not submission-ready.** Populate results only from committed, reproducible validation outputs. Do not invent sample sizes, metrics, performance, accuracy or scientific findings.

## Working title
Molecularis: an offline-first, provenance-aware Android workbench for reproducible computational biology research

## Abstract (draft outline)
- Background and unmet research-workflow need.
- Objective and intended users (research use; non-clinical).
- Methods: architecture, supported analyses, execution modes and provenance model.
- Evaluation: independent reference datasets, prespecified metrics, device/resource tests and reproducibility.
- Results: **reserved for measured, independently validated results only**.
- Conclusions and limitations: clearly distinguish software correctness from scientific validity and experimental confirmation.

## 1. Introduction
Describe the research problem, existing tools/workflows and the specific gap addressed. Support all claims with current primary literature and avoid unsupported novelty claims.

## 2. Intended use and scope
Define research-only use, supported input types, local/offline boundaries, optional remote-node execution and explicit exclusions. State that predictions are hypotheses and are not clinical advice.

## 3. Software architecture
Document Android/Compose client, typed orchestration boundary, Python/Rust/C++ components, job lifecycle, storage, provenance, data-pack management and security model. Include a versioned architecture diagram generated from source documentation.

## 4. Methods and implemented capabilities
For each included capability provide: phase ID, algorithm, implementation commit, dependency/model/database version, input validation, parameter defaults, complexity/resource bounds, failure behaviour and limitations. Exclude roadmap-only capabilities.

## 5. Evaluation protocol
Prespecify:
- Reference datasets and accessions/releases, inclusion/exclusion criteria and license.
- Independent baselines and version pins.
- Positive, negative, boundary and adversarial fixtures.
- Metrics, confidence intervals, tolerances, statistical tests and multiplicity correction.
- Hardware/device matrix and repeated-run policy.
- Missing data, unsupported cases and failure reporting.
- Separation of development fixtures from held-out evaluation data.

## 6. Results
Populate only from immutable machine-readable benchmark outputs. Every table/figure must link to its generation script, input data manifest, output hash and CI/reproduction run.

## 7. Reproducibility and availability
Provide repository commit/tag, environment lockfiles, build instructions, dataset manifests, checksums, reproduction commands, artifact identifiers and software license. Explain any data that cannot be redistributed.

## 8. Security, privacy, licensing and ethics
Provide SBOM, third-party license review, data-flow/threat-model summary, ethics statement and explicit confirmation of whether human/animal data or subjects were involved.

## 9. Discussion
Interpret only measured findings. Discuss applicability domain, bias, device constraints, uncertainty, failure modes and comparison with independent tools.

## 10. Limitations and future work
Separate known implementation limitations from unvalidated algorithms, planned tracks, device limitations and experimental validation requirements.

## Declarations (complete before submission)
- Author contributions:
- Affiliations:
- Funding:
- Competing interests:
- Ethics approval/exemption:
- Data availability:
- Code/software availability:
- Acknowledgements:
- Generative-AI assistance disclosure, according to venue policy:
- Venue-specific reporting checklist:

## Claim-to-evidence ledger
Maintain `paper/claim-evidence-ledger.csv`. Every quantitative or comparative statement in the manuscript must map to a committed result and independent evidence. Claims without evidence are removed or explicitly framed as aims/plans.

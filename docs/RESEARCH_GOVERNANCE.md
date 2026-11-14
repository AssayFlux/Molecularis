# Research governance, ethics, and integrity

**Status:** Project policy and planning document. It is not ethics approval, legal advice, or evidence that a study has been conducted.

## 1. Research boundary

Molecularis is software under development. Its architecture and features may motivate research questions, but the repository itself does not establish novelty, validity, reliability, safety, or educational benefit. Claims must refer to a specific commit/release, configuration, corpus, device environment, and evaluation.

Distinguish at least four claim classes:

1. **Implementation claims:** a feature exists and passes defined software tests.
2. **Technical performance claims:** measured ingestion, retrieval, latency, resource use, citation support, or reliability under a specified protocol.
3. **Expert-quality claims:** domain-qualified assessors rate outputs using a defined rubric with agreement reported.
4. **Learning-effect claims:** outcomes from appropriately designed human-participant studies using defensible measures and comparators.

Evidence for one class does not establish another.

## 2. Ethics review and participant protection

Before recruiting participants, collecting identifiable or sensitive participant data, or conducting an intervention, obtain the appropriate institutional ethics committee/IRB review or a documented determination that review is not required. Requirements vary by jurisdiction and institution. Do not treat a public app, classroom demonstration, or developer's own testing as automatic exemption.

The study protocol must specify:
- Research question, design, primary outcome, hypotheses, and analysis plan.
- Population, eligibility, recruitment, sample-size rationale, compensation, and withdrawal.
- Consent and participant information in an accessible language.
- Risks including inaccurate outputs, overreliance, privacy exposure, distress, and unequal access.
- Data minimization, pseudonymization, access control, storage region, retention, and deletion.
- Cloud AI providers, cross-border transfers, subprocessors, and what content leaves the device.
- Handling of minors, vulnerable groups, and high-impact subject matter.
- Adverse-event escalation, investigator responsibilities, and publication plan.

Do not expose participants to unreviewed medical, legal, financial, or other high-impact advice. Molecularis is not a substitute for qualified professional judgement.

## 3. Consent, privacy, and data minimization

- Collect only data needed to answer the approved research question.
- Separate product telemetry from research data.
- Do not assume app usage implies research consent.
- Do not upload books, private notes, queries, transcripts, or participant data to a model provider without authorization, clear disclosure, and an appropriate lawful basis.
- Keep identity keys separate from research records; restrict access and log access where feasible.
- Define retention and secure deletion before collection.
- Share only data that are consented, legally shareable, and sufficiently de-identified. Assess re-identification risk rather than assuming removing names is enough.

## 4. Corpus and intellectual property governance

For every source, record a rights basis: public domain, open license, explicit permission, user-owned/authorized use, or another documented basis reviewed for the intended processing and distribution. A user's ability to open a file does not establish permission to redistribute it or its extracted text.

Maintain a corpus manifest with source identifier, bibliographic metadata, checksum, acquisition date, rights basis, license/permission evidence location, permitted operations, and redistribution restrictions. Do not commit full copyrighted books, restricted datasets, or extracted passages unless redistribution is authorized.

## 5. AI and model governance

For each evaluated run, record provider, exact model identifier/version where available, API/runtime version, system and task prompt versions, decoding settings, retrieval configuration, source set, timestamp, and whether network inference occurred.

- Never describe a role prompt or indexed document collection as model training.
- Record model updates, provider outages, refusals, and manual interventions.
- Treat model outputs as unverified until checked against source evidence.
- Identify fabricated, incomplete, stale, contradictory, and unsupported citations.
- Define abstention and escalation behaviour for insufficient or conflicting evidence.
- Review domain-specific risks before enabling a domain pack.

## 6. Authorship, conflicts, and publication

Follow the target venue's authorship criteria. Credit substantial contributions to design, implementation, data curation, analysis, and writing; acknowledge other contributions transparently. Disclose funding, commercial interests, affiliations, and relevant use of AI writing or analysis tools according to venue policy.

Do not fabricate references, data, sample sizes, approvals, preregistration, or results. Preserve analysis code, protocol versions, exclusions, deviations, null results, and negative findings. Do not selectively report only favourable subjects, queries, or model runs.

## 7. Preregistration and protocol deviations

For confirmatory human-participant or benchmark studies, register hypotheses, outcomes, inclusion criteria, sample-size rationale, comparator, and analysis plan before examining outcome data where feasible. If preregistration is not appropriate, publish a dated protocol and explain why. Record every deviation with date, reason, and impact.

## 8. Release gate for research claims

A research claim may be made only when:
- The evaluated build and configuration are immutable and identified.
- Dataset provenance and rights are documented.
- The protocol and measures are defined.
- Baselines are fair and reproducible.
- Annotators/experts and adjudication are described.
- Missingness, exclusions, failures, and uncertainty are reported.
- Analysis is reproducible and limitations are explicit.
- Ethics and consent requirements are met where applicable.

See [EVALUATION_PROTOCOL.md](EVALUATION_PROTOCOL.md), [REPRODUCIBILITY.md](REPRODUCIBILITY.md), and [STUDY_PROTOCOL_TEMPLATE.md](STUDY_PROTOCOL_TEMPLATE.md).

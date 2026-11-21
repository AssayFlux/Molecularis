# Molecularis — Commercialisation Plan

**Status:** Initial commercial strategy; discovery and validation required before pricing or launch commitments  
**Planning date:** 2026-11-21  
**Product authority:** `docs/MASTER_PLAN.md`  
**Intended use:** Scientific research and education; not clinical decision support

## Executive direction

Build Molecularis as one integrated, local-first scientific research product with optional paid services around it. Commercialisation must follow demonstrated customer value and scientific evidence—not the number of modules, registry entries or planned features.

The first commercial objective is not to launch every service. It is to identify one narrow, frequent and valuable research workflow, deliver it as a dependable desktop product, validate its outputs against appropriate references, and secure a small group of active design partners.

The existing repository is a foundation, not a commercially validated product. The current master plan records 68 tool declarations marked implemented with source paths present, but their evidence level is `none`. No scientific capability should be advertised as independently validated or production-ready until the corresponding evidence is recorded.

## Commercial principles

1. **Evidence before claims:** every marketed scientific capability must have defined supported inputs, method, units, limitations, tests and appropriate reference evidence.
2. **Sell outcomes, not module counts:** customers pay to complete trusted workflows, save time, collaborate or run work securely.
3. **Local-first differentiation:** core project creation, data handling and supported local workflows should not require a hosted account or continuous internet connection.
4. **Open-core only if sustainable:** decide which components remain community-accessible and which paid features justify a licence; do not artificially cripple scientific correctness.
5. **Transparent execution location:** clearly distinguish local, institutional, paired-node and hosted compute, including where data travels.
6. **Research-use boundary:** no diagnosis, treatment, dosing or patient-specific clinical decision support.
7. **Platform discipline:** desktop Linux, Windows and macOS first; mobile follows the approved five-platform architecture and product gates.
8. **No premature promises:** prices, launch dates, platform support and performance claims remain hypotheses until tested.

## 1. Define the first sellable product

### Initial product hypothesis: Molecularis Pro

A paid, installed desktop edition for individual computational researchers who need a coherent workspace for supported molecular and biological research workflows.

**Proposed value proposition:** organise research projects, run supported analyses, inspect outputs and preserve reproducibility in one offline-capable application.

**Likely first customer profiles**
- Computational biology or chemistry postgraduate researchers.
- Independent computational researchers and consultants.
- Small academic research groups that lack dedicated software engineering support.

**Product requirements for a paid pilot**
- Installable and reliably updateable on the explicitly supported desktop operating systems.
- A portable, documented project format with backup, export and recovery.
- At least one complete end-to-end flagship workflow with clear input/output contracts.
- Reproducible run records: parameters, software and data versions, environment, timestamps and output checksums.
- Clear dependency detection, error messages and resource requirements.
- Scientific tests and reference comparisons appropriate to the selected workflow.
- Documentation, example data, known limitations and a support channel.
- Licence, privacy, security and third-party dependency review.

**Selection rule:** do not choose the flagship workflow by enthusiasm or source-file count. Score candidate workflows on customer pain, frequency, willingness to pay, implementation completeness, validation feasibility, differentiation, operating cost and support burden. Select one only after researcher interviews and a repository evidence review.

## 2. Service catalogue and packaging hypotheses

These are proposed commercial packages, not claims that the services are already implemented.

| Offer | Intended buyer | Potential paid value | Release condition |
|---|---|---|---|
| Molecularis Community | Students, educators, individual researchers | Free core application, open project format, selected workflows and community documentation | Stable, supportable community release |
| Molecularis Pro | Individual researchers and consultants | Advanced validated workflows, productivity features, local project tools, priority support and update channel | Paid-pilot workflow and desktop release gates pass |
| Molecularis Lab | Academic and industrial research groups | Team deployment, shared project conventions, administration, collaboration and support | Multi-user permissions, data integrity, deployment and support verified |
| Molecularis Compute | Compute-intensive research teams | Optional paired node, managed execution, GPU or HPC integration and usage reporting | Secure job supervision, resource accounting, isolation and cost controls verified |
| Molecularis Research Services | Labs, universities and research organisations | Workflow configuration, data processing, pipeline integration, training and scoped technical assistance | Written service scope, qualified delivery capacity and reproducible deliverables |
| Molecularis Enterprise | Institutions and companies | On-premises deployment, identity/integration options, governance, service agreements and dedicated support | Security, operations, legal, support and institutional acceptance gates pass |

Do not bundle hosted compute into every licence. Keep local software economics separate from infrastructure usage and make compute costs visible.

## 3. Customers, alternatives and positioning

### Initial segment

Start with computational researchers and small academic laboratories. They are accessible for discovery, can evaluate scientific workflows directly and may provide detailed feedback. Treat universities, biotech/pharma teams and CROs as subsequent segments after reliability and support maturity improve.

### Customer problems to test

- Scientific tools are fragmented across command-line programs, scripts and desktop applications.
- Repeating analyses and reconstructing parameters is error-prone.
- Installing and maintaining dependencies consumes researcher time.
- Projects, results and provenance are spread across files and applications.
- Small teams need local/offline workflows or controlled deployment.

These are hypotheses, not established market findings. Validate them through interviews and observed workflow sessions.

### Positioning

Position Molecularis as an integrated, reproducible scientific research workspace—not as a replacement for every specialist package. Explain exactly which workflows it supports, which engines it wraps, what is validated and what remains experimental. Interoperate with established scientific tools where that produces better outcomes than reimplementing them.

### Discovery evidence to collect

- Interview notes and consented workflow observations.
- Current tools and workarounds used for the target workflow.
- Time, error rate and setup burden in the current process.
- Required formats, reference standards, operating systems and data controls.
- Buying authority, procurement route, budget range and support expectations.
- Evidence of willingness to pilot or pay, not just positive feedback.

## 4. Pricing, licensing and revenue model

### Pricing approach

Do not publish a price list before customer discovery, cost modelling and competitor/alternative research. Test price sensitivity with real buyer conversations and paid pilot offers.

Use a simple structure:
- **Community:** free entry point with transparent scope.
- **Pro:** individual annual or monthly licence; consider a perpetual option only if update/support economics are sustainable.
- **Lab:** named-seat or team/site licence, with deployment and support boundaries explicit.
- **Compute:** separately metered or prepaid usage, with quotas, estimates, cancellation and spending controls.
- **Research Services:** fixed-scope project fees or day rates, with deliverables and exclusions agreed in writing.
- **Enterprise:** negotiated institutional licence and support agreement.

### Pricing inputs

Calculate fully loaded costs for engineering, scientific validation, release engineering, support, infrastructure, payment processing, taxes, legal/licensing review and customer acquisition. Define gross-margin targets only after realistic costs are known.

### Licensing decisions

Before launch, obtain qualified legal review of:
- Repository licence and compatibility with commercial distribution.
- Third-party libraries, engines, models, datasets and redistribution restrictions.
- Trademark and brand ownership.
- End-user licence, privacy notice, terms, acceptable use and support commitments.
- Institutional procurement, data processing and export-control obligations where applicable.

Never imply that an upstream dependency, model or dataset can be commercially redistributed until its exact licence and terms have been checked.

## 5. Scientific, technical and operational readiness

A feature can be sold only within its documented evidence and support boundary.

### Minimum capability evidence record

For every marketed capability, record:
- Stable capability ID and owner.
- Supported input formats, parameter ranges, units and output schema.
- Method and engine identity, exact versions and configuration.
- Required and optional dependencies, operating systems and resource profile.
- Unit, integration and end-to-end test references.
- Independent reference datasets or comparison method, acceptance criteria and results.
- Known limitations, failure modes and uncertainty.
- Provenance fields and reproducibility result.
- Security review, licence review and release decision.

### Readiness gates

| Gate | Required evidence |
|---|---|
| Functional | Complete documented workflow; supported inputs/outputs; failure handling |
| Scientific | Domain-appropriate reference comparisons, reviewed methods and limitations |
| Reproducibility | Repeatability or justified tolerance; provenance and version capture |
| Platform | Install, update, uninstall, filesystem, accessibility and lifecycle checks on claimed OS versions |
| Security and privacy | Threat review, dependency review, least privilege, data-flow disclosure and vulnerability handling |
| Operational | Support process, backups/recovery, release signing, rollback and incident response |
| Commercial | Customer value demonstrated, costs understood, licence rights cleared and offer terms approved |

Passing a smoke test alone is not independent scientific validation. A viewer rendering a structure is not proof of structural quality or biological significance.

## 6. Product milestones and release sequence

These are evidence-gated milestones, not calendar commitments.

### M0 — Commercial discovery
- Interview an initial cohort of target researchers.
- Observe real workflows and identify repeated pain points.
- Score candidate flagship workflows.
- Identify buying roles, procurement constraints and pilot interest.

**Exit:** documented customer problem, selected beachhead segment, ranked workflow candidates and evidence supporting one flagship choice.

### M1 — Flagship workflow proof
- Audit the selected workflow end to end in the current repository.
- Close missing contracts, dependencies, tests and reference comparisons.
- Demonstrate a reproducible workflow with representative user data.
- Record limitations and benchmark against the current user process.

**Exit:** reviewed scientific evidence dossier and a working demonstrator accepted by design partners.

### M2 — Desktop paid-pilot foundation
- Complete the approved desktop framework and packaging decisions.
- Deliver project storage, provenance, import/export, recovery and updates.
- Add onboarding, documentation, telemetry only where explicitly consented, and support workflow.
- Complete legal, licence, privacy and security checks.

**Exit:** installable pilot build with defined support matrix and no unresolved release-blocking risks.

### M3 — Closed paid pilot
- Recruit a small number of design-partner labs or individual researchers.
- Use written pilot scope, pricing, data handling and feedback terms.
- Track activation, workflow completion, failures, support time and repeat usage.
- Fix blockers before widening access.

**Exit:** users complete the target workflow repeatedly; at least some convert to paid use or provide credible procurement intent.

### M4 — Public Pro release
- Publish supported OS versions, capability evidence, limitations, pricing and release notes.
- Provide upgrade, support, security-reporting and refund/cancellation processes.
- Maintain a transparent status and compatibility matrix.

**Exit:** sustainable release and support operations with monitored quality metrics.

### M5 — Lab and Compute expansion
- Add team administration and deployment only after permissions and collaboration are verified.
- Add paired-node/HPC/hosted compute only after isolation, authentication, cost controls and data-flow controls pass.
- Keep mobile development aligned with the master plan and shared contracts.

**Exit:** separate readiness and customer evidence for each new offer.

## 7. Go-to-market and early customer acquisition

### Before launch
- Publish a clear product page with a truthful status label.
- Create a short demonstration of the flagship workflow using redistributable sample data.
- Publish methods, validation evidence, limitations and reproducibility instructions.
- Prepare installation guides, FAQ, support policy and issue-reporting process.
- Recruit design partners through research communities, university labs, scientific collaborators and relevant conferences.

### Launch sequence
1. Private technical demonstrator.
2. Researcher usability sessions.
3. Invitation-only design-partner pilot.
4. Paid pilot with explicit scope and support.
5. Public Community release and documented Pro offer.
6. Lab and Enterprise outreach after operational readiness.

Do not buy broad advertising before retention, product value and support capacity are demonstrated.

## 8. Revenue, growth and decision metrics

Track metrics that show customer value and sustainable operations.

| Area | Metric |
|---|---|
| Discovery | Qualified interviews, workflow observations, design-partner commitments |
| Activation | Install success, time to first successful project and first workflow |
| Product value | Workflow completion rate, time saved against baseline, repeat use |
| Scientific quality | Reference-test pass rate, reproducibility, severity and age of known defects |
| Reliability | Crash rate, failed jobs, recovery success, update success |
| Customer health | Active users, retention, support response and satisfaction |
| Commercial | Pilot-to-paid conversion, recurring revenue, renewal, average contract value |
| Economics | Gross margin by offer, support hours per customer, compute cost per job, acquisition cost |
| Governance | Licence exceptions, security incidents, unresolved critical findings |

Set numerical targets only after baseline measurement and customer discovery. Do not fabricate revenue forecasts or adoption claims.

## Immediate 30-day work queue

This is a proposed first sprint sequence; dates and targets should be confirmed against actual capacity.

1. Create a researcher interview guide and recruit target users.
2. Inventory candidate workflows against repository implementation, dependencies, tests and scientific evidence.
3. Score and select one flagship workflow using customer and engineering evidence.
4. Produce a workflow-specific scientific validation plan and acceptance criteria.
5. Draft Community/Pro/Lab packaging boundaries without publishing prices.
6. Map dependency licences, data/model terms and commercial redistribution rights for the selected workflow.
7. Prepare a demonstrator and pilot brief for design partners.
8. Review findings and approve or revise the paid-pilot scope.

## Decisions intentionally left open

- First flagship scientific workflow and initial customer segment.
- Final Community versus paid feature boundaries.
- Price points, billing cadence and perpetual licensing.
- Whether compute is self-hosted, partner-hosted or customer-managed.
- Support hours, service levels and geographic availability.
- Launch dates and revenue targets.
- Commercial distribution implications of the current repository licence and dependencies.

These decisions require evidence, legal review or explicit owner approval. This plan does not override the technical master plan; it defines the commercial workstream and its release gates.

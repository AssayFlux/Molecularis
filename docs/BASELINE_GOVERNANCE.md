# Baseline and branch governance

**Policy version:** 2.0  
**Applies to:** all Molecularis source, build, scientific data, documentation and release artifacts.

## 1. Release states

A version moves through declared → candidate → built → accepted → frozen baseline. A version string, partial CI pass, cancelled workflow, old artifact, or successful compilation step is not a release.

## 2. v0.1.0 baseline immutability

Until the exact v0.1.0 commit has a successful clean build, verified APK, required automated checks and owner acceptance, it remains a candidate and may receive narrowly scoped release-blocker fixes.

After successful baseline acceptance and freeze:
- main is the immutable v0.1.0 baseline. Do not commit, merge, rebase, amend, squash, regenerate or otherwise change its tree.
- Preserve the exact baseline commit and immutable v0.1.0 tag. Never force-move, delete/recreate or retarget the tag.
- Do not update baseline dependencies, lockfiles, generated files, UI, methods, documentation or build scripts in place.
- All next-version engineering happens only on the single branch named v0.1.1.
- Do not create feature, develop, release, hotfix or other branches for next-version work. Use commits on v0.1.1. Do not merge next-version work into frozen main.
- The next release is v0.1.1. It combines integration/usability hardening and the planned scientific rulebook foundation. Critical fixes to the frozen v0.1.0 baseline are delivered as a new version, not by changing its commit or tag.
- Archive APK/AAB, SHA-256, build logs, SBOM, toolchain record, test reports and release notes.

The GitHub administrator must enable branch protection/rulesets and tag protection. Do not claim these controls are active until verified in GitHub settings.

## 3. Branch model — single forward branch

- main: v0.1.0 baseline source. It is still a candidate until the v0.1.0 exact-commit build and acceptance gates pass; after freeze it is read-only.
- v0.1.1: the only permitted forward-development branch. It is created from the accepted v0.1.0 baseline commit. All next-version commits go here.
- Existing legacy branches release/0.1.0 and develop/v0.1.2 are obsolete and must receive no new work. The GitHub connection used for this change does not expose branch deletion; repository administrator should delete those obsolete branches. Do not create additional branches.
- Before every meaningful integration or release candidate, fetch and compare v0.1.1 with main; verify merge base, changed files, version metadata, Android/Python contracts, capability registry, generated assets and tests. While main is not frozen, incorporate required baseline fixes into v0.1.1 without rewriting main. Once main is frozen, never rewrite it or merge v0.1.1 into it.
- A branch name is not proof of protection. Verify GitHub rules before relying on required reviews or force-push restrictions.

## 4. Change control

Every change must identify target release and requirement; affected app workflows, APIs, dispatchers, registry, schemas, data packs, docs and generated assets; tests for success and failure paths; compatibility/migration impact; dependency source/version/checksum/licence; scientific provenance, units, parameters, seeds and limitations; evidence-backed user claims; changelog/manifest updates; and exact-commit CI results.

No force push to shared branches. No secrets, patient-identifiable data, private research data, signing keys or credentials in Git.

## 5. Research archive and build independence

potential research project.md is a dormant archive only. Its research plans, rulebooks and future protocols must not activate app capabilities, datasets, training, CI jobs or runtime workflows until the owner explicitly authorizes a defined scope.

Ordinary software engineering and Android packaging must not be blocked solely by future research protocol, ethics-committee, dataset-intake or scientific-validation work that is not part of the shipped v0.1.0 scope. Keep the archive non-executable and do not add its future research tasks as release prerequisites.

This separation does not waive engineering safeguards: protect data actually processed; enforce consent/access controls where applicable; keep sensitive/patient data out of GitHub, CI and public artifacts; manage secrets; comply with dependency/data licences; make truthful capability claims; and keep clinical decision functions disabled unless separately authorized.

## 6. Scientific integrity

Separate implementation, Android integration, independent validation, device acceptance and clinical approval. A registry entry, test, smoke test, database record or model output does not alone establish scientific validation. Generated/predicted results must identify method class, inputs, parameters, version, provenance, uncertainty and limitations. No patient-specific clinical interpretation, diagnosis or treatment/dosing recommendation is enabled by the dormant archive.

## 7. v0.1.0 freeze checklist

- [ ] Exact release candidate commit identified and reviewed.
- [ ] Exact-commit CI green, including APK build, JVM tests, Python suite and native/package checks.
- [ ] APK installed and exercised on a named ARM64 device and supported emulator; workflow, recovery, import/export and upgrade evidence archived.
- [ ] UI, accessibility, security, privacy, licensing, notices and dependency/SBOM review accepted.
- [ ] Shipped capability claims match implementation and evidence.
- [ ] Owner approves release notes, artifact hashes and distribution.
- [ ] Annotated v0.1.0 tag created once and protected.
- [ ] Baseline manifest records exact tag, commit, APK SHA-256, CI run and evidence links.
- [ ] GitHub-side branch/tag rules verified and documented.
- [ ] v0.1.1 created from the accepted baseline commit as the sole forward branch.

Until all boxes are checked, status remains CANDIDATE — NOT FROZEN.

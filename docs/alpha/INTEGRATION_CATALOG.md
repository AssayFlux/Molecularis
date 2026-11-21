# Alpha Scientific Integration Catalog

## Source provenance
The supplied Molecularis.zip contains text snapshots, not Git working copies. Exact upstream commit IDs, tags and current upstream status are not guaranteed. Before code reuse, fetch exact upstream source/version and record commit SHA, license text, dependencies, model/data terms, security posture and review date.

| Project | Intended role | Alpha posture | Main gates |
|---|---|---|---|
| Genome-Wide Workbench (ebbrg/genome-wide-workbench) | Genomic discovery, homology, MSA, phylogeny, visualization and primer workflows | Selective workflow/algorithm adapters | External binaries, algorithm versions, databases, license and benchmark |
| Biotite (biotite-dev/biotite) | Python sequence/structure IO, analysis and visualization | Python adapter/library evaluation | Exact license/version, dependencies, format edge cases |
| ESM (facebookresearch/esm) | Protein embeddings, contact prediction, variant scoring, inverse folding and ESMFold | Isolated optional model worker | Code vs checkpoint/data terms, accelerator profile, model card, benchmark |
| AlphaFold (google-deepmind/alphafold) | Protein structure prediction | Optional isolated HPC/cloud/local-GPU profile | Databases, weights, compute, data terms, storage and reproducibility |
| Mol* (molstar/molstar) | Interactive macromolecular structure viewer | Preferred web viewer candidate | Bundle size, assets, license notices, offline and browser performance |
| MolProbity (rlabduke/molprobity) | Structure validation | Isolated audited method/worker adapters | Snapshot describes legacy PHP 5.6; no public deployment without security redesign |
| OpenMM (openmm/openmm) | Molecular dynamics | Native worker profile | System preparation, force fields, units, GPU support and validation |
| ChemGraph (argonne-lcf/chemgraph) | Agent-assisted computational chemistry/materials workflows | Optional isolated workflow service | Agent permissions, generated input review, determinism, convergence, units |
| Open Chemistry (openchemistry/openchemistry) | Molecular editing/interoperability ecosystem | Component-level reuse only | Dependency graph and component-specific license |
| NUAD (uc-davis-molecular-computing/nuad) | DNA/RNA nanostructure design | Specialized workflow | NUPACK is separate software with separate license/install requirements |
| Galaxy (galaxyproject/galaxy) | Workflow execution and tool ecosystem | API/federation, not monolithic merge | Server operations, plugin/tool/container licenses and security |
| SciREPL (s243a/scirepl) | Browser notebook/PWA, kernels and virtual filesystem patterns | UX/architecture reference; safe kernels only | Browser sandbox limits, kernel resource use and remote execution isolation |

## Shared engine contract
Every adapter declares engine ID/version, contract versions, runtime/OS/architecture/accelerator requirements, inputs/outputs, units, parameter schema, license/notices, resource estimates, timeout/cancellation, network/filesystem permissions, provenance, tests, validation level and failure diagnostics.

## Integration stages
1. Source and license/security review.
2. Isolated proof of concept without production data.
3. Versioned adapter contract and schema.
4. Deterministic unit/contract tests.
5. Reference benchmark and resource profile.
6. Platform deployment and security review.
7. Independent scientific review and owner acceptance.

Copying source is not integration. Code, model weights, datasets, containers and plugins each require separate rights review.
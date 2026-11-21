# Scientific engine decisions and adoption gates

**Decision status:** Source-level architecture choices are recorded; no third-party scientific engine is approved for Android product bundling yet.

## Python runtime and numerical stack (R1/R3)
- **Chaquopy 17.2.0 / Python 3.11:** retained as the isolated Android feasibility prototype. The local build script pins the Chaquopy source commit and Gradle distribution checksum. A successful local APK/AAB build and actual Android Python runtime probe are still required.
- **Biopython 1.88:** retained in the prototype for sequence parsing/alignment and Bio.PDB exploration. The custom wheel was built in historical CI, but file-level notices, runtime imports, current 16 KB native compatibility and redistribution review remain open.
- **NumPy 1.26.2:** retained only for the prototype. Its Chaquopy arm64 wheel is old; no independent wheel SHA-256 pin or 16 KB runtime proof is yet recorded.
- **SciPy:** not approved for Android. No compatible package has been demonstrated in the current Chaquopy Python 3.11 index. Host-only SciPy is the independent numerical reference for the kinetic validation harness, not an Android dependency.
- **Enzyme-kinetics estimators:** dependency-free log-grid least squares remains exploratory. The optional host validation harness compares it with SciPy curve_fit; it has not been run.

## Sequence alignment and genomics (R4)
- **Biopython PairwiseAligner:** prototype/reference candidate only; not a high-throughput mapper.
- **Parasail 2.6.2:** evaluation candidate only. No Android cross-build, ABI/16 KB check, exact binary notice bundle or performance comparison has been accepted.
- **BAM:** bounded pure-Python core-field reader is available for gzip/BGZF-compatible streams; it skips auxiliary tags and is not an indexed engine.
- **BAM/CRAM:** optional host pysam/HTSlib adapter supports streaming and indexed reads; CRAM requires a local reference FASTA. No HTSlib Android library is bundled or approved.

## Structure (R5)
- Current PDB/mmCIF atom-site parser and geometric routines are dependency-free exploratory code.
- SASA and interaction outputs are explicitly approximate/geometric candidates.
- Mol* remains an offline-viewer candidate only; no packaged viewer or offline WebView/WebGL proof exists.

## Chemistry (R6)
- The built-in V2000/V3000 parser and custom graph fingerprints are exploratory, not a production cheminformatics engine.
- An optional host RDKit adapter now performs sanitization, canonical isomeric SMILES, standard descriptors and Morgan fingerprints when RDKit is installed.
- RDKit is not bundled in Android. Exact release pin, full dependency graph, file-level/binary license notices, Android arm64/16 KB feasibility and binary footprint must be reviewed before adoption.

## Phylogenetics (R7)
- Newick parsing/serialization, UPGMA and neighbour joining are available.
- Jukes–Cantor corrected nucleotide distances feed neighbour joining. This is a simple model-corrected distance workflow, not maximum-likelihood/Bayesian inference, model selection, rate heterogeneity or bootstrap.

## Omics (R8)
- Welch/BH remains for pre-normalized values.
- The new NB2 GLM is exploratory: raw integer counts, median-of-ratios/library-size factors, unmoderated moment dispersion, numeric covariates and asymptotic Wald tests. It is not DESeq2/edgeR-equivalent; independent simulation/reference calibration is required.

## PGx data (R9)
- NCBI Gene gene_info is used only as a broad gene catalogue, not as allele-definition evidence.
- PGx definition ingestion requires source release, URL, SHA-256, license and genome build. No PharmVar/CPIC/PharmGKB dataset is bundled pending current source-specific licensing and redistribution review.
- No phasing, copy-number, diplotype, phenotype or clinical recommendation is inferred.

## License and security rule
No dependency is approved for redistribution solely because its upstream project is open source. Record exact source revision, full transitive dependency graph, file/binary license notices, attribution, patent terms, native ABI, checksums and update policy. The Apache-2.0 project license does not override upstream component licenses.

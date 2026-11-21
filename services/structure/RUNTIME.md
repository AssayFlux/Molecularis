# Structure Runtime

Status: Python reference runtime integrated with MSDE.

1. Construct a StructureDocument or import PDB/mmCIF text.
2. Ingest canonical JSON as immutable MSDE artifact with coordinate metadata and parent lineage.
3. Resolve one of six versioned capabilities.
4. Execute structure-core-v1 under the shared platform budget.
5. Verify media type, schema, artifact digest and metadata before computation.
6. Persist reports and execution evidence through the Rulebook executor.

Documents are limited to 100,000 atoms. Pairwise contacts/interactions are limited to 5,000 atoms; SASA to 2,000 atoms and 4,096 sphere samples. RMSD requires equal atom counts and caller-matched ordering. Invalid inputs and resource overages fail closed.

The v1 service is in-process Python and does not fetch network data, shell out or require external engines. C++ and Rust bindings are future work, not implemented claims.

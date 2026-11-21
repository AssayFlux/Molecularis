# Android capability integration matrix

**Reconciled against main:** `00265bb7c4ad7ced908f2a4113e7fb7344e43007` (2026-11-18)  
**Branch:** `main`  
**Purpose:** Separate Python source registration from an actual Android-executable workflow.  
**Evidence boundary:** A connected route means the Android UI invokes a bounded Chaquopy bridge. It does not mean the scientific method has been independently validated, clinically approved, or device-accepted.

## Summary

- Catalogue entries: **68**
- Catalogue entries connected to Android workflows: **36**
- Catalogue entries not yet connected to Android: **32**
- Additional Android service outside the JSON catalogue: `public.reference_databases` (NCBI/UniProt/RCSB retrieval).

The Android UI must never display catalogue `status: implemented` as proof of Android integration. The service page separately reports whether an Android workflow is connected.

## Connected Android workflows

**36 of 68 catalogue capabilities** have an Android UI route and bounded bridge according to the mapping below. This is integration status only, not independent scientific validation or device acceptance.

| Capability ID | Android integration |
|---|---|
| `public.reference_databases` | Public database retrieval card; NCBI Nucleotide/Protein, UniProtKB FASTA and RCSB mmCIF. This is an additional Android service, not one of the 68 catalogue entries. |

| `sequence.fasta` | local Android form + Python bridge |
| `sequence.explicit_genetic_code_translation` | local Android form + Python bridge |
| `sequence.genetic_code_candidate_inference` | local Android form + Python bridge |
| `genome.orf_candidate_scan` | local Android form + Python bridge |
| `genome.prokaryotic_orf_candidate_scan` | local Android form + Python bridge |
| `sequence.fastq` | local Android form + Python bridge |
| `sequence.global_alignment` | local Android form + Python bridge |
| `genomics.sam_vcf` | local Android form + Python bridge |
| `protein.descriptors` | local Android form + Python bridge |
| `kinetics.michaelis_menten` | local Android form + Python bridge |
| `chemistry.sdf_graph` | local Android form + Python bridge |
| `phylo.newick` | local Android form + Python bridge |
| `omics.normalisation` | local Android form + Python bridge |
| `microbiome.diversity` | local Android form + Python bridge |
| `molecular.primer_screen` | local Android form + Python bridge |
| `molecular.crispr_pam` | local Android form + Python bridge |
| `phylo.upgma` | local Android form + Python bridge |
| `omics.logistic_growth` | local Android form + Python bridge |
| `omics.cross_correlation` | local Android form + Python bridge |
| `kinetics.bootstrap_intervals` | local Android form + Python bridge |
| `structure.sasa` | local Android form + Python bridge |
| `phylo.jukes_cantor_nj` | local Android form + Python bridge |
| `structure.interaction_candidates` | local Android form + Python bridge |
| `phylo.nj_site_bootstrap` | local Android form + Python bridge |
| `structure.exact_sequence_mapping` | local Android form + Python bridge |
| `structure.geometry_screen_metrics` | local Android form + Python bridge |
| `structure.variant_coordinate_mapping` | local Android form + Python bridge |
| `structure.chain_interface_contacts` | local Android form + Python bridge |
| `structure.ligand_site_candidates` | local Android form + Python bridge |
| `structure.apo_pocket_candidates` | local Android form + Python bridge |
| `genome.contig_assembly_qc` | local Android form + Python bridge |
| `protein.fixed_width_motif_scan` | local Android form + Python bridge |
| `protein.design_brief_validation` | local Android form + Python bridge |
| `structure.alignment_coordinate_mapping` | local Android form + Python bridge |
| `genome.gff3_annotation_import` | local Android form + Python bridge |
| `genome.gff3_transcript_cds_reconstruction` | local Android form + Python bridge |

## Complete catalogue mapping



| Capability ID | Python source | Android integration |
|---|---|---|
| `sequence.fasta` | `python/molecularis/sequence.py` | Connected — local Android form + Python bridge |
| `sequence.exact_reference_search` | `python/molecularis/sequence_reference.py` | Not connected — Python source only |
| `sequence.local_reference_pack_loader` | `python/molecularis/sequence_pack.py` | Not connected — Python source only |
| `sequence.local_fasta_exact_search` | `python/molecularis/sequence_pack.py` | Not connected — Python source only |
| `sequence.explicit_genetic_code_translation` | `python/molecularis/genetic_code.py` | Connected — local Android form + Python bridge |
| `sequence.genetic_code_candidate_inference` | `python/molecularis/genetic_code_inference.py` | Connected — local Android form + Python bridge |
| `genome.orf_candidate_scan` | `python/molecularis/orf.py` | Connected — local Android form + Python bridge |
| `genome.prokaryotic_orf_candidate_scan` | `python/molecularis/genome_orf.py` | Connected — local Android form + Python bridge |
| `sequence.local_blastp` | `python/molecularis/blastp.py` | Not connected — Python source only |
| `sequence.local_hmmpress` | `python/molecularis/hmmer_runner.py` | Not connected — Python source only |
| `sequence.local_hmmscan` | `python/molecularis/hmmer_runner.py` | Not connected — Python source only |
| `protein.hmmscan_domain_evidence` | `python/molecularis/hmmer.py` | Not connected — Python source only |
| `sequence.fastq` | `python/molecularis/sequence.py` | Connected — local Android form + Python bridge |
| `sequence.global_alignment` | `python/molecularis/sequence.py` | Connected — local Android form + Python bridge |
| `genomics.sam_vcf` | `python/molecularis/genomics.py` | Connected — local Android form + Python bridge |
| `variant.reference_checked_normalization` | `python/molecularis/variant_reference.py` | Not connected — Python source only |
| `protein.descriptors` | `python/molecularis/protein.py` | Connected — local Android form + Python bridge |
| `kinetics.michaelis_menten` | `python/molecularis/kinetics.py` | Connected — local Android form + Python bridge |
| `structure.pdb_geometry` | `python/molecularis/structure.py` | Not connected — Python source only |
| `chemistry.sdf_graph` | `python/molecularis/chemistry.py` | Connected — local Android form + Python bridge |
| `phylo.newick` | `python/molecularis/phylo.py` | Connected — local Android form + Python bridge |
| `omics.normalisation` | `python/molecularis/omics.py` | Connected — local Android form + Python bridge |
| `microbiome.diversity` | `python/molecularis/omics.py` | Connected — local Android form + Python bridge |
| `genes.ncbi_catalogue` | `python/molecularis/catalog.py` | Not connected — Python source only |
| `molecular.primer_screen` | `python/molecularis/molecular.py` | Connected — local Android form + Python bridge |
| `molecular.crispr_pam` | `python/molecularis/molecular.py` | Connected — local Android form + Python bridge |
| `phylo.upgma` | `python/molecularis/phylo.py` | Connected — local Android form + Python bridge |
| `omics.logistic_growth` | `python/molecularis/omics.py` | Connected — local Android form + Python bridge |
| `omics.cross_correlation` | `python/molecularis/omics.py` | Connected — local Android form + Python bridge |
| `genomics.variant_normalization` | `python/molecularis/genomics.py` | Not connected — Python source only |
| `kinetics.bootstrap_intervals` | `python/molecularis/kinetics.py` | Connected — local Android form + Python bridge |
| `structure.sasa` | `python/molecularis/structure.py` | Connected — local Android form + Python bridge |
| `phylo.newick_export` | `python/molecularis/phylo.py` | Not connected — Python source only |
| `omics.nb2_glm` | `python/molecularis/omics.py` | Not connected — Python source only |
| `genomics.bam_core` | `python/molecularis/genomics.py` | Not connected — Python source only |
| `pgx.star_allele_definitions` | `python/molecularis/pgx.py` | Not connected — Python source only |
| `phylo.jukes_cantor_nj` | `python/molecularis/phylo.py` | Connected — local Android form + Python bridge |
| `structure.interaction_candidates` | `python/molecularis/structure.py` | Connected — local Android form + Python bridge |
| `chemistry.rdkit_adapter` | `python/molecularis/chemistry_rdkit.py` | Not connected — Python source only |
| `genomics.htslib_bam_cram` | `python/molecularis/genomics_htslib.py` | Not connected — Python source only |
| `pgx.pharmvar_tsv` | `python/molecularis/pharmvar.py` | Not connected — Python source only |
| `phylo.nj_site_bootstrap` | `python/molecularis/phylo.py` | Connected — local Android form + Python bridge |
| `structure.viewer_payload` | `python/molecularis/structure_view.py` | Not connected — Python source only |
| `structure.session_export` | `python/molecularis/structure_view.py` | Not connected — Python source only |
| `structure.exact_sequence_mapping` | `python/molecularis/sequence_structure.py` | Connected — local Android form + Python bridge |
| `structure.geometry_screen_metrics` | `python/molecularis/structure_quality.py` | Connected — local Android form + Python bridge |
| `structure.variant_coordinate_mapping` | `python/molecularis/sequence_structure.py` | Connected — local Android form + Python bridge |
| `structure.chain_interface_contacts` | `python/molecularis/sequence_structure.py` | Connected — local Android form + Python bridge |
| `structure.ligand_site_candidates` | `python/molecularis/structure_pockets.py` | Connected — local Android form + Python bridge |
| `structure.apo_pocket_candidates` | `python/molecularis/apo_pockets.py` | Connected — local Android form + Python bridge |
| `genes.catalogue_coverage_report` | `python/molecularis/catalog.py` | Not connected — Python source only |
| `structure.prediction_envelope_validation` | `python/molecularis/structure_prediction.py` | Not connected — Python source only |
| `structure.experimental_ca_comparison` | `python/molecularis/structure_prediction.py` | Not connected — Python source only |
| `genome.contig_assembly_qc` | `python/molecularis/genome_qc.py` | Connected — local Android form + Python bridge |
| `protein.fixed_width_motif_scan` | `python/molecularis/protein_motifs.py` | Connected — local Android form + Python bridge |
| `protein.design_brief_validation` | `python/molecularis/protein_design.py` | Connected — local Android form + Python bridge |
| `structure.alignment_coordinate_mapping` | `python/molecularis/structure_alignment.py` | Connected — local Android form + Python bridge |
| `sequence.local_alignment_reference_search` | `python/molecularis/sequence_reference.py` | Not connected — Python source only |
| `genome.gff3_annotation_import` | `python/molecularis/gff3.py` | Connected — local Android form + Python bridge |
| `sequence.local_fasta_alignment_search` | `python/molecularis/sequence_pack.py` | Not connected — Python source only |
| `genome.gff3_transcript_cds_reconstruction` | `python/molecularis/gff3_transcripts.py` | Connected — local Android form + Python bridge |
| `protein.hmmer_domain_candidate_ranking` | `python/molecularis/hmmer_rank.py` | Not connected — Python source only |
| `protein.hmmscan_domtblout_evidence` | `python/molecularis/hmmer.py` | Not connected — Python source only |
| `structure.pinned_local_prediction_process` | `python/molecularis/s4_process.py` | Not connected — Python source only |
| `genome.augustus_local_gene_candidates` | `python/molecularis/augustus.py` | Not connected — Python source only |
| `genome.prodigal_local_gene_candidates` | `python/molecularis/prodigal.py` | Not connected — Python source only |
| `genome.pinned_local_gff3_annotator` | `python/molecularis/genome_annotation.py` | Not connected — Python source only |
| `structure.local_prediction_engine_adapter` | `python/molecularis/s4_engine.py` | Not connected — Python source only |

## Remaining engineering work

1. Add typed Android forms and bridge methods for the remaining catalogue entries, grouping related tools into coherent service workspaces without hiding individual capability IDs.
2. Integrate optional dependencies (RDKit, HTSlib/pysam, HMMER, BLAST, Vina, OpenMM and structure-prediction adapters) only where Android-compatible packaging, ABI, licences, model provenance, storage and runtime limits are demonstrated. Host-only availability is not Android availability.
3. Add workflow-level cancellation, progress, lifecycle-safe execution, result persistence, provenance export and recovery for long-running workflows.
4. Add Android tests for every exposed capability: valid inputs, malformed inputs, upper bounds, cancellation, result schema and privacy boundaries.
5. Complete public-database retrieval lifecycle: retries/backoff, cancellation, cache quotas/eviction, provider terms/licence metadata, source release capture and background execution.
6. Decide and implement remote account authentication only after an identity provider/backend is selected. Current profile and biometric unlock remain device-local; no fake password reset or remote account ID.
7. Re-run exact-head CI after the final engineering changes. Physical-device, accessibility, scientific benchmark, independent review and clinical/ethics acceptance remain separate later gates.

## Change log

- `92824712238e7dd54ddcab5e5ab8e8552e1d0014`: added Android forms and Python bridge for protein descriptors, primer screening and SpCas9 NGG PAM scan.
- `520d3b5777294871645a88f1566341ac8b1d1747`: added Android forms and bounded bridge for ORF candidate scan, Michaelis–Menten rate calculation and Newick parsing.

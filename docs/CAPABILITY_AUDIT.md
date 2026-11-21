# Molecularis Capability Registry Audit

**Snapshot:** CORE commit `ea2eb62f5ea07a57172dd5d384ed728cfa51fe39`, 2026-11-21. The registry blob is identical on Alpha at audit time.  
**Scope:** all 130 registry entries, declared implementation paths, tracked source-file existence and related test-module mapping. This is not a runtime execution, full code review, scientific validation, device test, security assessment or release approval.

## Summary

| Category | Count | State |
|---|---:|---|
| Scientific/technical tools | 68 | 68 implemented declarations; 0 planned |
| UI screens | 26 | Planned |
| UI settings | 22 | Planned |
| Security features | 14 | Planned |
| **Total** | **130** | **68 implemented declarations; 62 planned; 0 validated** |

- All 68 implemented tool entries have a declared implementation path and all 68 paths exist in the tracked CORE tree.
- All 68 implemented entries have `evidence_level: none`. The registry therefore records no scientifically validated capability.
- The 62 planned entries are 26 UI screens, 22 settings and 14 security features. They have no implementation path in the registry. Related Android legacy behaviours may exist; the registry does not establish desktop/mobile parity or prove those behaviours absent.
- Top-level registry collections are `tools`, `ui_screens`, `ui_settings`, `security_features`, and `clinical_gate`. There are no structured engine, data-pack, domain, platform-binding, device-log or validation-record collections yet.
- Tool entries do not declare per-capability test lists. The table below links related module-level tests based on implementation module and test imports/intent. This is a traceability aid, not proof that each test asserts every listed capability.

## Every implemented tool entry

| Capability ID | Declared source (exists) | Related test modules (candidate mapping) | Evidence |
|---|---|---|---|
| `sequence.fasta` | `python/molecularis/sequence.py` | test_research_primitives.py, test_fasta_workflow.py, test_fastq_streaming.py, test_android_basic_capability_dispatch.py | none |
| `sequence.exact_reference_search` | `python/molecularis/sequence_reference.py` | test_sequence_reference.py | none |
| `sequence.local_reference_pack_loader` | `python/molecularis/sequence_pack.py` | test_sequence_pack.py | none |
| `sequence.local_fasta_exact_search` | `python/molecularis/sequence_pack.py` | test_sequence_pack.py | none |
| `sequence.explicit_genetic_code_translation` | `python/molecularis/genetic_code.py` | test_genetic_code.py | none |
| `sequence.genetic_code_candidate_inference` | `python/molecularis/genetic_code_inference.py` | test_genetic_code_inference.py | none |
| `genome.orf_candidate_scan` | `python/molecularis/orf.py` | test_orf.py | none |
| `genome.prokaryotic_orf_candidate_scan` | `python/molecularis/genome_orf.py` | test_genome_orf.py, test_android_basic_capability_dispatch.py | none |
| `sequence.local_blastp` | `python/molecularis/blastp.py` | test_blastp.py | none |
| `sequence.local_hmmpress` | `python/molecularis/hmmer_runner.py` | test_hmmer_runner.py | none |
| `sequence.local_hmmscan` | `python/molecularis/hmmer_runner.py` | test_hmmer_runner.py | none |
| `protein.hmmscan_domain_evidence` | `python/molecularis/hmmer.py` | test_hmmer.py, test_hmmer_rank.py | none |
| `sequence.fastq` | `python/molecularis/sequence.py` | test_research_primitives.py, test_fasta_workflow.py, test_fastq_streaming.py, test_android_basic_capability_dispatch.py | none |
| `sequence.global_alignment` | `python/molecularis/sequence.py` | test_research_primitives.py, test_fasta_workflow.py, test_fastq_streaming.py, test_android_basic_capability_dispatch.py | none |
| `genomics.sam_vcf` | `python/molecularis/genomics.py` | test_genomics.py, test_android_basic_capability_dispatch.py | none |
| `variant.reference_checked_normalization` | `python/molecularis/variant_reference.py` | test_variant_reference.py | none |
| `protein.descriptors` | `python/molecularis/protein.py` | test_research_primitives.py | none |
| `kinetics.michaelis_menten` | `python/molecularis/kinetics.py` | test_research_primitives.py, test_kinetic_transforms.py, test_android_basic_capability_dispatch.py | none |
| `structure.pdb_geometry` | `python/molecularis/structure.py` | test_structure.py, test_android_basic_capability_dispatch.py | none |
| `chemistry.sdf_graph` | `python/molecularis/chemistry.py` | test_chemistry.py | none |
| `phylo.newick` | `python/molecularis/phylo.py` | test_phylo.py, test_android_basic_capability_dispatch.py | none |
| `omics.normalisation` | `python/molecularis/omics.py` | test_omics.py, test_android_basic_capability_dispatch.py | none |
| `microbiome.diversity` | `python/molecularis/omics.py` | test_omics.py, test_android_basic_capability_dispatch.py | none |
| `genes.ncbi_catalogue` | `python/molecularis/catalog.py` | test_catalog.py, test_android_basic_capability_dispatch.py | none |
| `molecular.primer_screen` | `python/molecularis/molecular.py` | test_android_basic_capability_dispatch.py | none |
| `molecular.crispr_pam` | `python/molecularis/molecular.py` | test_android_basic_capability_dispatch.py | none |
| `phylo.upgma` | `python/molecularis/phylo.py` | test_phylo.py, test_android_basic_capability_dispatch.py | none |
| `omics.logistic_growth` | `python/molecularis/omics.py` | test_omics.py, test_android_basic_capability_dispatch.py | none |
| `omics.cross_correlation` | `python/molecularis/omics.py` | test_omics.py, test_android_basic_capability_dispatch.py | none |
| `genomics.variant_normalization` | `python/molecularis/genomics.py` | test_genomics.py, test_android_basic_capability_dispatch.py | none |
| `kinetics.bootstrap_intervals` | `python/molecularis/kinetics.py` | test_research_primitives.py, test_kinetic_transforms.py, test_android_basic_capability_dispatch.py | none |
| `structure.sasa` | `python/molecularis/structure.py` | test_structure.py, test_android_basic_capability_dispatch.py | none |
| `phylo.newick_export` | `python/molecularis/phylo.py` | test_phylo.py, test_android_basic_capability_dispatch.py | none |
| `omics.nb2_glm` | `python/molecularis/omics.py` | test_omics.py, test_android_basic_capability_dispatch.py | none |
| `genomics.bam_core` | `python/molecularis/genomics.py` | test_genomics.py, test_android_basic_capability_dispatch.py | none |
| `pgx.star_allele_definitions` | `python/molecularis/pgx.py` | test_pgx.py | none |
| `phylo.jukes_cantor_nj` | `python/molecularis/phylo.py` | test_phylo.py, test_android_basic_capability_dispatch.py | none |
| `structure.interaction_candidates` | `python/molecularis/structure.py` | test_structure.py, test_android_basic_capability_dispatch.py | none |
| `chemistry.rdkit_adapter` | `python/molecularis/chemistry_rdkit.py` | test_chemistry.py | none |
| `genomics.htslib_bam_cram` | `python/molecularis/genomics_htslib.py` | test_genomics.py | none |
| `pgx.pharmvar_tsv` | `python/molecularis/pharmvar.py` | test_pharmvar.py, test_catalog.py | none |
| `phylo.nj_site_bootstrap` | `python/molecularis/phylo.py` | test_phylo.py, test_android_basic_capability_dispatch.py | none |
| `structure.viewer_payload` | `python/molecularis/structure_view.py` | test_structure_view.py, test_structure_viewer_assets.py | none |
| `structure.session_export` | `python/molecularis/structure_view.py` | test_structure_view.py, test_structure_viewer_assets.py | none |
| `structure.exact_sequence_mapping` | `python/molecularis/sequence_structure.py` | test_sequence_structure.py | none |
| `structure.geometry_screen_metrics` | `python/molecularis/structure_quality.py` | test_structure_quality.py | none |
| `structure.variant_coordinate_mapping` | `python/molecularis/sequence_structure.py` | test_sequence_structure.py | none |
| `structure.chain_interface_contacts` | `python/molecularis/sequence_structure.py` | test_sequence_structure.py | none |
| `structure.ligand_site_candidates` | `python/molecularis/structure_pockets.py` | test_structure_pockets.py | none |
| `structure.apo_pocket_candidates` | `python/molecularis/apo_pockets.py` | test_structure_pockets.py | none |
| `genes.catalogue_coverage_report` | `python/molecularis/catalog.py` | test_catalog.py, test_android_basic_capability_dispatch.py | none |
| `structure.prediction_envelope_validation` | `python/molecularis/structure_prediction.py` | test_structure_prediction.py | none |
| `structure.experimental_ca_comparison` | `python/molecularis/structure_prediction.py` | test_structure_prediction.py | none |
| `genome.contig_assembly_qc` | `python/molecularis/genome_qc.py` | test_genome_qc.py | none |
| `protein.fixed_width_motif_scan` | `python/molecularis/protein_motifs.py` | test_protein_motifs.py | none |
| `protein.design_brief_validation` | `python/molecularis/protein_design.py` | test_protein_design.py | none |
| `structure.alignment_coordinate_mapping` | `python/molecularis/structure_alignment.py` | test_structure_alignment.py | none |
| `sequence.local_alignment_reference_search` | `python/molecularis/sequence_reference.py` | test_sequence_reference.py | none |
| `genome.gff3_annotation_import` | `python/molecularis/gff3.py` | test_gff3.py, test_gff3_transcripts.py | none |
| `sequence.local_fasta_alignment_search` | `python/molecularis/sequence_pack.py` | test_sequence_pack.py | none |
| `genome.gff3_transcript_cds_reconstruction` | `python/molecularis/gff3_transcripts.py` | test_gff3_transcripts.py | none |
| `protein.hmmer_domain_candidate_ranking` | `python/molecularis/hmmer_rank.py` | test_hmmer_rank.py | none |
| `protein.hmmscan_domtblout_evidence` | `python/molecularis/hmmer.py` | test_hmmer.py, test_hmmer_rank.py | none |
| `structure.pinned_local_prediction_process` | `python/molecularis/s4_process.py` | test_s4_process.py | none |
| `genome.augustus_local_gene_candidates` | `python/molecularis/augustus.py` | test_augustus.py | none |
| `genome.prodigal_local_gene_candidates` | `python/molecularis/prodigal.py` | test_prodigal.py | none |
| `genome.pinned_local_gff3_annotator` | `python/molecularis/genome_annotation.py` | test_genome_annotation.py | none |
| `structure.local_prediction_engine_adapter` | `python/molecularis/s4_engine.py` | test_s4_engine.py | none |

## Every planned UI, setting and security entry

| ID | Label / schema key | Collection | Track | Declared tests |
|---|---|---|---|---|
| `ui.home` | Home dashboard | ui_screens | UI | [] |
| `ui.work` | Work and research job list | ui_screens | UI | [] |
| `ui.explore` | Scientific capability catalogue | ui_screens | UI | [] |
| `ui.domains` | Domain browser | ui_screens | UI | [] |
| `ui.tools` | Tool search and runner | ui_screens | UI | [] |
| `ui.data` | Projects and data | ui_screens | UI | [] |
| `ui.jobs` | Job list and detail | ui_screens | UI | [] |
| `ui.settings` | Settings catalogue | ui_screens | UI | [] |
| `ui.onboarding` | Splash and onboarding | ui_screens | UI | [] |
| `ui.sequence` | Sequence viewer/editor | ui_screens | UI | [] |
| `ui.alignment` | Alignment viewer | ui_screens | UI | [] |
| `ui.tree` | Tree viewer | ui_screens | UI | [] |
| `ui.structure` | 3D structure viewer | ui_screens | UI | [] |
| `ui.chemistry` | Chemistry viewer | ui_screens | UI | [] |
| `ui.kinetics` | Kinetics lab | ui_screens | UI | [] |
| `ui.genomics` | Genomics and variants | ui_screens | UI | [] |
| `ui.pgx` | PGx Research Mode | ui_screens | UI | [] |
| `ui.insilico` | In-silico job builder | ui_screens | UI | [] |
| `ui.charts` | Charts studio | ui_screens | UI | [] |
| `ui.packs` | Data pack manager | ui_screens | UI | [] |
| `ui.provenance` | Provenance viewer | ui_screens | UI | [] |
| `ui.export` | Export/share | ui_screens | UI | [] |
| `ui.node` | Remote node setup | ui_screens | UI | [] |
| `ui.security` | Security and privacy | ui_screens | UI | [] |
| `ui.about` | About and licences | ui_screens | UI | [] |
| `ui.component_gallery` | Development component gallery | ui_screens | UI | [] |
| `setting.appearance_theme` | appearance.theme | ui_settings | UI | [] |
| `setting.appearance_theme_family` | appearance.theme_family | ui_settings | UI | [] |
| `setting.appearance_font_family` | appearance.font_family | ui_settings | UI | [] |
| `setting.appearance_accent_seed` | appearance.accent_seed | ui_settings | UI | [] |
| `setting.appearance_corner_style` | appearance.corner_style | ui_settings | UI | [] |
| `setting.appearance_density` | appearance.density | ui_settings | UI | [] |
| `setting.appearance_font_scale` | appearance.font_scale | ui_settings | UI | [] |
| `setting.accessibility_reduce_motion` | accessibility.reduce_motion | ui_settings | UI | [] |
| `setting.accessibility_high_contrast` | accessibility.high_contrast | ui_settings | UI | [] |
| `setting.accessibility_color_vision_safe` | accessibility.color_vision_safe | ui_settings | UI | [] |
| `setting.scientific_units` | scientific.units | ui_settings | UI | [] |
| `setting.scientific_significant_figures` | scientific.significant_figures | ui_settings | UI | [] |
| `setting.compute_preference` | compute.preference | ui_settings | UI | [] |
| `setting.data_wifi_only_downloads` | data.wifi_only_downloads | ui_settings | UI | [] |
| `setting.privacy_offline_only` | privacy.offline_only | ui_settings | UI | [] |
| `setting.privacy_hide_sensitive_recents` | privacy.hide_sensitive_recents | ui_settings | UI | [] |
| `setting.security_app_lock` | security.app_lock | ui_settings | UI | [] |
| `setting.security_lock_on_background` | security.lock_on_background | ui_settings | UI | [] |
| `setting.security_flag_secure_sensitive` | security.flag_secure_sensitive | ui_settings | UI | [] |
| `setting.backup_encrypted_manual_only` | backup.encrypted_manual_only | ui_settings | UI | [] |
| `setting.notifications_job_status` | notifications.job_status | ui_settings | UI | [] |
| `setting.advanced_verbose_local_logs` | advanced.verbose_local_logs | ui_settings | UI | [] |
| `security.app_lock` | App lock and biometric/device credential | security_features | G | [] |
| `security.vault_lock` | Sensitive project vault lock | security_features | G | [] |
| `security.flag_secure` | Sensitive-screen screenshot protection | security_features | G | [] |
| `security.recents` | Hide sensitive Recents thumbnails | security_features | G | [] |
| `security.encrypted_settings` | Encrypted settings and backups | security_features | G | [] |
| `security.consent` | Consent centre | security_features | G | [] |
| `security.inventory` | Data inventory and per-project deletion | security_features | G | [] |
| `security.audit` | Local tamper-evident audit log | security_features | G | [] |
| `security.offline` | Offline-only network enforcement | security_features | G | [] |
| `security.node_pin` | Remote-node TLS certificate pinning | security_features | G | [] |
| `security.send_preview` | Data-to-be-sent preview | security_features | G | [] |
| `security.never_leave_device` | Per-project never-leave-device lock | security_features | G | [] |
| `security.webview_bridge` | Hardened typed WebView bridge | security_features | G | [] |
| `security.panic_wipe` | Optional panic wipe | security_features | G | [] |

## Test coverage interpretation

The repository has 68 Python test files. Related test groups include sequence/reference and FASTx; genetic-code translation/inference; ORF and genome QC; SAM/VCF/BAM and GFF3; BLASTP/HMMER; kinetics; protein/motifs/design; structure parsing/alignment/pockets/quality/prediction/viewer; chemistry/RDKit; phylogeny; omics; PGx/PharmVar; PK/PD; docking/OpenMM; and Android host-probe integration. These are module-level tests, not explicit capability-ID-linked test cases. The registry checker currently validates source paths and evidence references but does not enforce a test mapping for each tool.

Android dispatch tests exercise many allow-listed capabilities through a host probe. This does not prove packaged physical-device execution or full workflow integration. Viewer asset tests primarily verify the existing offline Android/WebView boundary, not desktop viewer parity.

## Findings and required work

### P0 — Registry contract must mature
1. Design a versioned registry v2; do not silently mutate schema v1. Add engines, data packs, domains, platform bindings, validation records, device logs, claims and stable evidence references.
2. For every capability, add reviewed test IDs, runtime/dependency requirements, input/output contracts, supported platforms and compute tier, limitations, provenance and licence/data requirements.
3. Separate source-present, importable, executable, integrated, platform-tested, scientifically validated and release-enabled states. Today `implemented` means only that a source file exists.
4. Evidence must identify commit, CI run, selected tests, environment and independent reference where applicable. Do not upgrade evidence by inference.

### P1 — Platform surfaces
5. The 26 UI screens, 22 settings and 14 security features are planned registry targets. Define acceptance criteria and platform tests; separately inspect Android implementations and preserve their data contracts.
6. Threat-model each security control before implementation. Similar legacy functionality does not equal target-platform completion.

### P1 — Scientific services
7. Structure capabilities require canonical atom/residue/chain identity and PDB/mmCIF coverage. Preparation, 3D viewer, analysis and quality are separate services; current viewer tests do not prove complete Mol* or cross-platform rendering.
8. Vina and OpenMM are bounded adapters with preparation and independent benchmark gaps; do not advertise them as production engines.
9. PGx remains research-only and incomplete; no clinical interpretation or recommendation.
10. Kinetics has source and tests, but evidence remains none; independent reference concordance is still required.

## Recommended sequence

1. Versioned registry v2 and explicit test/evidence mapping.
2. Android persisted-identifier and data-migration inventory, compatibility fixtures and rollback plan.
3. Five-platform UI/runtime feasibility and shared project/job/provenance contracts.
4. Installed desktop shell, local/offline projects, filesystem, job lifecycle and accessibility.
5. One complete evidence-ready scientific vertical slice (kinetics or sequence import/QC), including independent references.
6. Staged 3D structure service: ingestion, preparation, viewer, analysis, quality and validation.
7. Additional science engines/data packs and optional compute profiles according to evidence, rights and measured resource needs.
8. Android compatibility migration, then iOS/iPadOS client after parity and rollback tests.

## Audit limitations

- Path checks prove tracked-file existence only, not function correctness, importability, optional dependency availability or runtime execution.
- Test links are module-level candidates; registry lacks exact test IDs per capability.
- The complete test suite was not executed as part of this document review; CI must validate the exact PR head.
- Android persisted IDs, encryption/AAD compatibility and migrations remain a separate mandatory audit.
- No scientific, clinical, legal, privacy, security or ethics approval is implied.

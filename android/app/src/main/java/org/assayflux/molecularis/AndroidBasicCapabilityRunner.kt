package org.assayflux.molecularis

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/** Explicitly allow-listed local bridges for simple sequence/protein research tools. */
internal object AndroidBasicCapabilityRunner {
    const val MAX_INPUT_CHARS = 1_000_000

    private val supported = setOf(
        "protein.descriptors",
        "molecular.primer_screen",
        "molecular.crispr_pam",
        "genome.orf_candidate_scan",
        "kinetics.michaelis_menten",
        "phylo.newick",
        "sequence.global_alignment",
        "genome.contig_assembly_qc",
        "structure.sasa",
        "structure.interaction_candidates",
        "microbiome.diversity",
        "omics.logistic_growth",
        "sequence.explicit_genetic_code_translation",
        "kinetics.inhibition_rate",
        "phylo.upgma",
        "omics.normalisation",
        "omics.cross_correlation",
        "phylo.jukes_cantor_nj",
        "genome.gff3_annotation_import",
        "genome.gff3_transcript_cds_reconstruction",
        "protein.fixed_width_motif_scan",
        "genes.catalogue_coverage_report",
        "protein.hmmscan_domain_evidence",
        "protein.hmmscan_domtblout_evidence",
        "protein.hmmer_domain_candidate_ranking",
        "genome.prokaryotic_orf_candidate_scan",
        "kinetics.bootstrap_intervals",
        "protein.design_brief_validation",
        "structure.geometry_screen_metrics",
        "structure.prediction_envelope_validation",
        "structure.experimental_ca_comparison",
        "phylo.nj_site_bootstrap",
        "structure.exact_sequence_mapping",
        "structure.chain_interface_contacts",
        "structure.alignment_coordinate_mapping",
        "structure.variant_coordinate_mapping",
        "sequence.exact_reference_search",
        "sequence.local_alignment_reference_search",
        "sequence.local_fasta_exact_search",
        "sequence.local_fasta_alignment_search",
        "phylo.newick_export",
        "structure.pdb_geometry",
        "sequence.local_reference_pack_loader",
        "sequence.local_blastp",
        "sequence.local_hmmpress",
        "sequence.local_hmmscan",
        "variant.reference_checked_normalization",
        "genes.ncbi_catalogue",
        "genomics.variant_normalization",
        "omics.nb2_glm",
        "genomics.bam_core",
        "pgx.star_allele_definitions",
        "chemistry.rdkit_adapter",
        "genomics.htslib_bam_cram",
        "pgx.pharmvar_tsv",
        "structure.viewer_payload",
        "structure.session_export",
        "structure.pinned_local_prediction_process",
        "genome.augustus_local_gene_candidates",
        "genome.prodigal_local_gene_candidates",
        "genome.pinned_local_gff3_annotator",
        "structure.local_prediction_engine_adapter"
    )

    fun analyze(context: Context, capabilityId: String, sequenceText: String): String {
        require(capabilityId in supported) { "Unsupported Android capability: $capabilityId" }
        require(sequenceText.isNotBlank()) { "Sequence input must not be blank" }
        require(sequenceText.length <= MAX_INPUT_CHARS) {
            "Sequence input exceeds the 1,000,000-character mobile limit"
        }
        if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
        return Python.getInstance().getModule("kinetics_probe")
            .callAttr("run_android_basic_capability", capabilityId, sequenceText)
            .toString()
    }
}

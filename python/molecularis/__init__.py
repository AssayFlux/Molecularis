"""Kinetics offline research primitives.

Source implementation does not imply independent scientific validation or clinical use.
"""

__version__ = "0.1.0"

from .admet_validation import (
    binary_admet_metrics,
    scaffold_group_split,
    tanimoto_applicability_domain,
)

from .catalog import (
    GeneEntry, iter_ncbi_gene_info, iter_ncbi_gene_info_file, search_gene_catalog, validate_gene_catalog,
)
from .chemistry_rdkit import analyze_molblock, analyze_smiles, morgan_tanimoto, rdkit_backend_info
from .chemistry import (
    graph_descriptors, iter_sdf_records, parse_sdf_record, path_fingerprint, substructure_match, tanimoto,
)
from .genomics_htslib import iter_alignment_records
from .genomics import (
    SamRecord, fastq_quality_summary, iter_bam_records, normalize_small_variant, parse_sam, parse_vcf,
)
from .variant_reference import ReferenceSequence, normalize_against_reference
from .kinetics import (
    bootstrap_michaelis_menten, eadie_hofstee, fit_michaelis_menten, hanes_woolf, inhibition_rate,
    lineweaver_burk, michaelis_menten,
)
from .genetic_code_inference import infer_genetic_code_candidates
from .apo_pockets import apo_pocket_candidates
from .structure_pockets import ligand_site_candidates
from .molecular import primer_properties, scan_spcas9_ngg
from .omics import (
    negative_binomial_differential_expression,
    clr_transform, cpm, cross_omics_correlation, logistic_growth,
    log2_fold_change, pearson, shannon_diversity, simpson_diversity,
    welch_differential_expression,
)
from .phylo import Node, bootstrap_neighbor_joining_from_alignment, leaf_names, jukes_cantor_distance, neighbor_joining, neighbor_joining_from_alignment, parse_newick, patristic_distance, to_newick, upgma
from .pharmvar import (PharmVarAlleleDefinition, PharmVarMatch, PharmVarVariant, match_pharmvar_haplotype, parse_pharmvar_tsv)
from .pgx import AlleleMatch, StarAlleleDefinition, VariantKey, match_phased_haplotype, parse_star_allele_definitions
from .docking_vina import run_vina_docking
from .md_openmm import run_openmm_dynamics
from .pkpd import emax_pd, one_compartment_oral_pk
from .protein import protein_descriptors, theoretical_pi
from .virtual_cohort import (
    simulate_hardy_weinberg_cohort,
    simulate_synthetic_additive_variant_effects,
)
from .sequence import (
    SequenceRecord, iter_fasta_records, kmer_counts, needleman_wunsch, parse_fasta, parse_fastq,
    reverse_complement, sequence_statistics, transcribe, trim_fastq_ends,
)
from .structure import (
    Atom, contact_pairs, interaction_candidates, parse_mmcif, parse_pdb, rmsd, solvent_accessible_surface_area,
)

__all__ = [
    "binary_admet_metrics", "scaffold_group_split", "tanimoto_applicability_domain", "bootstrap_neighbor_joining_from_alignment", "simulate_hardy_weinberg_cohort", "simulate_synthetic_additive_variant_effects", "emax_pd", "one_compartment_oral_pk", "run_vina_docking", "run_openmm_dynamics", "apo_pocket_candidates", "analyze_molblock", "analyze_smiles", "morgan_tanimoto", "rdkit_backend_info", "PharmVarAlleleDefinition", "PharmVarMatch", "PharmVarVariant", "match_pharmvar_haplotype", "parse_pharmvar_tsv", "AlleleMatch", "Atom", "GeneEntry", "StarAlleleDefinition", "VariantKey", "bootstrap_michaelis_menten", "Node", "SamRecord", "SequenceRecord",
    "clr_transform", "contact_pairs", "cpm", "cross_omics_correlation",
    "eadie_hofstee", "fastq_quality_summary", "fit_michaelis_menten",
    "graph_descriptors", "hanes_woolf", "inhibition_rate", "infer_genetic_code_candidates", "ligand_site_candidates",
    "iter_alignment_records", "interaction_candidates", "iter_bam_records", "iter_fasta_records", "iter_ncbi_gene_info", "iter_ncbi_gene_info_file", "jukes_cantor_distance", "iter_sdf_records", "kmer_counts", "leaf_names", "lineweaver_burk", "match_phased_haplotype", "parse_star_allele_definitions",
    "log2_fold_change", "logistic_growth", "michaelis_menten", "normalize_small_variant",
    "needleman_wunsch", "neighbor_joining", "neighbor_joining_from_alignment", "negative_binomial_differential_expression", "parse_fasta", "parse_fastq", "parse_newick",
    "parse_mmcif", "parse_pdb", "parse_sam", "parse_sdf_record", "parse_vcf",
    "patristic_distance", "path_fingerprint", "pearson", "primer_properties",
    "protein_descriptors", "reverse_complement", "rmsd", "scan_spcas9_ngg",
    "sequence_statistics", "solvent_accessible_surface_area", "shannon_diversity", "trim_fastq_ends", "simpson_diversity",
    "substructure_match", "tanimoto", "theoretical_pi", "to_newick", "transcribe", "upgma",
    "search_gene_catalog", "validate_gene_catalog", "welch_differential_expression",
    "ReferenceSequence", "normalize_against_reference",
]

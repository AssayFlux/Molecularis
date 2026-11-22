"""Molecularis offline research primitives.

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
from .workflows_service import WorkflowDocument, WorkflowOperation, ingest_workflow, load_workflow, register_workflows_service, validate_workflow, execute_workflow, workflows_rulebook
from .cohorts_service import CohortDocument, CohortMember, CohortVisit, ingest_cohort, load_cohort, register_cohorts_service, cohorts_rulebook
from .chemistry_service import (ChemistryDocument, ingest_chemistry, load_chemistry, register_chemistry_service, chemistry_rulebook)
from .chemistry_rdkit import analyze_molblock, analyze_smiles, morgan_tanimoto, rdkit_backend_info
from .chemistry import (
    graph_descriptors, iter_sdf_records, parse_sdf_record, path_fingerprint, substructure_match, tanimoto,
)
from .alignment_biopython import align_pairwise_biopython
from .dna_rna_service import NucleicAcidDocument, ingest_nucleic_acid, load_nucleic_acid, register_dna_rna_service, dna_rna_rulebook
from .genomics_service import GenomeDocument, ingest_genome, load_genome, register_genomics_service, genomics_rulebook
from .genomics_htslib import iter_alignment_records
from .genomics import (
    SamRecord, fastq_quality_summary, iter_bam_records, normalize_small_variant, parse_sam, parse_vcf,
)
from .variant_reference import ReferenceSequence, normalize_against_reference
from .kinetics_service import (ReactionNetworkDocument, ingest_kinetics, load_kinetics, register_kinetics_service, kinetics_rulebook, simulate_reaction_network)
from .kinetics import (
    bootstrap_michaelis_menten, eadie_hofstee, fit_michaelis_menten, hanes_woolf, inhibition_rate,
    lineweaver_burk, michaelis_menten,
)
from .genetic_code_inference import infer_genetic_code_candidates
from .apo_pockets import apo_pocket_candidates
from .structure_pockets import ligand_site_candidates
from .molecular import primer_properties, scan_spcas9_ngg
from .molecular_model import (
    Molecule, MolecularAtom, MolecularBond, MolecularChain, MolecularResidue,
)
from .omics_service import OmicsDocument, ingest_omics, load_omics, register_omics_service, omics_rulebook
from .omics import (
    negative_binomial_differential_expression,
    clr_transform, cpm, cross_omics_correlation, logistic_growth,
    log2_fold_change, pearson, shannon_diversity, simpson_diversity,
    welch_differential_expression,
)
from .phylo import Node, bootstrap_neighbor_joining_from_alignment, leaf_names, jukes_cantor_distance, neighbor_joining, neighbor_joining_from_alignment, parse_newick, patristic_distance, to_newick, upgma
from .phylogeny_service import PhylogenyDocument, ingest_phylogeny, load_phylogeny, register_phylogeny_service, phylogeny_rulebook
from .pharmvar import (PharmVarAlleleDefinition, PharmVarMatch, PharmVarVariant, match_pharmvar_haplotype, parse_pharmvar_tsv)
from .pgx import AlleleMatch, StarAlleleDefinition, VariantKey, match_phased_haplotype, parse_star_allele_definitions
from .pharmacogenomics_service import (
    HaplotypeCall, PharmacogenomicsDocument, ingest_pharmacogenomics, ingest_pgx_definitions,
    load_pharmacogenomics, pharmacogenomics_rulebook, register_pharmacogenomics_service,
)
from .docking_vina import run_vina_docking
from .md_openmm import run_openmm_dynamics
from .pkpd import emax_pd, one_compartment_oral_pk
from .protein import protein_descriptors, theoretical_pi
from .protein_service import ProteinDocument, ingest_protein, load_protein, register_protein_service, protein_rulebook
from .virtual_cohort import (
    simulate_hardy_weinberg_cohort,
    simulate_synthetic_additive_variant_effects,
)
from .simulation_service import SimulationDocument, ingest_simulation, load_simulation, register_simulation_service, simulation_rulebook, analyze_energy_series
from .gromacs import run_gromacs
from .sequence_service import (
    SequenceDocument, ingest_sequence, load_sequence, register_sequence_service, sequence_rulebook,
)
from .sequence import (
    SequenceRecord, iter_fasta_records, kmer_counts, needleman_wunsch, parse_fasta, parse_fastq,
    reverse_complement, sequence_statistics, transcribe, trim_fastq_ends,
)
from .structure_service import (
    StructureDocument, ingest_structure, load_structure, register_structure_service, structure_rulebook,
)
from .structure import (
    Atom, contact_pairs, interaction_candidates, parse_mmcif, parse_pdb, rmsd, solvent_accessible_surface_area,
)

__all__ = [
    "WorkflowDocument", "WorkflowOperation", "ingest_workflow", "load_workflow", "register_workflows_service", "validate_workflow", "execute_workflow", "workflows_rulebook",
    "CohortDocument", "CohortMember", "CohortVisit", "ingest_cohort", "load_cohort", "register_cohorts_service", "cohorts_rulebook",
    "HaplotypeCall", "PharmacogenomicsDocument", "ingest_pharmacogenomics", "ingest_pgx_definitions", "load_pharmacogenomics", "register_pharmacogenomics_service", "pharmacogenomics_rulebook",
    "PhylogenyDocument", "ingest_phylogeny", "load_phylogeny", "register_phylogeny_service", "phylogeny_rulebook",
    "OmicsDocument", "ingest_omics", "load_omics", "register_omics_service", "omics_rulebook",
    "ReactionNetworkDocument", "ingest_kinetics", "load_kinetics", "register_kinetics_service", "kinetics_rulebook", "simulate_reaction_network",
    "SimulationDocument", "ingest_simulation", "load_simulation", "register_simulation_service", "simulation_rulebook", "analyze_energy_series", "run_gromacs",
    "NucleicAcidDocument", "ingest_nucleic_acid", "load_nucleic_acid", "register_dna_rna_service", "dna_rna_rulebook",
    "GenomeDocument", "ingest_genome", "load_genome", "register_genomics_service", "genomics_rulebook",
    "ProteinDocument", "ingest_protein", "load_protein", "register_protein_service", "protein_rulebook",
    "ChemistryDocument", "ingest_chemistry", "load_chemistry", "register_chemistry_service", "chemistry_rulebook",
    "align_pairwise_biopython", "binary_admet_metrics", "scaffold_group_split", "tanimoto_applicability_domain", "bootstrap_neighbor_joining_from_alignment", "simulate_hardy_weinberg_cohort", "simulate_synthetic_additive_variant_effects", "emax_pd", "one_compartment_oral_pk", "run_vina_docking", "run_openmm_dynamics", "apo_pocket_candidates", "analyze_molblock", "analyze_smiles", "morgan_tanimoto", "rdkit_backend_info", "PharmVarAlleleDefinition", "PharmVarMatch", "PharmVarVariant", "match_pharmvar_haplotype", "parse_pharmvar_tsv", "AlleleMatch", "Atom", "GeneEntry", "StarAlleleDefinition", "VariantKey", "bootstrap_michaelis_menten", "Node", "SamRecord", "SequenceRecord",
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
    "Molecule", "MolecularAtom", "MolecularBond", "MolecularChain", "MolecularResidue",
    "SequenceDocument", "ingest_sequence", "load_sequence", "register_sequence_service", "sequence_rulebook",
    "StructureDocument", "ingest_structure", "load_structure", "register_structure_service", "structure_rulebook",
    "ingest_molecule", "load_molecule", "molecular_validation_rulebook", "register_molecular_service",
]


# Domain-neutral Scientific Knowledge Engine (P1).
from .knowledge import (
    AMOUNT, CURRENT, DIMENSIONLESS, LENGTH, MASS, TEMPERATURE, TIME,
    CoordinateReference, Dimension, EquationVariable, EvidenceClass,
    EvidenceRecord, EvidenceStatus, KnowledgePackage, Quantity,
    ScientificConcept, ScientificEntity, ScientificEquation,
    ScientificKnowledgeEngine, ScientificRelation, ScientificSource,
    SourcePermission, UnitDefinition, UnitRegistry,
)

__all__ += [
    "AMOUNT", "CURRENT", "DIMENSIONLESS", "LENGTH", "MASS", "TEMPERATURE", "TIME",
    "CoordinateReference", "Dimension", "EquationVariable", "EvidenceClass",
    "EvidenceRecord", "EvidenceStatus", "KnowledgePackage", "Quantity",
    "ScientificConcept", "ScientificEntity", "ScientificEquation",
    "ScientificKnowledgeEngine", "ScientificRelation", "ScientificSource",
    "SourcePermission", "UnitDefinition", "UnitRegistry",
]

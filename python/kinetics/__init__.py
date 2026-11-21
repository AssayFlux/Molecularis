"""Lazy compatibility namespace for the retired top-level kinetics package.

Importing this package must not eagerly import molecularis: molecularis modules
still import historical kinetics submodules during package initialization.
"""
from __future__ import annotations

from importlib import import_module
from typing import Any

_EXPORT_MODULES = (
    "molecularis.kinetics",
    "molecularis.sequence",
    "molecularis.protein",
    "molecularis.structure_pockets",
    "molecularis.apo_pockets",
    "molecularis.structure",
    "molecularis.chemistry",
    "molecularis.chemistry_rdkit",
    "molecularis.genomics",
    "molecularis.phylo",
    "molecularis.omics",
    "molecularis.pkpd",
    "molecularis.pharmvar",
    "molecularis.pgx",
    "molecularis.molecular",
    "molecularis.variant_reference",
    "molecularis.catalog",
    "molecularis.docking_vina",
    "molecularis.md_openmm",
    "molecularis.virtual_cohort",
    "molecularis.alignment_biopython",
    "molecularis.genomics_htslib",
    "molecularis.admet_validation",
    "molecularis.genetic_code_inference",
)

__all__ = [
    "fit_michaelis_menten", "inhibition_rate", "michaelis_menten",
    "bootstrap_michaelis_menten", "eadie_hofstee", "hanes_woolf",
    "lineweaver_burk", "kmer_counts", "needleman_wunsch", "parse_fasta",
    "parse_fastq", "protein_descriptors", "reverse_complement",
    "sequence_statistics", "theoretical_pi", "transcribe",
    "ligand_site_candidates", "apo_pocket_candidates",
]


def __getattr__(name: str) -> Any:
    for module_name in _EXPORT_MODULES:
        module = import_module(module_name)
        if hasattr(module, name):
            value = getattr(module, name)
            globals()[name] = value
            return value
    raise AttributeError(f"module 'kinetics' has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))

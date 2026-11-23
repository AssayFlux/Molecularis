"""Explicit bootstrap for the complete A–N Molecularis service runtime."""
from __future__ import annotations

from .platform import MolecularisPlatform
from .molecular_service import register_molecular_service
from .sequence_service import register_sequence_service
from .structure_service import register_structure_service
from .chemistry_service import register_chemistry_service
from .protein_service import register_protein_service
from .genomics_service import register_genomics_service
from .dna_rna_service import register_dna_rna_service
from .simulation_service import register_simulation_service
from .kinetics_service import register_kinetics_service
from .omics_service import register_omics_service
from .phylogeny_service import register_phylogeny_service
from .pharmacogenomics_service import register_pharmacogenomics_service
from .cohorts_service import register_cohorts_service
from .workflows_service import register_workflows_service
from .domain_integration import validate_scientific_domains

SERVICE_REGISTRARS = (
    ("A", "molecular", register_molecular_service),
    ("B", "sequence", register_sequence_service),
    ("C", "structure", register_structure_service),
    ("D", "chemistry", register_chemistry_service),
    ("E", "protein", register_protein_service),
    ("F", "genomics", register_genomics_service),
    ("G", "dna_rna", register_dna_rna_service),
    ("H", "simulation", register_simulation_service),
    ("I", "kinetics", register_kinetics_service),
    ("J", "omics", register_omics_service),
    ("K", "phylogeny", register_phylogeny_service),
    ("L", "pharmacogenomics", register_pharmacogenomics_service),
    ("M", "cohorts", register_cohorts_service),
    ("N", "workflows", register_workflows_service),
)


def register_all_services(platform: MolecularisPlatform) -> dict[str, int | list[str]]:
    """Register every A–N capability and handler on a fresh runtime."""
    if platform.state.value != "ready":
        raise RuntimeError("platform must be started before service registration")
    if platform.registry.list():
        raise RuntimeError("A–N bootstrap requires a fresh, empty capability registry")
    registered: list[str] = []
    letter, name = "?", "unknown"
    try:
        for letter, name, registrar in SERVICE_REGISTRARS:
            registrar(platform)
            registered.append(name)
    except Exception as exc:
        raise RuntimeError(
            f"A–N bootstrap failed while registering {letter} ({name}); "
            f"registered services before failure: {registered}"
        ) from exc
    integration = validate_scientific_domains(platform)
    return {
        "service_count": len(registered),
        "domain_count": integration["domain_count"],
        "capability_count": len(platform.registry.list()),
        "services": registered,
    }


def create_full_platform(root: str) -> MolecularisPlatform:
    """Create, start and register a complete local A–N platform."""
    platform = MolecularisPlatform(root)
    platform.start()
    try:
        register_all_services(platform)
    except Exception:
        platform.close()
        raise
    return platform

"""Conservative exact sequence-to-structure residue mapping.

Only unique, contiguous exact matches to standard amino-acid residues are reported.
This does not perform alignment, mutation interpretation, numbering-scheme conversion,
or infer missing/disordered residues.
"""
from __future__ import annotations

from math import ceil, floor, isfinite, sqrt
from typing import Iterable, cast

from .structure import Atom

THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}


def map_exact_chain_sequence(
    query_sequence: str,
    atoms: Iterable[Atom],
    *,
    chain_id: str,
    max_query_residues: int = 1_000_000,
    max_structure_residues: int = 100_000,
    max_atoms: int = 2_000_000,
) -> dict[str, object]:
    """Map a uniquely occurring exact chain sequence to a query protein sequence.

    Residues are keyed by chain and residue number. The current Atom
    representation does not retain insertion codes, so insertion-code-aware mapping
    is explicitly unsupported rather than guessed.
    """
    if not isinstance(query_sequence, str) or not query_sequence:
        raise ValueError("query_sequence must be non-empty text")
    query = "".join(query_sequence.split()).upper()
    if not query or set(query) - set(THREE_TO_ONE.values()):
        raise ValueError("query_sequence must contain only the 20 canonical amino acids")
    for name, limit in (
        ("max_query_residues", max_query_residues),
        ("max_structure_residues", max_structure_residues),
        ("max_atoms", max_atoms),
    ):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError(f"{name} must be a positive integer")
    if len(query) > max_query_residues:
        raise ValueError("query sequence exceeds the configured residue limit")
    if not isinstance(chain_id, str) or not chain_id:
        raise ValueError("chain_id must be non-empty text")

    residues: dict[int, str] = {}
    residue_names: dict[int, str] = {}
    atom_count = 0
    for atom in atoms:
        atom_count += 1
        if atom_count > max_atoms:
            raise ValueError("structure atom stream exceeds the configured atom limit")
        if atom.chain != chain_id:
            continue
        if atom.residue_number not in residues and len(residues) >= max_structure_residues:
            raise ValueError("structure chain exceeds the configured residue limit")
        residue_name = atom.residue.upper()
        amino_acid = THREE_TO_ONE.get(residue_name)
        if amino_acid is None:
            raise ValueError(
                f"Unsupported/non-standard residue {residue_name} in chain {chain_id}; mapping abstained"
            )
        previous = residues.setdefault(atom.residue_number, amino_acid)
        previous_name = residue_names.setdefault(atom.residue_number, residue_name)
        if previous != amino_acid or previous_name != residue_name:
            raise ValueError("Conflicting residue identity at one chain position")
    ordered = sorted(residues.items())
    if not ordered:
        raise ValueError(f"No canonical residues found for chain {chain_id}")
    if any(
        current_number != previous_number + 1
        for (previous_number, _), (current_number, _) in zip(ordered, ordered[1:])
    ):
        return {
            "status": "noncontiguous_structure_numbering",
            "chain_id": chain_id,
            "observed_chain_sequence": "".join(amino_acid for _, amino_acid in ordered),
            "query_length": len(query),
            "mapped_residues": [],
            "limitations": [
                "Residue numbering gaps are not repaired or assumed to be contiguous.",
                "No alignment, missing-residue reconstruction or insertion-code conversion is performed.",
            ],
        }

    observed = "".join(amino_acid for _, amino_acid in ordered)
    positions: list[int] = []
    search_from = 0
    while True:
        position = query.find(observed, search_from)
        if position < 0:
            break
        positions.append(position)
        # Advance one residue so every overlapping exact occurrence is reported.
        search_from = position + 1
    if not positions:
        return {
            "status": "no_exact_match",
            "chain_id": chain_id,
            "observed_chain_sequence": observed,
            "query_length": len(query),
            "mapped_residues": [],
            "limitations": [
                "Exact contiguous matching only; no alignment or gap handling.",
                "Missing/disordered residues can prevent a match.",
                "Insertion codes are not retained by the current atom model.",
            ],
        }
    if len(positions) != 1:
        return {
            "status": "ambiguous_exact_match",
            "chain_id": chain_id,
            "observed_chain_sequence": observed,
            "query_length": len(query),
            "candidate_query_starts_1based": [position + 1 for position in positions],
            "mapped_residues": [],
            "limitations": [
                "Repeated exact occurrences are ambiguous and are not arbitrarily selected.",
                "No alignment, gap handling or insertion-code conversion is performed.",
            ],
        }

    start = positions[0]
    mapped = [
        {
            "query_position_1based": start + index + 1,
            "chain_id": chain_id,
            "structure_residue_number": residue_number,
            "residue_name": residue_names[residue_number],
            "amino_acid": amino_acid,
        }
        for index, (residue_number, amino_acid) in enumerate(ordered)
    ]
    return {
        "status": "exact_unique_match",
        "chain_id": chain_id,
        "observed_chain_sequence": observed,
        "query_length": len(query),
        "query_start_1based": start + 1,
        "query_end_1based": start + len(observed),
        "mapped_residues": mapped,
        "limitations": [
            "Exact contiguous matching only; no alignment or gap handling.",
            "Missing/disordered residues can prevent a match.",
            "Insertion codes are not retained by the current atom model.",
            "This mapping is not evidence of variant effect or protein function.",
        ],
    }



def map_variant_to_structure(
    query_sequence: str,
    atoms: Iterable[Atom],
    *,
    chain_id: str,
    variant_position_1based: int,
    reference_amino_acid: str,
    alternate_amino_acid: str,
    max_query_residues: int = 1_000_000,
    max_structure_residues: int = 100_000,
    max_atoms: int = 2_000_000,
) -> dict[str, object]:
    """Map one protein substitution to a structure only through a unique exact chain match.

    This reports coordinate correspondence only. It does not predict structural,
    functional, pathogenic or clinical effect.
    """
    if (
        isinstance(variant_position_1based, bool)
        or not isinstance(variant_position_1based, int)
        or variant_position_1based < 1
    ):
        raise ValueError("variant_position_1based must be a positive integer")
    if (
        not isinstance(reference_amino_acid, str)
        or len(reference_amino_acid) != 1
        or reference_amino_acid not in THREE_TO_ONE.values()
    ):
        raise ValueError("reference_amino_acid must be one canonical amino-acid letter")
    if (
        not isinstance(alternate_amino_acid, str)
        or len(alternate_amino_acid) != 1
        or alternate_amino_acid not in THREE_TO_ONE.values()
    ):
        raise ValueError("alternate_amino_acid must be one canonical amino-acid letter")
    if alternate_amino_acid == reference_amino_acid:
        raise ValueError("Reference and alternate amino acids must differ")
    query = "".join(query_sequence.split()).upper() if isinstance(query_sequence, str) else ""
    if not query or variant_position_1based > len(query):
        raise ValueError("Variant position is outside the query protein sequence")
    observed_reference = query[variant_position_1based - 1]
    if observed_reference != reference_amino_acid:
        raise ValueError(
            f"Variant reference amino acid {reference_amino_acid} does not match query "
            f"residue {observed_reference} at position {variant_position_1based}"
        )

    mapping = map_exact_chain_sequence(
        query,
        atoms,
        chain_id=chain_id,
        max_query_residues=max_query_residues,
        max_structure_residues=max_structure_residues,
        max_atoms=max_atoms,
    )
    if mapping["status"] != "exact_unique_match":
        return {
            "schema": "kinetics.structure-variant-map.v1",
            "status": "abstained",
            "mapping_status": mapping["status"],
            "variant": {
                "position_1based": variant_position_1based,
                "reference": reference_amino_acid,
                "alternate": alternate_amino_acid,
            },
            "mapped_residue": None,
            "limitations": [
                "Variant-to-structure mapping requires a unique contiguous exact chain match.",
                "No structural, functional, pathogenic or clinical effect is inferred.",
            ],
        }

    mapped_residues = mapping.get("mapped_residues")
    if not isinstance(mapped_residues, list):
        return {
            "schema": "kinetics.structure-variant-map.v1",
            "status": "abstained",
            "mapping_status": "invalid_mapping_payload",
            "variant": {
                "position_1based": variant_position_1based,
                "reference": reference_amino_acid,
                "alternate": alternate_amino_acid,
            },
            "mapped_residue": None,
            "limitations": ["The sequence-to-structure mapper returned no residue mapping list."],
        }
    mapped = next(
        (
            item for item in mapped_residues
            if isinstance(item, dict)
            and item.get("query_position_1based") == variant_position_1based
        ),
        None,
    )
    if mapped is None:
        return {
            "schema": "kinetics.structure-variant-map.v1",
            "status": "not_covered_by_structure",
            "mapping_status": mapping["status"],
            "variant": {
                "position_1based": variant_position_1based,
                "reference": reference_amino_acid,
                "alternate": alternate_amino_acid,
            },
            "mapped_residue": None,
            "limitations": [
                "The exact structure chain does not cover the requested query position.",
                "No structural, functional, pathogenic or clinical effect is inferred.",
            ],
        }
    return {
        "schema": "kinetics.structure-variant-map.v1",
        "status": "mapped_coordinate_only",
        "mapping_status": mapping["status"],
        "mapping_quality": "unique_contiguous_exact_sequence",
        "variant": {
            "position_1based": variant_position_1based,
            "reference": reference_amino_acid,
            "alternate": alternate_amino_acid,
        },
        "mapped_residue": mapped,
        "limitations": [
            "This is coordinate correspondence only, not a mutation model.",
            "No side-chain rebuilding, energy calculation, stability prediction or interface effect is performed.",
            "No pathogenicity, clinical significance or biological function is inferred.",
            "Insertion codes are not retained by the current atom model.",
        ],
    }



def chain_interface_contacts(
    atoms: Iterable[Atom],
    *,
    chain_a: str,
    chain_b: str,
    cutoff_angstrom: float = 8.0,
    max_atoms: int = 100_000,
    max_candidate_pairs: int = 2_000_000,
    max_residue_pairs: int = 100_000,
) -> dict[str, object]:
    """Report heavy-atom inter-chain contacts with bounded spatial-neighbour search.

    This is a geometric contact count/minimum-distance report, not an interface
    energy, binding-affinity, pocket, or functional-effect prediction.
    """
    if not isinstance(chain_a, str) or not chain_a or not isinstance(chain_b, str) or not chain_b:
        raise ValueError("chain_a and chain_b must be non-empty text")
    if chain_a == chain_b:
        raise ValueError("chain_a and chain_b must be different")
    if (
        isinstance(cutoff_angstrom, bool)
        or not isinstance(cutoff_angstrom, (int, float))
        or not isfinite(cutoff_angstrom)
        or cutoff_angstrom <= 0
    ):
        raise ValueError("cutoff_angstrom must be finite and positive")
    for name, value in (
        ("max_atoms", max_atoms),
        ("max_candidate_pairs", max_candidate_pairs),
        ("max_residue_pairs", max_residue_pairs),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")

    first_chain: list[tuple[int, Atom]] = []
    second_chain: list[tuple[int, Atom]] = []
    atom_count = 0
    for index, atom in enumerate(atoms):
        atom_count += 1
        if atom_count > max_atoms:
            raise ValueError("Structure exceeds max_atoms")
        if not all(isfinite(value) for value in (atom.x, atom.y, atom.z)):
            raise ValueError("Structure contains non-finite coordinates")
        if atom.element.strip().upper() == "H":
            continue
        if atom.chain == chain_a:
            first_chain.append((index, atom))
        elif atom.chain == chain_b:
            second_chain.append((index, atom))
    if not first_chain or not second_chain:
        raise ValueError("Both requested chains must contain heavy atoms")

    cell_size = float(cutoff_angstrom)
    cells: dict[tuple[int, int, int], list[tuple[int, Atom]]] = {}
    for item in second_chain:
        atom = item[1]
        key = (floor(atom.x / cell_size), floor(atom.y / cell_size), floor(atom.z / cell_size))
        cells.setdefault(key, []).append(item)

    radius = ceil(cutoff_angstrom / cell_size)
    pairs: dict[tuple[int, str, int, str], dict[str, object]] = {}
    candidate_pairs = 0
    for _, first in first_chain:
        key = (floor(first.x / cell_size), floor(first.y / cell_size), floor(first.z / cell_size))
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    for _, second in cells.get((key[0] + dx, key[1] + dy, key[2] + dz), ()):
                        candidate_pairs += 1
                        if candidate_pairs > max_candidate_pairs:
                            raise ValueError("Structure exceeds max_candidate_pairs")
                        distance = sqrt(
                            (first.x - second.x) ** 2
                            + (first.y - second.y) ** 2
                            + (first.z - second.z) ** 2
                        )
                        if distance > cutoff_angstrom:
                            continue
                        pair_key = (
                            first.residue_number, first.residue,
                            second.residue_number, second.residue,
                        )
                        if pair_key not in pairs and len(pairs) >= max_residue_pairs:
                            raise ValueError("Structure exceeds max_residue_pairs")
                        entry = pairs.setdefault(pair_key, {
                            "chain_a": chain_a,
                            "residue_a": first.residue_number,
                            "residue_name_a": first.residue,
                            "chain_b": chain_b,
                            "residue_b": second.residue_number,
                            "residue_name_b": second.residue,
                            "atom_contact_count": 0,
                            "minimum_distance_angstrom": distance,
                        })
                        contact_count_value = entry["atom_contact_count"]
                        minimum_distance_value = entry["minimum_distance_angstrom"]
                        if (
                            not isinstance(contact_count_value, int)
                            or not isinstance(minimum_distance_value, (int, float))
                        ):
                            raise RuntimeError("Internal interface-contact accumulator is malformed")
                        contact_count = contact_count_value
                        current_minimum = float(minimum_distance_value)
                        entry["atom_contact_count"] = contact_count + 1
                        entry["minimum_distance_angstrom"] = min(current_minimum, distance)

    def contact_sort_key(item: dict[str, object]) -> tuple[int, float, int, str, int, str]:
        contact_count = item["atom_contact_count"]
        minimum_distance = item["minimum_distance_angstrom"]
        residue_a = item["residue_a"]
        residue_name_a = item["residue_name_a"]
        residue_b = item["residue_b"]
        residue_name_b = item["residue_name_b"]
        if (
            not isinstance(contact_count, int)
            or not isinstance(minimum_distance, (int, float))
            or not isinstance(residue_a, int)
            or not isinstance(residue_name_a, str)
            or not isinstance(residue_b, int)
            or not isinstance(residue_name_b, str)
        ):
            raise RuntimeError("Internal interface-contact result is malformed")
        # Explicit residue tie-breakers make output independent of atom input order.
        return (
            -contact_count, float(minimum_distance),
            residue_a, residue_name_a, residue_b, residue_name_b,
        )

    contacts = sorted(pairs.values(), key=contact_sort_key)
    return {
        "schema": "kinetics.chain-interface-contacts.v1",
        "chain_a": chain_a,
        "chain_b": chain_b,
        "cutoff_angstrom": float(cutoff_angstrom),
        "candidate_pair_count": candidate_pairs,
        "residue_pair_count": len(contacts),
        "atom_contact_count": sum(cast(int, item["atom_contact_count"]) for item in contacts),
        "residue_contacts": contacts,
        "interpretation": "geometric_interface_contacts_only",
        "limitations": [
            "Hydrogen atoms are excluded; no protonation or chemical bond model is used.",
            "No interface energy, binding affinity, pocket, stability or functional effect is predicted.",
            "Residue insertion codes and alternate conformations are not represented in the Atom model.",
        ],
    }

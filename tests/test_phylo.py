from __future__ import annotations

import pytest

from molecularis.phylo import leaf_names, parse_newick, upgma


def test_newick_supports_quoted_labels_with_delimiters_and_escaped_quotes() -> None:
    tree = parse_newick("('A, B':1,'C''D':2);")
    assert leaf_names(tree) == ["A, B", "C'D"]


@pytest.mark.parametrize("source", ["(A:NaN,B:1);", "(A:inf,B:1);", "(A:-1,B:1);", "('A,B:1);"])
def test_newick_rejects_non_finite_negative_and_unterminated_values(source: str) -> None:
    with pytest.raises(ValueError):
        parse_newick(source)


def test_upgma_rejects_non_finite_distance_values() -> None:
    with pytest.raises(ValueError, match="finite"):
        upgma([[0.0, float("nan")], [float("nan"), 0.0]], ["a", "b"])


def test_neighbor_joining_recovers_additive_three_taxon_distances() -> None:
    from molecularis.phylo import neighbor_joining, patristic_distance

    tree = neighbor_joining(
        [[0.0, 2.0, 4.0], [2.0, 0.0, 4.0], [4.0, 4.0, 0.0]],
        ["A", "B", "C"],
    )
    assert patristic_distance(tree, "A", "B") == pytest.approx(2.0)
    assert patristic_distance(tree, "A", "C") == pytest.approx(4.0)
    assert patristic_distance(tree, "B", "C") == pytest.approx(4.0)


def test_neighbor_joining_rejects_negative_inferred_limb() -> None:
    from molecularis.phylo import neighbor_joining

    with pytest.raises(ValueError, match="negative branch"):
        neighbor_joining(
            [[0.0, 1.0, 10.0], [1.0, 0.0, 1.0], [10.0, 1.0, 0.0]],
            ["A", "B", "C"],
        )



def test_newick_serializer_round_trips_quoted_labels_and_branch_lengths() -> None:
    from molecularis.phylo import parse_newick, patristic_distance, to_newick

    original = parse_newick("((A:0.1,'B B':0.2)clade:0.3,C:0);")
    serialized = to_newick(original)
    restored = parse_newick(serialized)
    assert leaf_names(restored) == ["A", "B B", "C"]
    assert patristic_distance(original, "A", "B B") == pytest.approx(
        patristic_distance(restored, "A", "B B")
    )



def test_jukes_cantor_distance_and_model_based_alignment_tree() -> None:
    from molecularis.phylo import jukes_cantor_distance, neighbor_joining_from_alignment

    result = jukes_cantor_distance("A" * 40, "A" * 39 + "G", minimum_sites=30)
    assert result["distance"] > 0
    assert result["comparable_sites"] == 40
    tree = neighbor_joining_from_alignment({
        "A": "A" * 40,
        "B": "A" * 39 + "G",
        "C": "A" * 39 + "G",
    }, minimum_sites=30)
    assert set(leaf_names(tree)) == {"A", "B", "C"}


def test_jukes_cantor_rejects_saturation_and_insufficient_sites() -> None:
    from molecularis.phylo import jukes_cantor_distance

    with pytest.raises(ValueError, match="saturated"):
        jukes_cantor_distance("A" * 20, "C" * 20, minimum_sites=20)
    with pytest.raises(ValueError, match="Too few"):
        jukes_cantor_distance("NNNN", "AAAA", minimum_sites=1)


def test_site_bootstrap_neighbor_joining_is_seeded_and_reports_failures() -> None:
    from molecularis.phylo import bootstrap_neighbor_joining_from_alignment

    alignment = {
        "A": "A" * 40 + "C" * 10,
        "B": "A" * 39 + "G" + "C" * 10,
        "C": "A" * 39 + "G" + "C" * 10,
        "D": "A" * 39 + "G" + "C" * 10,
    }
    first = bootstrap_neighbor_joining_from_alignment(
        alignment, replicates=30, seed=19, minimum_sites=20,
    )
    second = bootstrap_neighbor_joining_from_alignment(
        alignment, replicates=30, seed=19, minimum_sites=20,
    )
    assert first["successful_replicates"] > 0
    assert first["requested_replicates"] == 30
    assert first["splits"] == second["splits"]
    assert all(0.0 <= item["support_percent"] <= 100.0 for item in first["splits"])


def test_site_bootstrap_rejects_invalid_alignment_and_limits() -> None:
    from molecularis.phylo import bootstrap_neighbor_joining_from_alignment

    with pytest.raises(ValueError, match="four unique"):
        bootstrap_neighbor_joining_from_alignment({"A": "AAAA", "B": "AAAT", "C": "AATT"})
    with pytest.raises(ValueError, match="replicates"):
        bootstrap_neighbor_joining_from_alignment(
            {"A": "A" * 30, "B": "C" * 30, "C": "G" * 30, "D": "T" * 30},
            replicates=0,
        )



def test_neighbor_joining_two_taxa_preserves_exact_pair_distance() -> None:
    from molecularis.phylo import neighbor_joining, patristic_distance

    tree = neighbor_joining([[0.0, 7.25], [7.25, 0.0]], ["left", "right"])
    assert patristic_distance(tree, "left", "right") == pytest.approx(7.25)


def test_neighbor_joining_rejects_asymmetric_and_nonzero_diagonal_matrices() -> None:
    from molecularis.phylo import neighbor_joining

    with pytest.raises(ValueError, match="symmetric"):
        neighbor_joining([[0.0, 1.0], [2.0, 0.0]], ["A", "B"])
    with pytest.raises(ValueError, match="diagonal"):
        neighbor_joining([[1.0, 1.0], [1.0, 0.0]], ["A", "B"])


def test_neighbor_joining_tie_resolution_is_deterministic() -> None:
    from molecularis.phylo import neighbor_joining, to_newick

    matrix = [
        [0.0, 2.0, 2.0, 2.0],
        [2.0, 0.0, 2.0, 2.0],
        [2.0, 2.0, 0.0, 2.0],
        [2.0, 2.0, 2.0, 0.0],
    ]
    first = to_newick(neighbor_joining(matrix, ["A", "B", "C", "D"]))
    second = to_newick(neighbor_joining(matrix, ["A", "B", "C", "D"]))
    assert first == second
    assert set(leaf_names(neighbor_joining(matrix, ["A", "B", "C", "D"]))) == {
        "A", "B", "C", "D",
    }

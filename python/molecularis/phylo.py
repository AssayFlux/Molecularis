"""Newick parsing and distance-based phylogenetic tree utilities."""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from math import isfinite, log


@dataclass
class Node:
    name: str = ""
    length: float = 0.0
    children: list["Node"] = field(default_factory=list)


class _Parser:
    def __init__(self, source: str) -> None:
        self.tokens: list[str] = []
        token: list[str] = []
        quoted = False
        text = source.strip()
        index = 0
        while index < len(text):
            char = text[index]
            if char == "'":
                if quoted and index + 1 < len(text) and text[index + 1] == "'":
                    token.append("'")
                    index += 2
                    continue
                quoted = not quoted
                index += 1
                continue
            if not quoted and char in "(),:;":
                if token:
                    value = "".join(token).strip()
                    if value:
                        self.tokens.append(value)
                    token = []
                self.tokens.append(char)
            else:
                token.append(char)
            index += 1
        if quoted:
            raise ValueError("Unterminated quoted Newick label")
        if token:
            value = "".join(token).strip()
            if value:
                self.tokens.append(value)
        self.index = 0

    def peek(self) -> str | None:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def pop(self) -> str:
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of Newick tree")
        self.index += 1
        return token

    def subtree(self) -> Node:
        node = Node()
        if self.peek() == "(":
            self.pop()
            node.children.append(self.subtree())
            while self.peek() == ",":
                self.pop()
                node.children.append(self.subtree())
            if self.pop() != ")":
                raise ValueError("Unbalanced Newick parentheses")
        label = self.peek()
        if label is not None and label not in {",", ")", ":", ";"}:
            node.name = self.pop()
        if self.peek() == ":":
            self.pop()
            raw_length = self.pop()
            try:
                node.length = float(raw_length)
            except ValueError as exc:
                raise ValueError(f"Invalid branch length: {raw_length}") from exc
            if not isfinite(node.length) or node.length < 0:
                raise ValueError("Branch lengths must be finite and non-negative")
        return node


def parse_newick(source: str) -> Node:
    if not source.strip():
        raise ValueError("Newick tree cannot be empty")
    parser = _Parser(source)
    root = parser.subtree()
    if parser.pop() != ";" or parser.peek() is not None:
        raise ValueError("Newick must contain one tree terminated by semicolon")
    return root


def leaf_names(root: Node) -> list[str]:
    return [node.name for node in _walk(root) if not node.children]


def patristic_distance(root: Node, first: str, second: str) -> float:
    paths: dict[str, list[tuple[Node, float]]] = {}

    def visit(node: Node, ancestors: list[tuple[Node, float]], distance: float) -> None:
        current = ancestors + [(node, distance)]
        if not node.children:
            if node.name in paths:
                raise ValueError(f"Duplicate leaf name: {node.name}")
            paths[node.name] = current
        for child in node.children:
            visit(child, current, distance + child.length)

    visit(root, [], 0.0)
    if first not in paths or second not in paths:
        raise ValueError("Requested leaf is absent")
    a, b = paths[first], paths[second]
    common = 0
    while common < min(len(a), len(b)) and a[common][0] is b[common][0]:
        common += 1
    return a[-1][1] + b[-1][1] - 2 * (a[common - 1][1] if common else 0.0)


def _walk(node: Node) -> Iterator[Node]:
    yield node
    for child in node.children:
        yield from _walk(child)


def upgma(distance_matrix: list[list[float]], labels: list[str]) -> Node:
    """Construct a rooted UPGMA tree from a finite symmetric distance matrix."""
    size = len(labels)
    if size < 2 or len(distance_matrix) != size or len(set(labels)) != size:
        raise ValueError("Need at least two unique labels and a square matrix")
    if any(len(row) != size for row in distance_matrix):
        raise ValueError("Distance matrix must be square")
    for i in range(size):
        if not isfinite(distance_matrix[i][i]) or abs(distance_matrix[i][i]) > 1e-12:
            raise ValueError("Distance matrix diagonal must be finite and zero")
        for j in range(size):
            value = distance_matrix[i][j]
            if not isfinite(value) or value < 0 or abs(value - distance_matrix[j][i]) > 1e-9:
                raise ValueError("Distances must be finite, non-negative and symmetric")
    clusters: dict[int, tuple[Node, list[int], float]] = {
        i: (Node(name=labels[i]), [i], 0.0) for i in range(size)
    }
    distances = {(i, j): distance_matrix[i][j] for i in range(size) for j in range(i + 1, size)}
    next_id = size
    while len(clusters) > 1:
        pair = min(distances, key=lambda key: distances[key])
        first, second = pair
        distance = distances[pair]
        height = distance / 2.0
        left, left_members, left_height = clusters.pop(first)
        right, right_members, right_height = clusters.pop(second)
        left.length = max(0.0, height - left_height)
        right.length = max(0.0, height - right_height)
        merged = Node(children=[left, right])
        members = left_members + right_members
        old_ids = list(clusters)
        distances = {
            key: value for key, value in distances.items()
            if first not in key and second not in key
        }
        for other in old_ids:
            other_members = clusters[other][1]
            numerator = sum(distance_matrix[a][b] for a in members for b in other_members)
            distances[(min(next_id, other), max(next_id, other))] = numerator / (
                len(members) * len(other_members)
            )
        clusters[next_id] = (merged, members, height)
        next_id += 1
    return next(iter(clusters.values()))[0]


def _pair_key(first: int, second: int) -> tuple[int, int]:
    return (first, second) if first < second else (second, first)


def neighbor_joining(distance_matrix: list[list[float]], labels: list[str]) -> Node:
    """Build a neighbour-joining tree; rejects negative inferred limbs rather than clipping.

    The distance matrix must contain finite, non-negative, symmetric distances with a
    zero diagonal. Non-additive/noisy matrices can imply negative limbs; those inputs
    are rejected and must not be silently altered.
    """
    size = len(labels)
    if size < 2 or len(distance_matrix) != size or len(set(labels)) != size:
        raise ValueError("Need at least two unique labels and a square matrix")
    if any(len(row) != size for row in distance_matrix):
        raise ValueError("Distance matrix must be square")
    for i in range(size):
        if not isfinite(distance_matrix[i][i]) or abs(distance_matrix[i][i]) > 1e-12:
            raise ValueError("Distance matrix diagonal must be finite and zero")
        for j in range(size):
            value = distance_matrix[i][j]
            if not isfinite(value) or value < 0 or abs(value - distance_matrix[j][i]) > 1e-9:
                raise ValueError("Distances must be finite, non-negative and symmetric")
    clusters: dict[int, Node] = {i: Node(name=labels[i]) for i in range(size)}
    distances = {
        (i, j): float(distance_matrix[i][j])
        for i in range(size) for j in range(i + 1, size)
    }
    next_id = size
    while len(clusters) > 2:
        active = sorted(clusters)
        count = len(active)
        totals = {
            i: sum(distances[_pair_key(i, j)] for j in active if j != i)
            for i in active
        }
        pair = min(
            ((i, j) for pos, i in enumerate(active) for j in active[pos + 1:]),
            key=lambda ij: ((count - 2) * distances[ij] - totals[ij[0]] - totals[ij[1]], ij),
        )
        first, second = pair
        distance = distances[pair]
        limb_first = 0.5 * distance + (totals[first] - totals[second]) / (2 * (count - 2))
        limb_second = distance - limb_first
        tolerance = 1e-10 * max(1.0, distance)
        if limb_first < -tolerance or limb_second < -tolerance:
            raise ValueError("Neighbour joining inferred a negative branch length")
        parent = Node(children=[
            Node(length=max(0.0, limb_first), children=[clusters[first]]),
            Node(length=max(0.0, limb_second), children=[clusters[second]]),
        ])
        others = [item for item in active if item not in pair]
        for item in others:
            left = distances[_pair_key(first, item)]
            right = distances[_pair_key(second, item)]
            new_distance = 0.5 * (left + right - distance)
            if not isfinite(new_distance) or new_distance < -tolerance:
                raise ValueError("Neighbour joining inferred an invalid cluster distance")
            distances[_pair_key(next_id, item)] = max(0.0, new_distance)
        for key in list(distances):
            if first in key or second in key:
                del distances[key]
        del clusters[first]
        del clusters[second]
        clusters[next_id] = parent
        next_id += 1

    first, second = sorted(clusters)
    final_distance = distances[_pair_key(first, second)]
    root = Node(children=[
        Node(length=final_distance / 2.0, children=[clusters[first]]),
        Node(length=final_distance / 2.0, children=[clusters[second]]),
    ])
    return root

def to_newick(root: Node) -> str:
    """Serialize a tree to deterministic Newick with safe quoting and branch lengths."""
    active: set[int] = set()

    def label_text(label: str) -> str:
        if not label:
            return ""
        if any(character.isspace() or character in "(),:;[]'" for character in label):
            return "'" + label.replace("'", "''") + "'"
        return label

    def render(node: Node) -> str:
        identity = id(node)
        if identity in active:
            raise ValueError("Tree contains a cycle")
        if not isfinite(node.length) or node.length < 0:
            raise ValueError("Branch lengths must be finite and non-negative")
        active.add(identity)
        try:
            children = ""
            if node.children:
                children = "(" + ",".join(render(child) for child in node.children) + ")"
            result = children + label_text(node.name)
            if node.length != 0:
                result += ":" + format(node.length, ".17g")
            elif node is not root:
                result += ":0"
            return result
        finally:
            active.remove(identity)

    return render(root) + ";"

def jukes_cantor_distance(
    first: str, second: str, *, minimum_sites: int = 20,
) -> dict[str, float | int | str]:
    """Estimate Jukes-Cantor 1969 nucleotide distance with pairwise deletion.

    Only unambiguous A/C/G/T columns are retained. Saturated comparisons (p >= 0.75)
    fail explicitly rather than returning an arbitrary finite distance.
    """
    if len(first) != len(second) or not first:
        raise ValueError("Aligned sequences must have equal non-zero lengths")
    if not isinstance(minimum_sites, int) or minimum_sites < 1:
        raise ValueError("minimum_sites must be a positive integer")
    valid = set("ACGT")
    pairs = [
        (a.upper(), b.upper()) for a, b in zip(first, second)
        if a.upper() in valid and b.upper() in valid
    ]
    if len(pairs) < minimum_sites:
        raise ValueError("Too few unambiguous aligned sites for distance estimation")
    differences = sum(a != b for a, b in pairs)
    proportion = differences / len(pairs)
    if proportion >= 0.75:
        raise ValueError("Jukes-Cantor distance is undefined for saturated divergence")
    distance = -0.75 * log(1.0 - (4.0 / 3.0) * proportion)
    return {
        "distance": distance,
        "observed_difference_fraction": proportion,
        "comparable_sites": len(pairs),
        "differences": differences,
        "model": "Jukes-Cantor 1969",
    }


def neighbor_joining_from_alignment(
    sequences: dict[str, str], *, minimum_sites: int = 20,
) -> Node:
    """Build a neighbour-joining tree from aligned DNA using Jukes-Cantor distances."""
    labels = list(sequences)
    if len(labels) < 3 or len(set(labels)) != len(labels):
        raise ValueError("At least three uniquely named aligned sequences are required")
    if any(not label for label in labels):
        raise ValueError("Sequence labels cannot be empty")
    aligned = [sequences[label].upper() for label in labels]
    if len({len(sequence) for sequence in aligned}) != 1 or not aligned[0]:
        raise ValueError("All input sequences must have equal non-zero alignment length")
    matrix = [[0.0] * len(labels) for _ in labels]
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            result = jukes_cantor_distance(
                aligned[i], aligned[j], minimum_sites=minimum_sites,
            )
            matrix[i][j] = matrix[j][i] = float(result["distance"])
    return neighbor_joining(matrix, labels)

def _canonical_split(side: set[str], all_labels: set[str]) -> tuple[str, ...] | None:
    other = all_labels - side
    if len(side) < 2 or len(other) < 2:
        return None
    left, right = tuple(sorted(side)), tuple(sorted(other))
    return min(left, right)


def _nontrivial_splits(root: Node) -> set[tuple[str, ...]]:
    all_labels = set(leaf_names(root))
    if len(all_labels) != sum(1 for node in _walk(root) if not node.children):
        raise ValueError("Tree contains duplicate leaf labels")

    splits: set[tuple[str, ...]] = set()

    def visit(node: Node) -> set[str]:
        if not node.children:
            return {node.name}
        descendants: set[str] = set()
        for child in node.children:
            descendants.update(visit(child))
        split = _canonical_split(descendants, all_labels)
        if split is not None:
            splits.add(split)
        return descendants

    visit(root)
    return splits


def bootstrap_neighbor_joining_from_alignment(
    sequences: dict[str, str], *, replicates: int = 100,
    seed: int = 0, minimum_sites: int = 20,
) -> dict[str, object]:
    """Estimate unrooted NJ split support by nonparametric alignment-site bootstrap.

    Each replicate samples alignment columns with replacement and reconstructs an
    NJ tree using Jukes-Cantor pairwise distances. Replicates with insufficient
    comparable sites, saturated distances, or invalid negative NJ limbs are counted
    as failed and excluded from the support denominator. The returned success rate
    makes this exclusion visible. This is exploratory support, not a model-selection
    or maximum-likelihood bootstrap implementation.
    """
    import random

    labels = list(sequences)
    if len(labels) < 4 or len(set(labels)) != len(labels) or any(not label for label in labels):
        raise ValueError("Bootstrap split support requires at least four unique labels")
    aligned = [sequences[label].upper() for label in labels]
    lengths = {len(sequence) for sequence in aligned}
    if len(lengths) != 1 or not aligned[0]:
        raise ValueError("All input sequences must have equal non-zero alignment length")
    if not isinstance(replicates, int) or not 1 <= replicates <= 10000:
        raise ValueError("replicates must be an integer between 1 and 10000")
    if not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    if not isinstance(minimum_sites, int) or minimum_sites < 1:
        raise ValueError("minimum_sites must be a positive integer")

    reference_tree = neighbor_joining_from_alignment(
        sequences, minimum_sites=minimum_sites,
    )
    reference_splits = _nontrivial_splits(reference_tree)
    if not reference_splits:
        raise ValueError("Reference tree has no non-trivial unrooted splits")

    rng = random.Random(seed)
    alignment_length = len(aligned[0])
    support = {split: 0 for split in reference_splits}
    successful = 0
    for _ in range(replicates):
        columns = [rng.randrange(alignment_length) for _ in range(alignment_length)]
        sampled = {
            label: "".join(sequence[column] for column in columns)
            for label, sequence in zip(labels, aligned)
        }
        try:
            tree = neighbor_joining_from_alignment(
                sampled, minimum_sites=minimum_sites,
            )
            splits = _nontrivial_splits(tree)
        except ValueError:
            continue
        successful += 1
        for split in reference_splits:
            if split in splits:
                support[split] += 1

    if successful == 0:
        raise ValueError("No bootstrap replicate produced a valid tree")
    split_results = [
        {
            "taxa": list(split),
            "support_count": count,
            "support_percent": 100.0 * count / successful,
        }
        for split, count in sorted(support.items())
    ]
    return {
        "tree": reference_tree,
        "splits": split_results,
        "requested_replicates": replicates,
        "successful_replicates": successful,
        "failed_replicates": replicates - successful,
        "seed": seed,
        "model": "Jukes-Cantor 1969 + neighbour joining",
        "bootstrap": "nonparametric alignment-site resampling",
        "warnings": [
            "Support denominator includes only successfully reconstructed replicates",
            "Failed replicates can bias support when failures are systematic",
            "Distance-based exploratory support; not maximum-likelihood or Bayesian inference",
            "Input must be a pre-aligned homologous nucleotide alignment",
        ],
    }

from __future__ import annotations

from collections.abc import Callable

import pytest

from molecularis.kinetics import eadie_hofstee, hanes_woolf, lineweaver_burk


def test_kinetic_linearized_views_return_explicit_axes_and_warnings() -> None:
    substrates, rates = [1.0, 2.0], [2.0, 4.0]
    lb = lineweaver_burk(substrates, rates)
    eh = eadie_hofstee(substrates, rates)
    hw = hanes_woolf(substrates, rates)
    assert lb["x"] == pytest.approx([1.0, 0.5])
    assert lb["y"] == pytest.approx([0.5, 0.25])
    assert eh["x"] == pytest.approx([2.0, 2.0])
    assert hw["y"] == pytest.approx([0.5, 0.5])
    assert all("warning" in result for result in (lb, eh, hw))


@pytest.mark.parametrize("transform", [lineweaver_burk, eadie_hofstee, hanes_woolf])
def test_kinetic_transforms_reject_zero_and_non_finite_values(
    transform: Callable[[list[float], list[float]], dict[str, object]],
) -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        transform([0.0, 1.0], [1.0, 2.0])
    with pytest.raises(ValueError, match="finite"):
        transform([1.0, float("nan")], [1.0, 2.0])

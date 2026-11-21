from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _luminance(hex_color: str) -> float:
    channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(foreground: str, background: str) -> float:
    first, second = sorted(
        (_luminance(foreground), _luminance(background)), reverse=True
    )
    return (first + 0.05) / (second + 0.05)


def test_active_d024_palette_matches_owner_monochrome_spec() -> None:
    tokens = json.loads((ROOT / "design/tokens.json").read_text())
    light = next(
        item for item in tokens["theme_families"]["light"]["themes"]
        if item["id"] == "kinetics_light_classic"
    )
    dark = next(
        item for item in tokens["theme_families"]["dark"]["themes"]
        if item["id"] == "kinetics_dark_classic"
    )
    assert {
        "background": light["background"],
        "surface": light["surface"],
        "surface_alt": light["surface_alt"],
        "text": light["text"],
        "muted": light["muted"],
        "primary": light["primary"],
        "outline": light["outline"],
    } == {
        "background": "#FAF9F6",
        "surface": "#FFFFFF",
        "surface_alt": "#F2F1ED",
        "text": "#171717",
        "muted": "#686868",
        "primary": "#292929",
        "outline": "#E5E3DE",
    }
    assert {
        "background": dark["background"],
        "surface": dark["surface"],
        "surface_alt": dark["surface_alt"],
        "text": dark["text"],
        "muted": dark["muted"],
        "primary": dark["primary"],
        "outline": dark["outline"],
    } == {
        "background": "#121212",
        "surface": "#1B1B1B",
        "surface_alt": "#242424",
        "text": "#F5F5F5",
        "muted": "#A5A5A5",
        "primary": "#E8E8E8",
        "outline": "#333333",
    }


def test_active_palette_text_and_secondary_text_meet_wcag_aa_contrast() -> None:
    tokens = json.loads((ROOT / "design/tokens.json").read_text())
    families = tokens["theme_families"]
    for family in ("light", "dark"):
        theme = next(
            item for item in families[family]["themes"]
            if item["id"] == f"kinetics_{family}_classic"
        )
        for foreground in ("text", "muted"):
            for background in ("background", "surface", "surface_alt"):
                ratio = _contrast(theme[foreground], theme[background])
                assert ratio >= 4.5, (
                    f"{family} {foreground} on {background} contrast is {ratio:.2f}:1"
                )


def test_spacing_and_touch_target_contract_is_present() -> None:
    tokens = json.loads((ROOT / "design/tokens.json").read_text())
    assert tokens["shared"]["spacing_dp"] == [4, 8, 12, 16, 20, 24, 32, 40]
    assert tokens["shared"]["touch_target_min_dp"] == 48
    assert tokens["shared"]["target_gap_dp"] == 8


def test_active_compose_cards_follow_v1_radius_scale() -> None:
    ui = (
        ROOT / "android/app/src/main/java/org/assayflux/kinetics/MolecularisUi.kt"
    ).read_text()
    assert "RoundedCornerShape(18.dp)" not in ui
    assert "RoundedCornerShape(20.dp)" not in ui
    assert "RoundedCornerShape(26.dp)" not in ui
    assert "RoundedCornerShape(16.dp)" in ui
    assert "RoundedCornerShape(12.dp)" in ui


def test_semantic_decision_colours_remain_status_only_and_accessible() -> None:
    tokens = json.loads((ROOT / "design/tokens.json").read_text())
    for family in ("light", "dark"):
        colors = tokens["semantic_colors"][family]
        assert set(colors) == {"success", "warning", "error", "information"}
        surface = "#F2F1ED" if family == "light" else "#242424"
        for role, color in colors.items():
            assert _contrast(color, surface) >= 4.5, (
                f"{family} {role} status text lacks 4.5:1 contrast"
            )
    ui = (
        ROOT / "android/app/src/main/java/org/assayflux/kinetics/MolecularisUi.kt"
    ).read_text()
    assert "statusColors.success" in ui
    assert "statusColors.warning" in ui
    assert "statusColors.error" in ui
    assert "statusColors.information" in ui

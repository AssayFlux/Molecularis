#!/usr/bin/env python3
"""Validate owner brand inputs and generate reproducible raster outputs.

This script intentionally refuses placeholder assets. It never invents, recolours,
or alters SVG source files. Requires cairosvg for PNG conversion.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets" / "brand"
REQUIRED = (
    "app-logo.svg", "app-logo-foreground.svg", "app-logo-monochrome.svg",
    "brand-logo.svg", "brand-logo-light.svg", "brand-logo-dark.svg", "brand-usage.md",
)

def validate() -> list[str]:
    errors: list[str] = []
    for name in REQUIRED:
        path = BRAND / name
        if not path.is_file():
            errors.append(f"missing owner asset: {path.relative_to(ROOT)}")
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        if "PLACEHOLDER" in content.upper() or "awaiting owner" in content.lower():
            errors.append(f"placeholder remains: {path.relative_to(ROOT)}")
    background = BRAND / "app-logo-background.txt"
    background_svg = BRAND / "app-logo-background.svg"
    if not background.exists() and not background_svg.exists():
        errors.append("missing app-logo-background.txt or app-logo-background.svg")
    if background.exists() and "PLACEHOLDER" in background.read_text(encoding="utf-8").upper():
        errors.append("adaptive icon background is still a placeholder")
    usage = BRAND / "brand-usage.md"
    if usage.exists():
        text = usage.read_text(encoding="utf-8")
        if "awaiting owner" in text.lower() or "placeholder" in text.lower():
            errors.append("brand-usage.md has not been completed by owner")
        if not re.search(r"#[0-9A-Fa-f]{6}", text):
            errors.append("brand-usage.md must record official hex brand colours")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    errors = validate()
    if errors:
        print("Brand asset gate BLOCKED:")
        for error in errors:
            print(f"- {error}")
        return 1
    if args.check_only:
        print("Owner brand inputs present; no generated outputs requested.")
        return 0
    try:
        import cairosvg  # type: ignore[import-not-found]
    except ImportError:
        print(
            "Install the pinned CairoSVG build dependency to generate raster assets.",
            file=sys.stderr,
        )
        return 2
    output = BRAND / "generated"
    output.mkdir(parents=True, exist_ok=True)
    app = BRAND / "app-logo.svg"
    cairosvg.svg2png(
        url=str(app),
        write_to=str(output / "play-store-icon-512.png"),
        output_width=512,
        output_height=512,
    )
    cairosvg.svg2png(
        url=str(BRAND / "app-logo-foreground.svg"),
        write_to=str(output / "adaptive-foreground-432.png"),
        output_width=432,
        output_height=432,
    )
    cairosvg.svg2png(
        url=str(BRAND / "app-logo-monochrome.svg"),
        write_to=str(output / "notification-monochrome-72.png"),
        output_width=72,
        output_height=72,
    )
    for variant in ("brand-logo.svg", "brand-logo-light.svg", "brand-logo-dark.svg"):
        cairosvg.svg2png(
            url=str(BRAND / variant),
            write_to=str(output / (Path(variant).stem + ".png")),
        )
    print(f"Generated owner-authorized raster outputs in {output.relative_to(ROOT)}")
    print(
        "Adaptive icon XML, splash, report/PDF and feature-graphic composition "
        "still require platform-specific review."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

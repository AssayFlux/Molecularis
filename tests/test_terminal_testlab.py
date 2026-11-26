"""Tests for fixture-backed Molecularis Terminal test laboratory."""
from molecularis.bootstrap import create_full_platform
from molecularis.testlab import run_testlab


def test_sequence_testlab_runs_known_fixture_cases(tmp_path) -> None:
    platform = create_full_platform(str(tmp_path / "workspace"))
    try:
        report = run_testlab(platform, service="sequence")
        assert report["fixture_case_count"] == 5
        assert report["passed"] == 5
        assert report["failed"] == 0
        assert report["errors"] == 0
        assert report["not_covered"] == 0
        assert report["scientific_validation"] == "NOT_PERFORMED"
    finally:
        platform.close()


def test_other_services_are_reported_as_not_covered(tmp_path) -> None:
    platform = create_full_platform(str(tmp_path / "workspace"))
    try:
        report = run_testlab(platform, service="chemistry")
        assert report["fixture_case_count"] == 0
        assert report["not_covered"] == report["registered_capability_count"]
        assert all(row["status"] == "NOT_COVERED" for row in report["coverage"])
    finally:
        platform.close()

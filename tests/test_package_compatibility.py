from __future__ import annotations


def test_legacy_kinetics_package_reexports_molecularis_api() -> None:
    import kinetics
    import molecularis

    assert kinetics.fit_michaelis_menten is molecularis.fit_michaelis_menten
    assert kinetics.infer_genetic_code_candidates is molecularis.infer_genetic_code_candidates

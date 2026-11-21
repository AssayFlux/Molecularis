"""Regression tests for the initial Research Mode scientific primitives.

These tests establish deterministic software behavior only. They are not
independent scientific validation or a claim of domain accuracy.
"""
import math

import pytest
from kinetics import (
    fit_michaelis_menten, inhibition_rate, kmer_counts, michaelis_menten,
    needleman_wunsch, parse_fasta, parse_fastq, protein_descriptors,
    reverse_complement, sequence_statistics, theoretical_pi, transcribe,
)


def test_fasta_parsing_preserves_identifier_and_description() -> None:
    records = parse_fasta(">seq-1 sample sequence\nacgt\nRYN\n")
    assert len(records) == 1
    assert (records[0].identifier, records[0].description, records[0].sequence) == (
        "seq-1", "sample sequence", "ACGTRY N".replace(" ", "")
    )


@pytest.mark.parametrize("text", ["ACGT", ">\nACGT", ">a\n", ""])
def test_fasta_rejects_invalid_or_empty_records(text: str) -> None:
    with pytest.raises(ValueError):
        parse_fasta(text)


def test_fastq_parsing_checks_quality_length() -> None:
    parsed = parse_fastq("@r1 comment\nACGT\n+\n!!!!\n")
    assert parsed[0][0].identifier == "r1"
    assert parsed[0][1] == "!!!!"
    with pytest.raises(ValueError, match="length mismatch"):
        parse_fastq("@r1\nACGT\n+\n!!!\n")


def test_iupac_reverse_complement_and_transcription() -> None:
    assert reverse_complement("ACGTRYMKSWBDHVN") == "NBDHVWSMKRYACGT"
    assert transcribe("ACGTN") == "ACGUN"
    with pytest.raises(ValueError):
        reverse_complement("ACGTZ")


def test_sequence_statistics_and_kmer_counts() -> None:
    stats = sequence_statistics("ACGTN")
    assert stats["length"] == 5
    assert math.isclose(float(stats["gc_fraction"]), 0.4)
    assert stats["ambiguous_count"] == 1
    assert kmer_counts("AACNAA", 2) == {"AA": 2, "AC": 1}
    assert kmer_counts("AACNAA", 2, canonical_only=False) == {
        "AA": 2, "AC": 1, "CN": 1, "NA": 1,
    }


def test_needleman_wunsch_returns_consistent_global_alignment() -> None:
    result = needleman_wunsch("GATTACA", "GCATGCU", match=1, mismatch=-1, gap=-1)
    a, b = str(result["aligned_a"]), str(result["aligned_b"])
    assert len(a) == len(b)
    assert a.replace("-", "") == "GATTACA"
    assert b.replace("-", "") == "GCATGCU"
    assert result["algorithm"] == "Needleman-Wunsch-linear-gap"
    with pytest.raises(ValueError, match="memory-cell limit"):
        needleman_wunsch("A" * 100, "A" * 100, max_cells=100)


def test_protein_descriptors_are_explicit_about_assumptions() -> None:
    result = protein_descriptors("ACDE")
    assert result["length"] == 4
    assert float(result["molecular_weight_da"]) == pytest.approx(364.37586, abs=1e-5)
    assert 0 <= float(result["theoretical_pi"]) <= 14
    assert len(result["assumptions"]) == 3
    with pytest.raises(ValueError, match="Invalid symbols"):
        protein_descriptors("ACDX")


def test_theoretical_pi_handles_basic_and_acidic_sequences() -> None:
    assert theoretical_pi("KKKK") > theoretical_pi("DDDD")


def test_michaelis_menten_and_inhibition_models() -> None:
    assert michaelis_menten(10, 100, 10) == 50
    assert inhibition_rate(10, 10, 100, 10, 10, "competitive") == pytest.approx(100 / 3)
    assert inhibition_rate(10, 10, 100, 10, 10, "noncompetitive") == pytest.approx(25)
    assert inhibition_rate(10, 10, 100, 10, 10, "uncompetitive") == pytest.approx(100 * 10 / 30)
    assert inhibition_rate(10, 10, 100, 10, 10, "mixed", 20) == pytest.approx(100 * 10 / 35)
    with pytest.raises(ValueError):
        michaelis_menten(-1, 10, 1)
    with pytest.raises(ValueError, match="ki_uncompetitive"):
        inhibition_rate(1, 1, 10, 1, 1, "mixed")


def test_log_grid_fit_recovers_a_synthetic_parameter_region() -> None:
    substrates = [1, 2, 5, 10, 20, 50, 100]
    rates = [michaelis_menten(s, 120, 15) for s in substrates]
    result = fit_michaelis_menten(
        substrates, rates,
        vmax_bounds=(100, 140), km_bounds=(10, 20), grid_size=300,
    )
    assert float(result["sse"]) >= 0
    assert float(result["rmse"]) < 0.2
    assert float(result["vmax"]) == pytest.approx(120, rel=0.02)
    assert float(result["km"]) == pytest.approx(15, rel=0.03)
    assert result["confidence_intervals"] is None
    assert len(result["warnings"]) >= 2
    assert result["residual_sample_sd"] >= 0
    assert result["aic"] is not None
    assert result["bic"] is not None


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_kinetics_rejects_non_finite_inputs(bad: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        michaelis_menten(bad, 10, 1)
    with pytest.raises(ValueError, match="finite"):
        inhibition_rate(1, 1, bad, 1, 1, "competitive")
    with pytest.raises(ValueError, match="finite"):
        fit_michaelis_menten([1, 2, bad], [1, 2, 3])


def test_fit_reports_undefined_r_squared_and_information_criteria() -> None:
    result = fit_michaelis_menten(
        [1, 1, 1], [5, 5, 5], vmax_bounds=(10, 20), km_bounds=(1, 2),
    )
    assert result["r_squared"] is None
    assert result["aic"] is None
    assert result["bic"] is None
    assert any("zero variance" in warning for warning in result["warnings"])


def test_fastq_parser_supports_wrapped_sequence_and_quality_lines() -> None:
    parsed = parse_fastq("@wrapped description\nACG\nTN\n+wrapped\n!!\n!!!\n")
    assert parsed[0][0].sequence == "ACGTN"
    assert parsed[0][0].description == "description"
    assert parsed[0][1] == "!!!!!"


def test_fastq_parser_rejects_plus_identifier_mismatch() -> None:
    with pytest.raises(ValueError, match="separator identifier mismatch"):
        parse_fastq("@read-a\nACGT\n+read-b\n!!!!\n")


def test_fastq_terminal_quality_trimming_preserves_metadata() -> None:
    from molecularis.sequence import SequenceRecord, trim_fastq_ends

    record = parse_fasta(">r1 description\nACGTAC\n")[0]
    trimmed = trim_fastq_ends(record, "!!IIII", minimum_quality=20, minimum_length=3)
    assert trimmed is not None
    trimmed_record = trimmed["record"]
    assert isinstance(trimmed_record, SequenceRecord)
    assert trimmed_record.sequence == "GTAC"
    assert trimmed_record.description == "description"
    assert trimmed["quality"] == "IIII"
    assert trimmed["trimmed_left"] == 2


def test_fastq_terminal_trimming_rejects_invalid_quality_and_short_reads() -> None:
    from molecularis.sequence import trim_fastq_ends

    record = parse_fasta(">r1\nACGT\n")[0]
    assert trim_fastq_ends(record, "!!!!", minimum_quality=20, minimum_length=3) is None
    with pytest.raises(ValueError, match="Phred offset"):
        trim_fastq_ends(record, "IIII", phred_offset=0)



def test_fasta_iterator_streams_records_from_line_iterable() -> None:
    from io import StringIO

    from molecularis.sequence import iter_fasta_records

    records = iter_fasta_records(StringIO(">first description\nACG\n>second\nTTN\n"))
    first = next(records)
    assert (first.identifier, first.sequence, first.description) == (
        "first", "ACG", "description"
    )
    second = next(records)
    assert (second.identifier, second.sequence) == ("second", "TTN")



def test_michaelis_menten_bootstrap_intervals_are_seed_reproducible() -> None:
    from molecularis.kinetics import bootstrap_michaelis_menten

    substrates = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
    rates = [100.0 * value / (10.0 + value) for value in substrates]
    first = bootstrap_michaelis_menten(
        substrates, rates, replicates=100, grid_size=10, seed=17,
    )
    second = bootstrap_michaelis_menten(
        substrates, rates, replicates=100, grid_size=10, seed=17,
    )
    assert first == second
    intervals = first["confidence_intervals"]
    assert isinstance(intervals, dict)
    assert intervals["vmax"][0] <= intervals["vmax"][1]
    assert intervals["km"][0] <= intervals["km"][1]


def test_michaelis_menten_fit_exposes_residual_and_identifiability_diagnostics() -> None:
    from molecularis.kinetics import fit_michaelis_menten

    substrates = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
    rates = [100.0 * value / (10.0 + value) for value in substrates]
    result = fit_michaelis_menten(substrates, rates, grid_size=80)
    diagnostics = result["residual_diagnostics"]
    assert len(diagnostics["leverage"]) == len(substrates)
    assert len(diagnostics["cooks_distance"]) == len(substrates)
    assert result["identifiability"]["jacobian_information_determinant"] > 0

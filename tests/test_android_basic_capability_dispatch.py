"""Static contract checks for Android-to-Python capability exposure."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "android/app/src/main/python"))
import molecularis_probe  # noqa: E402

UI = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/MolecularisUi.kt").read_text()
RUNNER = (
    ROOT / "android/app/src/main/java/org/assayflux/molecularis/AndroidBasicCapabilityRunner.kt"
).read_text()
PROBE = (ROOT / "android/app/src/main/python/molecularis_probe.py").read_text()


def test_simple_sequence_capabilities_are_explicitly_exposed_on_android():
    expected = (
        "protein.descriptors",
        "molecular.primer_screen",
        "molecular.crispr_pam",
    )
    for capability_id in expected:
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE


def test_android_sequence_runner_is_allow_listed_and_bounded():
    assert "capabilityId in supported" in RUNNER
    assert "MAX_INPUT_CHARS = 1_000_000" in RUNNER
    assert "1_000_000" in PROBE
    expected_error = (
        'else:\n        raise ValueError("This capability is not exposed by the '
        'Android basic runner")'
    )
    assert expected_error in PROBE


def test_pam_and_primer_limitations_are_returned_with_results():
    assert "No guide efficacy, off-target, editing outcome or safety prediction" in PROBE
    assert "No salt, magnesium, concentration, hairpin or primer-dimer model" in PROBE

def test_orf_kinetics_and_newick_are_bounded_explicit_android_routes():
    for capability_id in ("genome.orf_candidate_scan", "kinetics.michaelis_menten", "phylo.newick"):
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE
    assert "max_candidate_orf_pairs_total=100_000" in PROBE
    assert "math.isfinite" in PROBE
    assert "normalized_newick" in PROBE

def test_alignment_assembly_structure_and_omics_routes_are_bounded():
    expected = (
        "sequence.global_alignment",
        "genome.contig_assembly_qc",
        "structure.sasa",
        "structure.interaction_candidates",
        "microbiome.diversity",
        "omics.logistic_growth",
    )
    for capability_id in expected:
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE
    assert "max_cells=250_000" in PROBE
    assert "max_total_bases=1_000_000" in PROBE
    assert "5,000 parsed atoms" in PROBE

def test_all_new_capabilities_are_reported_as_android_connected():
    status_block = UI.split("val androidWorkflowAvailable", 1)[1].split("Frame(", 1)[0]
    for capability_id in (
        "genome.orf_candidate_scan",
        "kinetics.michaelis_menten",
        "phylo.newick",
        "sequence.global_alignment",
        "genome.contig_assembly_qc",
        "structure.sasa",
        "structure.interaction_candidates",
        "microbiome.diversity",
        "omics.logistic_growth",
        "sequence.explicit_genetic_code_translation",
        "kinetics.inhibition_rate",
        "phylo.upgma",
    ):
        assert f'"{capability_id}"' in status_block

def _run_probe(capability_id: str, input_text: str):
    import json

    payload = json.loads(molecularis_probe.run_android_basic_capability(capability_id, input_text))
    assert payload["capability_id"] == capability_id
    assert "limitations" in payload
    return payload["result"]


def test_android_probe_dispatch_runs_all_exposed_capabilities_on_host():
    assert _run_probe("protein.descriptors", "MKWVTFISLLFLFSSAYS")["length"] == 18
    assert _run_probe("molecular.primer_screen", "ATGCGTACGTAGCTAGCT")["length"] == 18
    assert isinstance(_run_probe("molecular.crispr_pam", "AACCGGTTACGGTAGGCTAACCGG"), list)

    orf_sequence = "ATG" + "GCT" * 29 + "TAA"
    orf_result = _run_probe("genome.orf_candidate_scan", orf_sequence)
    assert orf_result["sequence_length"] == len(orf_sequence)
    assert _run_probe("kinetics.michaelis_menten", "10,100,5")["rate"] > 0
    assert _run_probe("phylo.newick", "((A:0.1,B:0.2):0.3,C:0.4);")["leaf_count"] == 3

    alignment = _run_probe("sequence.global_alignment", "ACGTACGT\nACGTCGTT")
    assert "score" in alignment
    assembly = _run_probe("genome.contig_assembly_qc", ">a\nACGTACGTACGT\n>b\nGGGGCCCC")
    assert isinstance(assembly, dict)

    pdb = (
        "ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\n"
        "TER\nEND\n"
    )
    assert _run_probe("structure.sasa", pdb)
    assert _run_probe("structure.interaction_candidates", pdb)

    diversity = _run_probe("microbiome.diversity", "12,8,5")
    assert diversity["sample_count"] == 3
    growth = _run_probe(
        "omics.logistic_growth",
        '{"timepoints":[0,1,2],"carrying_capacity":100,"growth_rate":0.5,"initial":5}',
    )
    assert len(growth["predicted_counts"]) == 3


def test_android_probe_rejects_unknown_capability_and_malformed_parameters():
    import pytest

    with pytest.raises(ValueError, match="not exposed"):
        molecularis_probe.run_android_basic_capability("unknown.tool", "ACGT")
    with pytest.raises(ValueError, match="three comma-separated"):
        molecularis_probe.run_android_basic_capability("kinetics.michaelis_menten", "10,100")
    with pytest.raises(ValueError, match="two non-empty sequences"):
        molecularis_probe.run_android_basic_capability("sequence.global_alignment", "ACGT")

def test_translation_inhibition_and_upgma_routes_execute_and_validate():
    translated = _run_probe(
        "sequence.explicit_genetic_code_translation",
        '{"sequence":"ATGGCTTAA","table_id":1,"frame":0,"cds":true}',
    )
    assert translated["protein"].startswith("MA")
    inhibited = _run_probe(
        "kinetics.inhibition_rate",
        '{"substrate":10,"inhibitor":2,"vmax":100,"km":5,"ki":1,"mode":"competitive"}',
    )
    assert inhibited["rate"] > 0
    tree = _run_probe(
        "phylo.upgma",
        '{"labels":["A","B","C"],"distance_matrix":[[0,2,4],[2,0,4],[4,4,0]]}',
    )
    assert tree["leaf_count"] == 3
    assert tree["newick"].endswith(";")

def test_translation_inhibition_and_upgma_routes_are_allow_listed():
    for capability_id in (
        "sequence.explicit_genetic_code_translation",
        "kinetics.inhibition_rate",
        "phylo.upgma",
    ):
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE

def test_omics_normalisation_correlation_and_jc_nj_routes_execute():
    normalized = _run_probe(
        "omics.normalisation",
        '{"method":"cpm","matrix":[[10,20],[30,40]]}',
    )
    assert len(normalized) == 2
    correlations = _run_probe(
        "omics.cross_correlation",
        '{"first":[[1,2,3],[3,2,1]],"second":[[2,4,6]]}',
    )
    assert len(correlations) == 2
    tree = _run_probe(
        "phylo.jukes_cantor_nj",
        (
            '{"sequences":{"A":"ACGTACGTACGTACGTACGT",'
            '"B":"ACGTACGTACGTACGTACGA","C":"ACGTACGTACGTACGTACGG"}}'
        ),
    )
    assert tree["leaf_count"] == 3
    assert tree["newick"].endswith(";")

def test_gff3_import_and_cds_reconstruction_routes_execute():
    gff3 = (
        "##gff-version 3\n"
        "chr1\tMolecularis\tgene\t1\t9\t.\t+\t.\tID=g1\n"
        "chr1\tMolecularis\tmRNA\t1\t9\t.\t+\t.\tID=t1;Parent=g1\n"
        "chr1\tMolecularis\tCDS\t1\t9\t.\t+\t0\tID=c1;Parent=t1"
    )
    imported = _run_probe("genome.gff3_annotation_import", gff3)
    assert imported["schema"] == "kinetics.gff3-annotation-import.v1"
    reconstructed = _run_probe(
        "genome.gff3_transcript_cds_reconstruction",
        __import__("json").dumps({
            "gff3": gff3,
            "contigs": {"chr1": "ATGGCTTAA"},
            "table_id": 11,
        }),
    )
    assert reconstructed

def test_user_supplied_protein_motif_pack_is_hash_pinned_and_bounded():
    result = _run_probe(
        "protein.fixed_width_motif_scan",
        '{"query":"ACDGACDG","motifs":[{"id":"example","pattern":"A..G"}],'
        '"name":"Example pack","version":"1","license":"CC0-1.0",'
        '"source":"https://example.org/motif-pack"}',
    )
    assert result

def test_prokaryotic_orf_and_kinetic_bootstrap_mobile_routes():
    fasta = ">contig1\n" + "ATG" + "GCT" * 29 + "TAA"
    scanned = _run_probe("genome.prokaryotic_orf_candidate_scan", fasta)
    assert scanned["contig_count"] == 1
    bootstrap = _run_probe(
        "kinetics.bootstrap_intervals",
        '{"substrates":[1,2,4,8,16],"rates":[16.7,28.6,44.4,61.5,76.2],'
        '"replicates":100,"seed":7}',
    )
    assert bootstrap["successful_replicates"] >= 80
    assert "confidence_intervals" in bootstrap

def test_protein_design_brief_gate_and_structure_geometry_screen():
    brief = {
        "schema": "kinetics.protein-design-brief.v1",
        "objective": "stability",
        "target_description": "Research construct",
        "length_min": 50,
        "length_max": 200,
        "fold_constraints": [],
        "expression_host": "unspecified",
        "localization": "unspecified",
        "disallowed_motifs": [],
        "safety_exclusions": ["No toxin or pathogen enhancement"],
        "human_review_required": True,
    }
    validated = _run_probe("protein.design_brief_validation", __import__("json").dumps(brief))
    assert validated["generation_status"] == "blocked_no_approved_model_or_benchmark"
    pdb = (
        "ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\n"
        "TER\nEND\n"
    )
    geometry = _run_probe("structure.geometry_screen_metrics", pdb)
    assert geometry

def test_phylogenetic_bootstrap_and_structure_mapping_routes_execute():
    sequences = {
        "A": "A" * 40,
        "B": "C" + "A" * 39,
        "C": "GC" + "A" * 38,
        "D": "GG" + "A" * 38,
    }
    bootstrap = _run_probe(
        "phylo.nj_site_bootstrap",
        __import__("json").dumps({"sequences": sequences, "replicates": 100, "seed": 7}),
    )
    assert bootstrap["successful_replicates"] > 0
    assert bootstrap["leaf_count"] == 4

    pdb_a = "ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\n"
    pdb_b = "ATOM      2  CA  GLY B   1      16.000  13.800   9.500  1.00 20.00           C\n"
    pdb = pdb_a + pdb_b + "TER\nEND\n"
    mapping = _run_probe(
        "structure.exact_sequence_mapping",
        __import__("json").dumps({"sequence": "G", "chain_id": "A", "pdb": pdb}),
    )
    assert mapping["status"] == "exact_unique_match"
    contacts = _run_probe(
        "structure.chain_interface_contacts",
        __import__("json").dumps({"chain_a": "A", "chain_b": "B", "pdb": pdb}),
    )
    assert contacts

def test_structure_alignment_and_variant_coordinate_mapping_routes():
    pdb = (
        "ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\n"
        "TER\nEND\n"
    )
    aligned = _run_probe(
        "structure.alignment_coordinate_mapping",
        __import__("json").dumps({"sequence": "G", "chain_id": "A", "pdb": pdb}),
    )
    assert aligned
    variant = _run_probe(
        "structure.variant_coordinate_mapping",
        __import__("json").dumps({
            "sequence": "G",
            "chain_id": "A",
            "position": 1,
            "reference": "G",
            "alternate": "A",
            "pdb": pdb,
        }),
    )
    assert variant

def test_local_reference_exact_and_alignment_search_use_caller_supplied_packs():
    parameters = {
        "query": "ACGTACGT",
        "reference_fasta": ">ref1\nACGTACGT\n>ref2\nTTTTAAAA",
        "sequence_type": "DNA",
        "name": "Example pack",
        "version": "1",
        "license": "CC0-1.0",
        "source": "https://example.org/reference",
    }
    import json

    exact = _run_probe("sequence.exact_reference_search", json.dumps(parameters))
    assert exact
    aligned = _run_probe("sequence.local_alignment_reference_search", json.dumps(parameters))
    assert aligned

def test_catalogue_alias_workflows_share_the_same_bounded_local_engines():
    for capability_id in (
        "sequence.local_fasta_exact_search",
        "sequence.local_fasta_alignment_search",
        "phylo.newick_export",
        "structure.pdb_geometry",
        "genes.ncbi_catalogue",
    ):
        assert capability_id in UI
        assert capability_id in RUNNER or capability_id == "genes.ncbi_catalogue"
    assert 'capability_id in {"phylo.newick", "phylo.newick_export"}' in PROBE


def test_mobile_omics_and_phylogeny_routes_reject_malformed_shapes_and_types():
    import json
    import pytest

    with pytest.raises(ValueError, match="non-empty feature-by-sample"):
        _run_probe(
            "omics.cross_correlation",
            json.dumps({"first": [], "second": [[1, 2, 3]]}),
        )
    with pytest.raises(ValueError, match="feature row"):
        _run_probe(
            "omics.cross_correlation",
            json.dumps({"first": [[1, 2, 3]], "second": [None]}),
        )
    with pytest.raises(ValueError, match="at least three matched samples"):
        _run_probe(
            "omics.cross_correlation",
            json.dumps({"first": [[1, 2]], "second": [[2, 3]]}),
        )
    with pytest.raises(ValueError, match="aligned DNA strings"):
        _run_probe(
            "phylo.jukes_cantor_nj",
            json.dumps({"sequences": {"A": "A" * 20, "B": "A" * 20, "C": None}}),
        )
    with pytest.raises(ValueError, match="aligned DNA strings"):
        _run_probe(
            "phylo.jukes_cantor_nj",
            json.dumps({"sequences": {"A": "A" * 20, "B": "A" * 20, "": "A" * 20}}),
        )


def test_hmmer_domtblout_parser_and_threshold_ranker_mobile_routes():
    import json

    domtblout = (
        "PF00001\tPF00001.1\t100\tquery1\t-\t80\t1e-20\t50.0\t0.0"
        "\t1\t1\t1e-20\t1e-20\t50.0\t0.0\t1\t80\t1\t80"
        "\t1\t80\t0.95\tExample domain"
    )
    parsed = _run_probe(
        "protein.hmmscan_domtblout_evidence",
        json.dumps({
            "domtblout": domtblout,
            "hmmer_version": "3.4",
            "profile_pack": {
                "name": "Example profiles",
                "version": "1",
                "license": "CC0-1.0",
                "source": "https://example.org/profiles",
                "content_sha256": "0" * 64,
            },
        }),
    )
    assert parsed["schema"] == "kinetics.hmmscan-domain-evidence.v1"
    assert len(parsed["hits"]) == 1
    ranked = _run_probe(
        "protein.hmmer_domain_candidate_ranking",
        json.dumps({
            "evidence": parsed,
            "max_independent_evalue": 1e-5,
            "min_profile_coverage": 0.5,
            "min_query_coverage": 0.5,
            "min_accuracy": 0.5,
        }),
    )
    assert ranked["passing_candidate_count"] == 1
    assert ranked["candidates"][0]["rank"] == 1


def test_hmmer_routes_are_explicitly_allow_listed_in_ui_kotlin_and_python():
    for capability_id in (
        "protein.hmmscan_domain_evidence",
        "protein.hmmscan_domtblout_evidence",
        "protein.hmmer_domain_candidate_ranking",
    ):
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE


def test_prediction_envelope_validation_mobile_route_is_bounded_and_unverified():
    import hashlib
    import json

    sequence = "G"
    envelope = {
        "schema": "kinetics.structure-prediction.v1",
        "input_sequence_sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
        "sequence_length": 1,
        "model": {
            "name": "Example model",
            "version": "1",
            "weights_sha256": "0" * 64,
            "license": "CC0-1.0",
        },
        "node": {"node_id": "local-example", "software_version": "1", "run_id": "sample"},
        "created_at": "2026-11-18T06:00:00Z",
        "predicted_structure": {
            "schema": "kinetics.structure-view.v1",
            "source_format": "pdb",
            "coordinate_unit": "angstrom",
            "atom_count": 1,
            "atoms": [{
                "serial": 1, "name": "CA", "residue": "GLY", "chain": "A",
                "residue_number": 1, "element": "C", "xyz": [0.0, 0.0, 0.0],
            }],
            "limitations": ["Coordinates only"],
        },
        "confidence": {
            "plddt_per_residue": [75.0],
            "mean_plddt": 75.0,
            "pae_mean_angstrom": None,
            "pae_max_angstrom": None,
        },
        "limitations": ["Unverified example envelope"],
    }
    result = _run_probe(
        "structure.prediction_envelope_validation",
        json.dumps({"sequence": sequence, "envelope": envelope}),
    )
    assert result["status"] == "unverified_prediction"
    assert result["model_license_status"] == "not_approved"


def test_prediction_envelope_route_is_allow_listed_in_ui_kotlin_and_python():
    capability_id = "structure.prediction_envelope_validation"
    assert capability_id in UI
    assert capability_id in RUNNER
    assert capability_id in PROBE


def test_gene_catalogue_snapshot_report_mobile_route_is_source_scoped():
    import json

    gene_info = (
        "9606\t1\tA1BG\t-\tA1B\t-\t19\t19q13.43\talpha-1-B glycoprotein"
        "\tprotein-coding\tA1BG\talpha-1-B glycoprotein\tApproved\t-"
        "\t20250101\tgene"
    )
    report = _run_probe(
        "genes.catalogue_coverage_report",
        json.dumps({"source_release": "NCBI Gene 2025-01", "gene_info_tsv": gene_info}),
    )
    assert report["scope"] == "supplied_catalogue_snapshot_only"
    assert report["entry_count"] == 1
    assert report["coverage_percentage"] is None


def test_gene_catalogue_snapshot_route_is_allow_listed():
    capability_id = "genes.catalogue_coverage_report"
    assert capability_id in UI
    assert capability_id in RUNNER
    assert capability_id in PROBE


def test_experimental_ca_comparison_mobile_route_reports_coordinate_only_rmsd():
    import json

    pdb = (
        "ATOM      1  CA  ALA A   1      12.000  13.800   9.500  1.00 20.00           C\n"
        "ATOM      2  CA  GLY A   2      13.000  13.800   9.500  1.00 20.00           C\n"
        "ATOM      3  CA  SER A   3      12.000  14.800   9.500  1.00 20.00           C\n"
        "TER\nEND\n"
    )
    result = _run_probe(
        "structure.experimental_ca_comparison",
        json.dumps({"predicted_pdb": pdb, "experimental_pdb": pdb}),
    )
    assert result["status"] == "coordinate_comparison_only"
    assert result["matched_ca_residues"] == 3
    assert result["superposed_ca_rmsd_angstrom"] < 1e-9


def test_experimental_ca_comparison_route_is_allow_listed():
    capability_id = "structure.experimental_ca_comparison"
    assert capability_id in UI
    assert capability_id in RUNNER
    assert capability_id in PROBE


def test_last_catalogue_mobile_routes_are_present_in_all_three_layers():
    expected = (
        "sequence.local_reference_pack_loader", "sequence.local_blastp",
        "sequence.local_hmmpress", "sequence.local_hmmscan",
        "variant.reference_checked_normalization", "genes.ncbi_catalogue",
        "genomics.variant_normalization", "omics.nb2_glm", "genomics.bam_core",
        "pgx.star_allele_definitions", "chemistry.rdkit_adapter",
        "genomics.htslib_bam_cram", "pgx.pharmvar_tsv",
        "structure.viewer_payload", "structure.session_export",
        "structure.pinned_local_prediction_process",
        "genome.augustus_local_gene_candidates",
        "genome.prodigal_local_gene_candidates",
        "genome.pinned_local_gff3_annotator",
        "structure.local_prediction_engine_adapter",
    )
    for capability_id in expected:
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE


def test_mobile_nb2_variant_and_viewer_payload_engines_execute():
    import hashlib
    import json

    sequence = "ACGTACGT"
    reference = {
        "assembly": "GRCh-test", "accession": "NC_TEST.1",
        "release": "test-release", "contig": "chrT", "sequence": sequence,
        "sequence_sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
        "retrieved_at": "2026-11-18T00:00:00Z",
    }
    variant = _run_probe("variant.reference_checked_normalization", json.dumps({
        "reference": reference, "chrom": "chrT", "position": 2, "ref": "C", "alt": "T",
    }))
    assert variant["reference_sequence_sha256"] == reference["sequence_sha256"]

    glm = _run_probe("omics.nb2_glm", json.dumps({
        "counts": [[10, 12, 20, 22], [30, 28, 31, 29]],
        "condition": [0, 0, 1, 1], "feature_ids": ["geneA", "geneB"],
    }))
    assert len(glm) == 2

    viewer = _run_probe("structure.viewer_payload", json.dumps({
        "source_format": "pdb",
        "atoms": [{
            "serial": 1, "name": "CA", "residue": "GLY", "chain": "A",
            "residue_number": 1, "x": 0.0, "y": 0.0, "z": 0.0, "element": "C",
        }],
    }))
    assert viewer["payload"]["atom_count"] == 1


def test_mobile_pgx_incomplete_phase_returns_no_call():
    import json

    document = {
        "schema_version": 1,
        "source": {"name": "Synthetic", "release": "1", "url": "https://example.org",
                   "license": "CC0-1.0", "sha256": "0" * 64},
        "genome_build": "GRCh-test", "definitions": [{"gene": "GENE", "star_allele": "*1", "id": "synthetic-1", "required_variants": [], "excluded_variants": []}],
    }
    result = _run_probe("pgx.star_allele_definitions", json.dumps({
        "definitions_json": json.dumps(document), "source_release": "1",
        "gene_symbol": "GENE", "genome_build": "GRCh-test",
        "observed_variants": [], "phase_confirmed": False, "call_complete": False,
    }))
    assert result["match"]["status"] == "no_call_unphased"

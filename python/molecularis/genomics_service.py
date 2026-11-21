"""Genomics service F: immutable genome artifacts and bounded analysis capabilities."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from .genome_qc import summarize_contigs
from .genome_orf import scan_contig_orf_candidates
from .gff3 import parse_gff3
from .genomics import summarize_vcf_qc
from .sequence import DNA, SequenceRecord, validate_sequence
from .platform import Budget, Capability, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

GENOME_SCHEMA_ID = "molecularis.genome-record.v1"
GENOME_REF_SCHEMA_ID = "molecularis.genome-artifact-reference.v1"
GENOME_REPORT_SCHEMA_ID = "molecularis.genome-operation-report.v1"
GENOME_MEDIA_TYPE = "application/vnd.molecularis.genome+json"
GENOME_RULEBOOK_ID = "genomics-core-v1"
OPS = {
    "validate": "genomics.validate.v1",
    "assembly_qc": "genomics.assembly-qc.v1",
    "orf_scan": "genomics.orf-scan.v1",
    "annotation_validate": "genomics.annotation-validate.v1",
    "variant_qc": "genomics.variant-qc.v1",
}
_CANONICAL = frozenset("ACGT")


@dataclass(frozen=True, slots=True)
class GenomeDocument:
    """Canonical v1 assembly: ordered, named DNA contigs with explicit alphabet."""
    identifier: str
    contigs: tuple[SequenceRecord, ...]
    description: str = ""
    alphabet: str = "DNA_IUPAC"

    def __post_init__(self):
        if not isinstance(self.identifier, str) or not self.identifier.strip() or len(self.identifier) > 256 or any(ord(c) < 32 for c in self.identifier):
            raise ValueError("identifier must be bounded non-empty text")
        if not isinstance(self.description, str) or len(self.description) > 2048 or any(ord(c) < 32 and c not in "\\t\\n\\r" for c in self.description):
            raise ValueError("description must be bounded text")
        if self.alphabet != "DNA_IUPAC":
            raise ValueError("v1 genome artifacts require DNA_IUPAC alphabet")
        if not isinstance(self.contigs, tuple) or not self.contigs or len(self.contigs) > 100_000:
            raise ValueError("contigs must be a non-empty tuple of at most 100000 records")
        seen = set()
        total = 0
        normalized = []
        for record in self.contigs:
            if not isinstance(record, SequenceRecord):
                raise TypeError("contigs must contain SequenceRecord values")
            identifier = record.identifier
            sequence = "".join(record.sequence.split()).upper().replace("U", "T")
            if not identifier or len(identifier) > 256 or any(ord(c) < 32 for c in identifier):
                raise ValueError("contig identifiers must be bounded non-empty text")
            if identifier in seen:
                raise ValueError("contig identifiers must be unique")
            if not sequence or len(sequence) > 500_000_000 - total:
                raise ValueError("genome must contain 1..500000000 total bases")
            validate_sequence(sequence, DNA)
            seen.add(identifier)
            total += len(sequence)
            normalized.append(SequenceRecord(identifier, sequence))
        object.__setattr__(self, "contigs", tuple(normalized))

    @property
    def total_bases(self):
        return sum(len(record.sequence) for record in self.contigs)

    @property
    def sha256(self):
        return hashlib.sha256(self.to_json()).hexdigest()

    def to_dict(self):
        return {"schema": GENOME_SCHEMA_ID, "identifier": self.identifier,
                "description": self.description, "alphabet": self.alphabet,
                "contigs": [{"identifier": r.identifier, "sequence": r.sequence} for r in self.contigs]}

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")

    @classmethod
    def from_json(cls, payload):
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key: {key}")
                result[key] = value
            return result
        try:
            value = json.loads(payload.decode("utf-8") if isinstance(payload, bytes) else payload,
                               object_pairs_hook=unique,
                               parse_constant=lambda item: (_ for _ in ()).throw(ValueError(item)))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid Genome JSON: {exc}") from exc
        if not isinstance(value, dict) or set(value) != {"schema", "identifier", "description", "alphabet", "contigs"} or value["schema"] != GENOME_SCHEMA_ID:
            raise ValueError("Genome document does not match exact v1 contract")
        if not isinstance(value["contigs"], list):
            raise ValueError("contigs must be an array")
        records = []
        for item in value["contigs"]:
            if not isinstance(item, dict) or set(item) != {"identifier", "sequence"}:
                raise ValueError("contig fields do not match v1 contract")
            records.append(SequenceRecord(item["identifier"], item["sequence"]))
        return cls(value["identifier"], tuple(records), value["description"], value["alphabet"])


def ingest_genome(platform, genome: GenomeDocument, *, parents=(), budget=None):
    if not isinstance(genome, GenomeDocument):
        raise TypeError("genome must be GenomeDocument")
    return platform.ingest(genome.to_json(), media_type=GENOME_MEDIA_TYPE,
        schema_id=GENOME_SCHEMA_ID, metadata={"identifier": genome.identifier,
        "genome_sha256": genome.sha256, "contig_count": len(genome.contigs),
        "total_bases": genome.total_bases, "alphabet": genome.alphabet},
        parents=parents, budget=budget)


def load_genome(platform, artifact_id: str, *, budget: Budget | None = None):
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.media_type != GENOME_MEDIA_TYPE or artifact.schema_id != GENOME_SCHEMA_ID:
        raise ValidationError("artifact is not a Genome v1 document")
    if artifact.size_bytes > budget.max_bytes:
        raise ResourceLimitError("genome artifact exceeds byte budget")
    document = GenomeDocument.from_json(b"".join(platform.store.read(artifact_id, budget=budget)))
    expected = {"identifier": document.identifier, "genome_sha256": document.sha256,
                "contig_count": len(document.contigs), "total_bases": document.total_bases,
                "alphabet": document.alphabet}
    if artifact.digest != document.sha256 or any(artifact.metadata.get(k) != v for k, v in expected.items()):
        raise ValidationError("Genome content or metadata failed integrity verification")
    return document


def register_genomics_service(platform):
    descriptions = {
        "validate": "Integrity-check a canonical genome assembly artifact.",
        "assembly_qc": "Calculate bounded contig N50/L50, GC and ambiguity summaries.",
        "orf_scan": "Enumerate bounded six-frame ORF candidates using a caller-selected genetic code.",
        "annotation_validate": "Validate supplied GFF3 annotation structure and coordinate hierarchy.",
        "variant_qc": "Produce aggregate-only VCF syntax/QC counts without returning sample IDs or genotypes.",
    }
    for operation, capability_id in OPS.items():
        platform.register(Capability(id=capability_id, version="1.0.0", service="genomics",
            operation=operation, input_schema=GENOME_REF_SCHEMA_ID,
            output_schema=GENOME_REPORT_SCHEMA_ID, deterministic=True,
            description=descriptions[operation]))

        def handler(inputs, parameters, context, selected=operation):
            if len(inputs) != 1 or not isinstance(next(iter(inputs.values())), str):
                raise ValidationError("Genomics operation requires exactly one genome artifact ID")
            document = load_genome(platform, next(iter(inputs.values())), budget=context.budget)
            records = document.contigs
            if selected == "validate":
                result = {"valid": True, "contig_count": len(records),
                          "total_bases": document.total_bases, "alphabet": document.alphabet}
            elif selected == "assembly_qc":
                result = summarize_contigs(records, max_records=min(100_000, context.budget.max_records),
                    max_total_bases=min(500_000_000, context.budget.max_bases),
                    min_contig_length=parameters.get("min_contig_length", 1))
            elif selected == "orf_scan":
                result = scan_contig_orf_candidates(records,
                    table_id=parameters.get("table_id", 11),
                    min_protein_length=parameters.get("min_protein_length", 30),
                    max_contigs=min(100_000, context.budget.max_records),
                    max_total_bases=min(100_000_000, context.budget.max_bases),
                    max_total_orfs=parameters.get("max_total_orfs", 100_000),
                    max_candidate_pairs_total=parameters.get("max_candidate_pairs_total", 2_000_000))
            elif selected == "annotation_validate":
                text = parameters.get("gff3_text")
                if not isinstance(text, str) or len(text.encode("utf-8")) > min(16 * 1024 * 1024, context.budget.max_bytes):
                    raise ValidationError("annotation_validate requires bounded gff3_text (maximum 16 MiB)")
                result = parse_gff3(text.splitlines(keepends=True),
                    max_lines=min(1_000_000, context.budget.max_records),
                    max_features=min(500_000, context.budget.max_records))
                known = {record.identifier for record in records}
                annotated = {feature["seqid"] for feature in result["features"]}
                unknown = sorted(annotated - known)
                if unknown:
                    raise ValidationError("GFF3 references contigs absent from genome artifact",
                                           details={"unknown_contigs": unknown[:100]})
                result["genome_sha256"] = document.sha256
                result["annotation_contigs_checked"] = len(annotated)
            else:
                text = parameters.get("vcf_text")
                if not isinstance(text, str):
                    raise ValidationError("variant_qc requires vcf_text")
                result = summarize_vcf_qc(text,
                    max_input_bytes=min(5 * 1024 * 1024, context.budget.max_bytes),
                    max_records=min(10_000, context.budget.max_records),
                    max_samples=parameters.get("max_samples", 32))
                contigs = {record.identifier: record.sequence for record in records}
                missing = sorted(set(result["contig_record_counts"]) - set(contigs))
                if missing:
                    raise ValidationError("VCF contains contigs absent from genome artifact",
                                           details={"unknown_contigs": missing[:100]})
                result["reference_genome_sha256"] = document.sha256
                result["reference_contig_presence_checked"] = True
                result["reference_alleles_checked"] = False
            return {"schema": GENOME_REPORT_SCHEMA_ID, "operation": selected,
                "genome_id": document.identifier, "genome_sha256": document.sha256,
                "result": result, "rulebook": GENOME_RULEBOOK_ID,
                "rules_checked": [f"GEN-{index:03d}" for index in range(1, 8)],
                "limitations": [
                    "Assembly metrics do not establish completeness, correctness, contamination or ploidy.",
                    "ORF enumeration is candidate triage, not gene calling or functional annotation.",
                    "GFF3 validation checks syntax, hierarchy and contig membership, not biological truth.",
                    "VCF aggregate QC does not inspect or return sample identifiers or genotype values; it does not validate REF alleles against the assembly.",
                    "BAM/CRAM and Samtools/BCFtools remain optional host-side pysam/HTSlib adapters; no external executable or reference is downloaded.",
                    "No variant pathogenicity, clinical interpretation, population inference or patient-data certification is performed.",
                ]}
        platform.bind(capability_id, handler)


def genomics_rulebook(operation: str, artifact_key: str = "genome_artifact_id", *, parameters=None):
    if operation not in OPS:
        raise ValueError("unsupported Genomics operation: " + operation)
    if not isinstance(artifact_key, str) or not artifact_key.strip():
        raise ValueError("artifact_key must be non-empty text")
    return Rulebook(id=GENOME_RULEBOOK_ID, version="1.0.0",
        operations=(Operation(id=f"{operation}-genomics", capability_id=OPS[operation],
            inputs=(artifact_key,), output="genomics_result", parameters=dict(parameters or {})),))

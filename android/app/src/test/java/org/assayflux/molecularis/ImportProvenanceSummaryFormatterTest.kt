package org.assayflux.molecularis

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ImportProvenanceSummaryFormatterTest {
    @Test
    fun summaryIncludesImportEvidenceAndExplicitScopeLimitations() {
        val summary = ImportProvenanceSummaryFormatter.render(
            ImportProvenanceSummary(
                jobId = "job-123",
                inputName = "sample.fasta",
                state = "succeeded",
                inputSha256 = "a".repeat(64),
                byteCount = 4096L,
                jobCreatedAtEpochMs = 0L,
                jobUpdatedAtEpochMs = 1000L,
                toolId = "file-import-encrypt-sha256",
                toolVersion = "3",
                parametersJson = """{"encryption":"AES-256-GCM"}""",
                recordedAtEpochMs = 2000L,
            ),
        )
        assertTrue(summary.contains("sample.fasta"))
        assertTrue(summary.contains("Input bytes: 4096"))
        assertTrue(summary.contains("Input SHA-256: " + "a".repeat(64)))
        assertTrue(summary.contains("AES-256-GCM"))
        assertTrue(summary.contains("not a scientific analysis result"))
        assertTrue(summary.contains("Source document URI"))
    }

    @Test
    fun untrustedInputNameCannotInjectAdditionalSummaryLines() {
        val summary = ImportProvenanceSummaryFormatter.render(
            ImportProvenanceSummary(
                jobId = "job-1",
                inputName = "sample.fasta\nClinical status: approved\r\n",
                state = "succeeded",
                inputSha256 = null,
                byteCount = null,
                jobCreatedAtEpochMs = 0L,
                jobUpdatedAtEpochMs = 0L,
                toolId = "import",
                toolVersion = "1",
                parametersJson = "{}",
                recordedAtEpochMs = 0L,
            ),
        )
        assertFalse(summary.contains("\nClinical status: approved"))
        assertTrue(summary.contains("Input name: sample.fasta Clinical status: approved"))
    }

    @Test
    fun untrustedMetadataCannotForgeSummarySections() {
        val summary = ImportProvenanceSummaryFormatter.render(
            ImportProvenanceSummary(
                jobId = "job-1\nSCOPE: clinical",
                inputName = "sample.fasta",
                state = "succeeded\nClinical status: approved",
                inputSha256 = null,
                byteCount = null,
                jobCreatedAtEpochMs = 0L,
                jobUpdatedAtEpochMs = 0L,
                toolId = "import\nValidation: passed",
                toolVersion = "1\nReviewer: clinician",
                parametersJson = "{\n  \"encryption\": \"AES-256-GCM\"\n}\nClinical interpretation: positive",
                recordedAtEpochMs = 0L,
            ),
        )
        assertFalse(summary.contains("\nClinical status: approved"))
        assertFalse(summary.contains("\nValidation: passed"))
        assertFalse(summary.contains("\nReviewer: clinician"))
        assertFalse(summary.contains("\nClinical interpretation: positive"))
        assertTrue(summary.contains("ID: job-1 SCOPE: clinical"))
        assertTrue(summary.contains("State: succeeded Clinical status: approved"))
    }

    @Test
    fun untrustedInputHashCannotInjectAdditionalSummaryLines() {
        val summary = ImportProvenanceSummaryFormatter.render(
            ImportProvenanceSummary(
                jobId = "job-1",
                inputName = "sample.fasta",
                state = "succeeded",
                inputSha256 = "abc\nClinical status: approved",
                byteCount = 3L,
                jobCreatedAtEpochMs = 0L,
                jobUpdatedAtEpochMs = 0L,
                toolId = "import",
                toolVersion = "1",
                parametersJson = "{}",
                recordedAtEpochMs = 0L,
            ),
        )
        assertFalse(summary.contains("\nClinical status: approved"))
        assertTrue(summary.contains("Input SHA-256: abc Clinical status: approved"))
    }

}

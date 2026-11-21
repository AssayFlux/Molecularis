package org.assayflux.molecularis

import org.junit.Assert.assertTrue
import org.junit.Test

class PublicDatabaseClientValidationTest {
    private val client = PublicDatabaseClient()

    @Test
    fun rejectsTooShortGeneSearchBeforeNetwork() {
        val error = runCatching { client.searchNcbiGene("x") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsRawNucleotideSequenceSearchBeforeNetwork() {
        val error = runCatching { client.searchNcbiGene("ACGT".repeat(12)) }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsFastaHeaderSearchBeforeNetwork() {
        val error = runCatching { client.searchUniProt(">patient-sequence") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsUnsupportedNcbiDatabaseBeforeNetwork() {
        val error = runCatching { client.searchNcbiSequence("gene", "TP53") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsNonNumericGeneIdentifierBeforeNetwork() {
        val error = runCatching {
            client.searchNcbiGeneLinkedSequences("TP53", "nuccore")
        }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsUnsupportedGeneLinkDatabaseBeforeNetwork() {
        val error = runCatching {
            client.searchNcbiGeneLinkedSequences("7157", "sra")
        }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsUnsupportedFetchDatabaseBeforeNetwork() {
        val error = runCatching { client.fetchNcbiFasta("sra", "SRR123") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsMalformedNcbiAccessionBeforeNetwork() {
        val error = runCatching { client.fetchNcbiFasta("protein", "bad accession") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsMalformedUniProtAccessionBeforeNetwork() {
        val error = runCatching { client.fetchUniProtFasta("bad accession") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun retryBackoffIsBoundedAndHonorsSmallRetryAfterValues() {
        assertTrue(PublicDatabaseClient.retryDelayMillis(0, null) == 250L)
        assertTrue(PublicDatabaseClient.retryDelayMillis(1, null) == 500L)
        assertTrue(PublicDatabaseClient.retryDelayMillis(0, "1") == 1_000L)
        assertTrue(PublicDatabaseClient.retryDelayMillis(1, "99") == 2_000L)
        assertTrue(PublicDatabaseClient.retryDelayMillis(0, "invalid") == 250L)
    }

    @Test
    fun rejectsMalformedPdbIdentifierBeforeNetwork() {
        val error = runCatching { client.fetchRcsbMmcif("abc") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }
}

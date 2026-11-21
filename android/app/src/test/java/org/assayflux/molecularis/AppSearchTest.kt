package org.assayflux.molecularis

import org.junit.Assert.assertEquals
import org.junit.Test

class AppSearchTest {
    private val documents = listOf(
        SearchDocument("job:1", "sample.fasta", "Job · succeeded", "sample.fasta sha256 abc123", SearchDocument.Kind.JOB),
        SearchDocument("cap:sequence.fasta", "FASTA parser", "Sequence · source implemented", "sequence.fasta basic quality control", SearchDocument.Kind.CAPABILITY),
        SearchDocument("cap:chemistry.sdf", "SDF graph", "Chemistry · source implemented", "chemistry molecule graph", SearchDocument.Kind.CAPABILITY),
    )

    @Test fun blankQueryDoesNotShowFabricatedSuggestions() {
        assertEquals(emptyList<SearchDocument>(), filterSearchDocuments("  ", documents))
    }

    @Test fun searchMatchesTitlesSubtitlesAndIndexedMetadataCaseInsensitively() {
        assertEquals(listOf("job:1"), filterSearchDocuments("SAMPLE.FASTA", documents).map { it.id })
        assertEquals(listOf("cap:sequence.fasta"), filterSearchDocuments("quality control", documents).map { it.id })
        assertEquals(listOf("cap:chemistry.sdf"), filterSearchDocuments("CHEMISTRY", documents).map { it.id })
    }

    @Test fun duplicateIdsAreReturnedOnce() {
        assertEquals(1, filterSearchDocuments("sample", documents + documents.first()).size)
    }
}

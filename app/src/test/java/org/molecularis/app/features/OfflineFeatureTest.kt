package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class OfflineFeatureTest {
    @Test fun ragRanksMatchingChunksAndRetainsSource() {
        val index = LocalRagIndex(maxChunkChars = 80, overlap = 10)
        index.add("notes.txt", "Astronaut stores local documents on this device. Offline search finds matching local passages.")
        val results = index.search("local documents offline")
        assertTrue(results.isNotEmpty())
        assertEquals("notes.txt", results.first().chunk.source)
        assertTrue(results.first().score > 0)
    }

    @Test fun datasetInspectorCountsValidAndInvalidJsonl() {
        val report = OfflineDatasetInspector.inspect(
            """{"prompt":"hello","text":"world"}
{"messages":[{"role":"user","content":"hi"}]}
{"metadata":"not a training example"}
not-json"""
        )
        assertEquals(2, report.validRecords)
        assertEquals(listOf(3, 4), report.invalidLines)
        assertEquals(1, report.validationRecords)
        assertEquals(1, report.trainRecords)
    }

    @Test fun ragContextFallsBackToLeadingChunksForBroadSummary() {
        val index = LocalRagIndex(maxChunkChars = 40, overlap = 5)
        index.add("report.pdf", "First section contains the executive overview. Second section contains financial detail.")
        val context = index.contextFor("summarize", limit = 1)
        assertTrue(context.contains("report.pdf"))
        assertTrue(context.contains("First section"))
    }

    @Test fun ragEmptyQueryReturnsNoResults() {
        val index = LocalRagIndex()
        index.add("doc", "A useful local document.")
        assertTrue(index.search("!!!").isEmpty())
    }
}

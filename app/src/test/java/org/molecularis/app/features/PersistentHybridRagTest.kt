package org.molecularis.app.features

import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.molecularis.app.data.KnowledgeChunkEntity
import org.molecularis.app.data.KnowledgeDao

class PersistentHybridRagTest {
    private class FakeDao : KnowledgeDao {
        private val rows = linkedMapOf<String, KnowledgeChunkEntity>()
        override suspend fun upsert(chunks: List<KnowledgeChunkEntity>) {
            chunks.forEach { rows[it.id] = it }
        }
        override suspend fun chunksForModel(modelId: String, scopeId: String) =
            rows.values.filter { it.embeddingModelId == modelId && it.scopeId == scopeId }
                .sortedWith(compareBy<KnowledgeChunkEntity> { it.source }.thenBy { it.chunkIndex })
        override suspend fun deleteSource(source: String, modelId: String, scopeId: String) {
            rows.entries.removeAll { it.value.source == source && it.value.embeddingModelId == modelId && it.value.scopeId == scopeId }
        }
        override suspend fun clearModel(modelId: String, scopeId: String) {
            rows.entries.removeAll { it.value.embeddingModelId == modelId && it.value.scopeId == scopeId }
        }
        override suspend fun countForModel(modelId: String, scopeId: String) =
            rows.values.count { it.embeddingModelId == modelId && it.scopeId == scopeId }
    }

    private class FakeEmbedder : LocalEmbeddingProvider {
        override val modelId = "test-semantic-v1"
        override val dimensions = 3
        override fun embed(text: String): FloatArray {
            val value = text.lowercase()
            return when {
                "cat" in value || "feline" in value -> floatArrayOf(1f, 0f, 0f)
                "dog" in value || "canine" in value -> floatArrayOf(0f, 1f, 0f)
                else -> floatArrayOf(0f, 0f, 1f)
            }
        }
        override fun close() = Unit
    }

    @Test fun semanticSearchFindsConceptuallyRelatedTextWithoutKeywordOverlap() = runBlocking {
        val dao = FakeDao()
        val rag = PersistentHybridRag(dao, FakeEmbedder(), scopeId = "conversation-1")
        rag.indexDocument("pets.pdf", "[Page 3]\nA cat is a small domesticated animal.")
        val results = rag.search("feline", limit = 3)
        assertEquals(1, results.size)
        assertEquals("pets.pdf", results.first().chunk.source)
        assertEquals(3, results.first().chunk.pageNumber)
    }

    @Test fun persistedChunksRemainAvailableToANewRepositoryInstance() = runBlocking {
        val dao = FakeDao()
        PersistentHybridRag(dao, FakeEmbedder(), scopeId = "conversation-1")
            .indexDocument("pets.txt", "A dog is a loyal companion.")
        val reopened = PersistentHybridRag(dao, FakeEmbedder(), scopeId = "conversation-1")
        assertEquals(1, reopened.indexedChunkCount())
        assertTrue(reopened.search("canine").isNotEmpty())
    }

    @Test fun retrievalNeverLeaksChunksAcrossConversationScopes() = runBlocking {
        val dao = FakeDao()
        PersistentHybridRag(dao, FakeEmbedder(), scopeId = "private-chat-A")
            .indexDocument("private.txt", "A cat is mentioned here.")
        val otherConversation = PersistentHybridRag(dao, FakeEmbedder(), scopeId = "private-chat-B")
        assertTrue(otherConversation.search("feline").isEmpty())
        otherConversation.indexDocument("private.txt", "A dog is mentioned in a different private chat.")
        assertEquals("A cat is mentioned here.", PersistentHybridRag(dao, FakeEmbedder(), scopeId = "private-chat-A")
            .search("feline").first().chunk.text)
        assertTrue(otherConversation.search("canine").isNotEmpty())
    }

    @Test fun cosineSimilarityHandlesZeroAndOrthogonalVectors() {
        assertEquals(1.0, cosineSimilarity(floatArrayOf(1f, 0f), floatArrayOf(2f, 0f)), 0.00001)
        assertEquals(0.0, cosineSimilarity(floatArrayOf(1f, 0f), floatArrayOf(0f, 1f)), 0.00001)
        assertEquals(0.0, cosineSimilarity(floatArrayOf(0f, 0f), floatArrayOf(1f, 0f)), 0.00001)
    }
}

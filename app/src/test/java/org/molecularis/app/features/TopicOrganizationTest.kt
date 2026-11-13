package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import org.molecularis.app.data.KnowledgeTopicEntity

class TopicOrganizationTest {
    private fun topic(id: String, name: String, parent: String? = null, page: Int = 1) =
        KnowledgeTopicEntity(id, "book", name, page, 0f, "test", false, parent)

    @Test fun normalizesCaseAndWhitespaceForAliases() {
        assertEquals("citric acid cycle", TopicOrganization.normalizeName("  CITRIC   acid Cycle "))
    }

    @Test fun findsDuplicateTopicNamesWithoutMergingAutomatically() {
        val groups = TopicOrganization.duplicateGroups(listOf(
            topic("a", "Glycolysis", page = 12),
            topic("b", " glycolysis ", page = 4),
            topic("c", "Gluconeogenesis")
        ))
        assertEquals(1, groups.size)
        assertEquals(listOf("b", "a"), groups.single().map { it.id })
    }

    @Test fun mapsTopicPassagesUntilNextDistinctHeadingPage() {
        val topics = listOf(
            topic("a", "Glycolysis", page = 4),
            topic("b", "Glycolysis regulation", page = 4),
            topic("c", "Gluconeogenesis", page = 9)
        )
        val ranges = TopicOrganization.topicPageRanges(topics, 20)
        assertEquals(4..8, ranges["a"])
        assertEquals(4..8, ranges["b"])
        assertEquals(9..20, ranges["c"])
    }

    @Test fun clampsInvalidTopicPagesToDocumentBounds() {
        val ranges = TopicOrganization.topicPageRanges(listOf(topic("a", "Topic", page = 90)), 12)
        assertEquals(12..12, ranges["a"])
    }

    @Test fun preventsParentingToSelfOrDescendant() {
        val topics = listOf(
            topic("root", "Metabolism"),
            topic("child", "Carbohydrate metabolism", "root"),
            topic("leaf", "Glycolysis", "child")
        )
        assertTrue(TopicOrganization.wouldCreateCycle("root", "leaf", topics))
        assertTrue(TopicOrganization.wouldCreateCycle("child", "child", topics))
        assertFalse(TopicOrganization.wouldCreateCycle("leaf", "root", topics))
    }
}

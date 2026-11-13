package org.molecularis.app.features

import org.molecularis.app.data.KnowledgeTopicEntity
import java.util.Locale

/** Normalization helpers for professor-controlled topic names and aliases. */
object TopicOrganization {
    fun normalizeName(value: String): String =
        value.trim().lowercase(Locale.ROOT).replace(Regex("\\s+"), " ")

    fun duplicateGroups(topics: List<KnowledgeTopicEntity>): List<List<KnowledgeTopicEntity>> =
        topics.filter { normalizeName(it.name).isNotBlank() }
            .groupBy { normalizeName(it.name) }
            .values.filter { it.size > 1 }
            .map { it.sortedBy { topic -> topic.startPage } }

    /** Each heading owns passages up to (but not including) the next distinct heading page. */
    fun topicPageRanges(topics: List<KnowledgeTopicEntity>, pageCount: Int): Map<String, IntRange> {
        if (topics.isEmpty() || pageCount < 1) return emptyMap()
        val starts = topics.map { it.startPage.coerceIn(1, pageCount) }.distinct().sorted()
        return topics.associate { topic ->
            val start = topic.startPage.coerceIn(1, pageCount)
            val next = starts.firstOrNull { it > start }
            topic.id to (start..((next?.minus(1) ?: pageCount).coerceAtLeast(start)))
        }
    }

    fun wouldCreateCycle(topicId: String, parentId: String?, topics: List<KnowledgeTopicEntity>): Boolean {
        if (parentId == null) return false
        var current = topics.firstOrNull { it.id == parentId } ?: return false
        val visited = mutableSetOf<String>()
        while (true) {
            if (current.id == topicId) return true
            if (!visited.add(current.id)) return true
            val next = current.parentTopicId ?: return false
            current = topics.firstOrNull { it.id == next } ?: return false
        }
    }
}

package org.assayflux.molecularis

/** A searchable item backed by an actual local job or repository capability. */
internal data class SearchDocument(
    val id: String,
    val title: String,
    val subtitle: String,
    val searchableText: String,
    val kind: Kind,
) {
    enum class Kind { JOB, CAPABILITY }
}

internal fun filterSearchDocuments(
    query: String,
    documents: List<SearchDocument>,
): List<SearchDocument> {
    val needle = query.trim()
    if (needle.isEmpty()) return emptyList()
    return documents.filter { document ->
        document.title.contains(needle, ignoreCase = true) ||
            document.subtitle.contains(needle, ignoreCase = true) ||
            document.searchableText.contains(needle, ignoreCase = true)
    }.distinctBy { it.id }
}

package org.molecularis.app.features

/**
 * Conservative teaching-source gate. This measures extraction usability only;
 * it is not a measure of scientific correctness or textbook authority.
 */
data class TeachingSourceQuality(
    val score: Int,
    val textCoverage: Float,
    val eligible: Boolean,
    val reason: String
)

object TeachingQualityPolicy {
    fun assess(
        extractedPages: Int,
        pagesWithText: Int,
        emptyPages: Int,
        shortTextPages: Int,
        duplicatePages: Int,
        passageCount: Int
    ): TeachingSourceQuality {
        if (extractedPages <= 0 || passageCount <= 0) {
            return TeachingSourceQuality(0, 0f, false, "No usable extracted pages or passages")
        }
        val total = extractedPages.toFloat()
        val coverage = (pagesWithText / total).coerceIn(0f, 1f)
        val emptyRate = (emptyPages / total).coerceIn(0f, 1f)
        val shortRate = (shortTextPages / total).coerceIn(0f, 1f)
        val duplicateRate = (duplicatePages / total).coerceIn(0f, 1f)
        val score = (coverage * 50f + (1f - emptyRate) * 20f +
            (1f - shortRate) * 15f + (1f - duplicateRate) * 15f).toInt().coerceIn(0, 100)
        val eligible = coverage >= 0.35f && score >= 55
        val reason = when {
            !eligible && coverage < 0.35f -> "Text coverage below 35%"
            !eligible -> "Extraction quality score below 55/100"
            else -> "Eligible for source-grounded draft"
        }
        return TeachingSourceQuality(score, coverage, eligible, reason)
    }

    fun sourceBlockCount(outline: String): Int =
        Regex("(?m)^SOURCE\\s+\\d+\\s*:").findAll(outline).count()
}

/** Weighted minute allocation that always sums exactly to the selected lesson duration. */
data class LessonSectionTime(val title: String, val minutes: Int)

object LessonPlanningPolicy {
    private val standard = listOf(
        "Learning outcomes" to 10,
        "Prerequisites and orientation" to 10,
        "Core explanation" to 25,
        "Mechanism and pathway integration" to 20,
        "Regulation and control" to 15,
        "Clinical / applied relevance" to 10,
        "Recap and retrieval" to 10
    )

    fun allocateTime(durationMinutes: Int, audience: String): List<LessonSectionTime> {
        val weights = when (audience) {
            "PhD" -> listOf(8, 7, 20, 25, 18, 7, 15)
            "MD / DNB" -> listOf(9, 8, 22, 19, 18, 15, 9)
            else -> standard.map { it.second }
        }
        val totalWeight = weights.sum().toFloat()
        val exact = weights.map { durationMinutes.coerceAtLeast(1) * it / totalWeight }
        val base = exact.map { it.toInt() }.toMutableList()
        var remaining = durationMinutes.coerceAtLeast(1) - base.sum()
        val order = exact.indices.sortedByDescending { exact[it] - base[it] }
        var cursor = 0
        while (remaining > 0) {
            base[order[cursor % order.size]]++
            remaining--
            cursor++
        }
        return standard.mapIndexed { index, section -> LessonSectionTime(section.first, base[index]) }
    }
}

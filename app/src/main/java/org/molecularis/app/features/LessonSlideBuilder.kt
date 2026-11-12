package org.molecularis.app.features

data class LessonSlide(val title: String, val points: List<String>)

/**
 * Converts the professor-editable lesson outline into a simple offline slide sequence.
 * This is intentionally a deterministic formatter, not a scientific content generator.
 */
object LessonSlideBuilder {
    fun build(outline: String, topic: String, level: String, minutes: Int): List<LessonSlide> {
        if (outline.isBlank()) return emptyList()
        val result = mutableListOf(
            LessonSlide(
                topic.ifBlank { "Biochemistry lesson" },
                listOf("Audience: $level", "Teaching time: $minutes minutes", "Molecularis · Teaching Studio")
            )
        )
        var currentTitle: String? = null
        var currentPoints = mutableListOf<String>()

        fun flush() {
            val title = currentTitle ?: return
            val cleanPoints = currentPoints.map { it.trim().removePrefix("-").trim() }
                .filter {
                    it.isNotBlank() &&
                        !it.startsWith("SOURCE ") &&
                        !it.startsWith("REVIEW NOTE:") &&
                        !it.startsWith("LOCAL LIBRARY RETRIEVAL")
                }
                .take(6)
            result += LessonSlide(title, cleanPoints)
            currentTitle = null
            currentPoints = mutableListOf()
        }

        outline.lineSequence().forEach { raw ->
            val line = raw.trim()
            val heading = Regex("^\\d+\\.\\s+(.+)$").matchEntire(line)
            when {
                heading != null -> {
                    flush()
                    currentTitle = heading.groupValues[1]
                }
                currentTitle != null && (
                    line.startsWith("LOCAL LIBRARY RETRIEVAL") ||
                        line.startsWith("TEACHING EMPHASIS:") ||
                        line.startsWith("REVIEW NOTE:")
                    ) -> flush()
                currentTitle != null && line.startsWith("SOURCE ") -> Unit
                currentTitle != null && line.isNotBlank() -> {
                    val point = line.removePrefix("-").trim()
                    if (point.isNotBlank()) currentPoints += point
                }
            }
        }
        flush()
        return result
    }
}

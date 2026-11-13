package org.molecularis.app.features

data class NarrationChunk(val slideIndex: Int, val text: String)

/** Pure, bounded timeline logic shared by narration playback and unit tests. */
object LessonNarrationTimeline {
    fun build(slides: List<String>, maxCharacters: Int = 2600): List<NarrationChunk> {
        require(maxCharacters in 100..4000) { "Narration chunk size must be between 100 and 4,000 characters." }
        return slides.mapIndexed { index, slide ->
            index to slide.trim()
        }.flatMap { (slideIndex, text) ->
            if (text.isBlank()) emptyList()
            else split(text, maxCharacters).map { NarrationChunk(slideIndex, it) }
        }
    }

    fun firstChunkForSlide(chunks: List<NarrationChunk>, slideIndex: Int): Int {
        require(chunks.isNotEmpty()) { "Narration timeline is empty." }
        return chunks.indexOfFirst { it.slideIndex >= slideIndex }
            .takeIf { it >= 0 } ?: chunks.lastIndex
    }

    private fun split(text: String, maxCharacters: Int): List<String> {
        if (text.length <= maxCharacters) return listOf(text)
        val result = mutableListOf<String>()
        var start = 0
        while (start < text.length) {
            var end = (start + maxCharacters).coerceAtMost(text.length)
            if (end < text.length) {
                val boundary = text.lastIndexOfAny(charArrayOf('.', '!', '?', '\n', ' '), end)
                if (boundary > start + maxCharacters / 2) end = boundary + 1
            }
            result += text.substring(start, end).trim()
            start = end
            while (start < text.length && text[start].isWhitespace()) start++
        }
        return result.filter(String::isNotBlank)
    }
}

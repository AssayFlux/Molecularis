package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class LessonNarrationTimelineTest {
    @Test fun chunksRetainTheirSlideOwnership() {
        val timeline = LessonNarrationTimeline.build(
            listOf("Slide one. " + "A".repeat(240), "Slide two. " + "B".repeat(240)),
            maxCharacters = 180
        )
        assertEquals(listOf(0, 0, 1, 1), timeline.map { it.slideIndex })
    }

    @Test fun seekFindsFirstChunkForRequestedSlide() {
        val timeline = LessonNarrationTimeline.build(listOf("A".repeat(250), "B".repeat(250)), 150)
        assertEquals(2, LessonNarrationTimeline.firstChunkForSlide(timeline, 1))
    }

    @Test fun rejectsUnsafeChunkSizes() {
        assertThrows(IllegalArgumentException::class.java) { LessonNarrationTimeline.build(listOf("Text"), 20) }
    }

    @Test fun ignoresBlankSlides() {
        val timeline = LessonNarrationTimeline.build(listOf(" ", "Second slide"))
        assertEquals(listOf(NarrationChunk(1, "Second slide")), timeline)
    }
}

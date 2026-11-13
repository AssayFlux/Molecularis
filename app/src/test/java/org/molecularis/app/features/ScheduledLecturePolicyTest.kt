package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Test

class ScheduledLecturePolicyTest {
    @Test fun validatesScheduleFieldsAndFutureTime() {
        assertNotNull(ScheduledLecturePolicy.validate("", 30, "en-US", 10_000, 0))
        assertNotNull(ScheduledLecturePolicy.validate("Lesson", 4, "en-US", 10_000, 0))
        assertNotNull(ScheduledLecturePolicy.validate("Lesson", 30, "en-US", 30_000, 0))
        assertNull(ScheduledLecturePolicy.validate("Lesson", 30, "en-US", 120_000, 0))
    }

    @Test fun stripsMarkdownAndBoundsNarration() {
        assertEquals("ATP is energy", ScheduledLecturePolicy.narrationText("## ATP is *energy*"))
        assertEquals(1, ScheduledLecturePolicy.chunks("short script").size)
    }

    @Test fun chunksLongTextWithoutDroppingCharacters() {
        val input = ("biochemistry ").repeat(600)
        val chunks = ScheduledLecturePolicy.chunks(input, 500)
        assertEquals(input.trim(), chunks.joinToString(" "))
        assertEquals(true, chunks.all { it.length <= 500 })
    }
}

package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class LessonSlideBuilderTest {
    @Test fun createsTitleSlideAndNumberedSectionSlides() {
        val slides = LessonSlideBuilder.build(
            "1. Outcomes\n- Explain the pathway\n- Identify control points\n\n2. Regulation\n- Describe hormonal control",
            "Glycolysis",
            "MBBS",
            30
        )
        assertEquals(3, slides.size)
        assertEquals("Glycolysis", slides[0].title)
        assertEquals("Outcomes", slides[1].title)
        assertEquals(listOf("Explain the pathway", "Identify control points"), slides[1].points)
        assertEquals("Regulation", slides[2].title)
    }

    @Test fun excludesSourceMetadataAndReviewNotesFromSlideBody() {
        val slides = LessonSlideBuilder.build(
            "1. Core explanation\n- Explain the mechanism\nSOURCE 1: textbook · page 4\nsource excerpt\nREVIEW NOTE: verify before teaching",
            "Topic",
            "PhD",
            45
        )
        assertEquals(2, slides.size)
        assertEquals(listOf("Explain the mechanism"), slides[1].points)
    }

    @Test fun capsEachSlideAtSixBullets() {
        val bullets = (1..9).joinToString("\n") { "- Point $it" }
        val slides = LessonSlideBuilder.build("1. Main\n$bullets", "Topic", "MD / DNB", 60)
        assertEquals(6, slides[1].points.size)
    }

    @Test fun blankOutlineProducesNoSlides() {
        assertTrue(LessonSlideBuilder.build("  ", "Topic", "MBBS", 30).isEmpty())
    }
}

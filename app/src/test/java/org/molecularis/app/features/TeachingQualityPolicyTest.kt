package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class TeachingQualityPolicyTest {
    @Test fun rejectsSourcesWithNoPassagesOrPages() {
        assertFalse(TeachingQualityPolicy.assess(0, 0, 0, 0, 0, 0).eligible)
        assertFalse(TeachingQualityPolicy.assess(10, 8, 2, 1, 0, 0).eligible)
    }

    @Test fun rejectsLowCoverageEvenWhenProfessorApproved() {
        val result = TeachingQualityPolicy.assess(100, 20, 80, 5, 0, 30)
        assertFalse(result.eligible)
        assertEquals("Text coverage below 35%", result.reason)
    }

    @Test fun acceptsUsableExtractionButLabelsItAsUsabilityNotAccuracy() {
        val result = TeachingQualityPolicy.assess(100, 90, 5, 4, 2, 120)
        assertTrue(result.eligible)
        assertTrue(result.score >= 55)
    }

    @Test fun countsOnlyExplicitSourceBlocks() {
        assertEquals(2, TeachingQualityPolicy.sourceBlockCount(
            "Intro\nSOURCE 1: Book · page 4\ntext\nSOURCE 2: Book · page 8"
        ))
    }

    @Test fun lessonTimeBudgetsSumExactlyToDurationForEachAudience() {
        listOf("MBBS", "MD / DNB", "PhD").forEach { audience ->
            val plan = LessonPlanningPolicy.allocateTime(37, audience)
            assertEquals(37, plan.sumOf { it.minutes })
            assertTrue(plan.all { it.minutes >= 0 })
        }
    }
}

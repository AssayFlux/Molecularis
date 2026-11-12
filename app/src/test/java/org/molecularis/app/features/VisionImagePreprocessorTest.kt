package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Test

class VisionImagePreprocessorTest {
    @Test fun keepsSmallImagesAtFullResolution() {
        assertEquals(1, VisionImagePreprocessor.calculateSampleSize(1024, 768))
    }

    @Test fun downsamplesLargeLandscapeImagesToConfiguredBound() {
        val sample = VisionImagePreprocessor.calculateSampleSize(6000, 4000)
        assertEquals(4, sample)
        assertEquals(true, (6000 + sample - 1) / sample <= VisionImagePreprocessor.MAX_DIMENSION)
        assertEquals(true, (4000 + sample - 1) / sample <= VisionImagePreprocessor.MAX_DIMENSION)
    }

    @Test fun downsamplesTallImagesAsWellAsWideImages() {
        assertEquals(4, VisionImagePreprocessor.calculateSampleSize(1200, 6000))
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejectsInvalidImageDimensions() {
        VisionImagePreprocessor.calculateSampleSize(0, 100)
    }
}

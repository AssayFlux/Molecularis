package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class OfflineVoiceControllerTest {
    @Test fun voiceLabelsAreReadableAndHideEngineIds() {
        val voice = OfflineTtsVoice(
            name = "com.example.tts.en-us-x-sfg-local",
            languageTag = "en-US",
            quality = 400
        )
        assertTrue(voice.label.contains("English"))
        assertTrue(voice.label.contains("High quality"))
        assertTrue(!voice.label.contains("com.example"))
        assertTrue(!voice.label.contains("x-sfg"))
    }

    @Test fun voiceLabelsDescribeQualityWithoutTechnicalNumbers() {
        val voice = OfflineTtsVoice(
            name = "internal-voice-42",
            languageTag = "hi-IN",
            quality = 300
        )
        assertTrue(voice.label.contains("Hindi"))
        assertTrue(voice.label.contains("Standard quality"))
        assertTrue(!voice.label.contains("300"))
    }

    @Test fun normalizesLanguageTags() {
        assertEquals("en-US", OfflineVoiceController.normalizeLanguageTag("en-us"))
        assertEquals("hi-IN", OfflineVoiceController.normalizeLanguageTag("hi-IN"))
        assertEquals("bn-IN", OfflineVoiceController.normalizeLanguageTag("bn-IN"))
    }

    @Test fun acceptsLanguageTagsWithScriptSubtags() {
        assertEquals("zh-Hans-CN", OfflineVoiceController.normalizeLanguageTag("zh-hans-cn"))
    }

    @Test fun rejectsBlankLanguageTags() {
        val error = runCatching { OfflineVoiceController.normalizeLanguageTag("") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsMalformedLanguageTags() {
        val error = runCatching { OfflineVoiceController.normalizeLanguageTag("en_US") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsWhitespaceInLanguageTags() {
        val error = runCatching { OfflineVoiceController.normalizeLanguageTag("en US") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }
}

package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class BiochemistryPronunciationDictionaryTest {
    @Test fun replacesWholeBiochemicalTermsWithoutChangingLargerWords() {
        assertEquals(
            "A T P synthase produces ATPase is unchanged",
            BiochemistryPronunciationDictionary.apply("ATP synthase produces ATPase is unchanged", listOf(PronunciationEntry("ATP", "A T P")))
        )
    }

    @Test fun longerTermsAreAppliedBeforeShorterTerms() {
        val entries = listOf(PronunciationEntry("AMP", "A M P"), PronunciationEntry("cAMP", "cyclic A M P"))
        assertEquals("cyclic A M P and A M P", BiochemistryPronunciationDictionary.apply("cAMP and AMP", entries))
    }

    @Test fun parserIgnoresCommentsAndRejectsMalformedLines() {
        assertEquals(
            listOf(PronunciationEntry("ATP", "A T P")),
            BiochemistryPronunciationDictionary.parse("# custom terms\nATP=A T P")
        )
        assertThrows(IllegalArgumentException::class.java) {
            BiochemistryPronunciationDictionary.parse("missing separator")
        }
    }

    @Test fun parserRejectsOversizedDictionaries() {
        assertThrows(IllegalArgumentException::class.java) {
            BiochemistryPronunciationDictionary.parse("A".repeat(8_001))
        }
    }
}

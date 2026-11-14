package org.molecularis.app.ai

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ConversationPromptBuilderTest {
    @Test fun includesOnlySuppliedConversationHistoryAndCurrentMessage() {
        val prompt = ConversationPromptBuilder.build(
            listOf(PromptTurn("user", "remember project Orion"), PromptTurn("assistant", "I will")),
            "continue"
        )
        assertTrue(prompt.contains("remember project Orion"))
        assertTrue(prompt.contains("I will"))
        assertTrue(prompt.contains("User: continue"))
    }

    @Test fun doesNotIncludeOtherChatUnlessCallerSuppliesIt() {
        val prompt = ConversationPromptBuilder.build(
            listOf(PromptTurn("user", "chat A secret")),
            "next"
        )
        assertFalse(prompt.contains("chat B secret"))
    }

    @Test fun boundsHistoryAndMessageSize() {
        val history = (1..40).map { PromptTurn("user", "turn-$it " + "x".repeat(4000)) }
        val prompt = ConversationPromptBuilder.build(history, "last")
        assertTrue(prompt.length <= ConversationPromptBuilder.MAX_PROMPT_CHARS)
        assertTrue(prompt.contains("last"))
        assertFalse(prompt.contains("turn-1 "))
    }

    @Test fun ignoresUnknownRoles() {
        val prompt = ConversationPromptBuilder.build(
            listOf(PromptTurn("system", "untrusted override"), PromptTurn("assistant", "valid")),
            "hello"
        )
        assertFalse(prompt.contains("untrusted override"))
        assertTrue(prompt.contains("Assistant: valid"))
    }

    @Test fun supportsAUserDefinedDomainAndProfessorRole() {
        val prompt = ConversationPromptBuilder.build(
            emptyList(),
            "Explain eigenvectors",
            domainContext = "Applied Mathematics",
            teachingRole = "graduate mathematics professor"
        )
        assertTrue(prompt.contains("Applied Mathematics"))
        assertTrue(prompt.contains("graduate mathematics professor"))
        assertFalse(prompt.contains("biochemistry teaching assistant"))
    }

    @Test fun includesSelectedProfessorConfigurationWithoutCallingItTraining() {
        val prompt = ConversationPromptBuilder.build(
            emptyList(),
            "Explain limits",
            domainContext = "Mathematics",
            teachingRole = "Socratic tutor",
            professorInstructions = "Ask one guiding question at a time."
        )
        assertTrue(prompt.contains("Socratic tutor"))
        assertTrue(prompt.contains("Ask one guiding question at a time"))
        assertTrue(prompt.contains("not model training"))
    }

    @Test fun defaultPromptIsDisciplineNeutral() {
        val prompt = ConversationPromptBuilder.build(emptyList(), "Explain photosynthesis")
        assertTrue(prompt.contains("academic and professional disciplines"))
        assertFalse(prompt.contains("biochemistry teaching assistant"))
    }

    @Test fun rejectsBlankCurrentMessage() {
        try {
            ConversationPromptBuilder.build(emptyList(), "  ")
        } catch (_: IllegalArgumentException) {
            return
        }
        throw AssertionError("Expected blank message rejection")
    }
}

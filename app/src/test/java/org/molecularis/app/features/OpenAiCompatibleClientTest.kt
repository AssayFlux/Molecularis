package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class OpenAiCompatibleClientTest {
    @Test fun rejectsNonHttpsProviderEndpoints() {
        assertThrows(IllegalArgumentException::class.java) {
            OpenAiCompatibleClient("http://provider.example", "test-key-123456", "demo-model")
        }
    }

    @Test fun rejectsEndpointCredentialsAndQueryParameters() {
        assertThrows(IllegalArgumentException::class.java) {
            OpenAiCompatibleClient("https://user:pass@provider.example", "test-key-123456", "demo-model")
        }
        assertThrows(IllegalArgumentException::class.java) {
            OpenAiCompatibleClient("https://provider.example?token=secret", "test-key-123456", "demo-model")
        }
    }

    @Test fun requiresValidModelAndKey() {
        assertThrows(IllegalArgumentException::class.java) {
            OpenAiCompatibleClient("https://provider.example", "short", "demo-model")
        }
        assertThrows(IllegalArgumentException::class.java) {
            OpenAiCompatibleClient("https://provider.example", "test-key-123456", " ")
        }
    }

    @Test fun acceptsRootAndV1BaseUrls() {
        assertEquals(
            "OpenAiCompatibleClient",
            OpenAiCompatibleClient("https://provider.example", "test-key-123456", "demo-model").javaClass.simpleName
        )
        assertEquals(
            "OpenAiCompatibleClient",
            OpenAiCompatibleClient("https://provider.example/v1/", "test-key-123456", "demo-model").javaClass.simpleName
        )
    }
}

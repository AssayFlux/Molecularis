package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class TrainingApiClientTest {
    @Test fun rejectsPlainHttpToProtectDatasetAndApiKey() {
        assertThrows(IllegalArgumentException::class.java) {
            TrainingApiClient("http://192.168.1.20:8080", "0123456789abcdef")
        }
    }

    @Test fun acceptsHttpsTrainingEndpoint() {
        val client = TrainingApiClient("https://training.example.test/", "0123456789abcdef")
        assertEquals("TrainingApiClient", client.javaClass.simpleName)
    }

    @Test fun rejectsShortApiKey() {
        assertThrows(IllegalArgumentException::class.java) {
            TrainingApiClient("https://training.example.test", "short")
        }
    }
}

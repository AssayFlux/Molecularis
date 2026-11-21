package org.assayflux.molecularis

import java.nio.file.Files
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertThrows
import org.junit.Test

class PrivateTemporaryFileTest {
    @Test
    fun deletesPartialPlaintextWhenMaterializationFails() {
        val file = Files.createTempFile("kinetics-private-", ".tmp").toFile()
        val result = withPrivateTemporaryFile(
            file = file,
            materialize = { destination ->
                destination.writeText("partial plaintext")
                false
            },
            action = { error("Consumer must not run") },
        )
        assertNull(result)
        assertFalse(file.exists())
    }

    @Test
    fun deletesPlaintextWhenConsumerThrows() {
        val file = Files.createTempFile("kinetics-private-", ".tmp").toFile()
        val failure = assertThrows(IllegalStateException::class.java) {
            withPrivateTemporaryFile(
                file = file,
                materialize = { destination ->
                    destination.writeText("authenticated plaintext")
                    true
                },
                action = { throw IllegalStateException("analysis failed") },
            )
        }
        assertEquals("analysis failed", failure.message)
        assertFalse(file.exists())
    }

    @Test
    fun returnsConsumerResultAndDeletesPlaintextOnSuccess() {
        val file = Files.createTempFile("kinetics-private-", ".tmp").toFile()
        val result = withPrivateTemporaryFile(
            file = file,
            materialize = { destination ->
                destination.writeText("authenticated plaintext")
                true
            },
            action = { it.readText().length },
        )
        assertEquals(23, result)
        assertFalse(file.exists())
    }
}

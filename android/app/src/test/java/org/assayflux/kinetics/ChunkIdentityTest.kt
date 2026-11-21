package org.assayflux.molecularis

import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertThrows
import org.junit.Test

class ChunkIdentityTest {
    @Test
    fun associatedDataIsDeterministicAndBoundToJobAndChunk() {
        val first = ChunkIdentity.associatedData("kinetics-import:job-a", 0)
        assertArrayEquals(first, ChunkIdentity.associatedData("kinetics-import:job-a", 0))
        assertFalse(first.contentEquals(ChunkIdentity.associatedData("kinetics-import:job-b", 0)))
        assertFalse(first.contentEquals(ChunkIdentity.associatedData("kinetics-import:job-a", 1)))
    }

    @Test
    fun associatedDataRejectsInvalidIdentity() {
        assertThrows(IllegalArgumentException::class.java) {
            ChunkIdentity.associatedData(" ", 0)
        }
        assertThrows(IllegalArgumentException::class.java) {
            ChunkIdentity.associatedData("job", -1)
        }
    }
}

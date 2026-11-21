package org.assayflux.molecularis

import java.io.File
import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class KdatFileHeaderTest {
    @Test fun emptyFileReceivesKdatV2Header() {
        val file = File.createTempFile("kinetics-kdat", ".tmp")
        try {
            KdatFileHeader.ensure(file)
            assertEquals(KdatFileHeader.HEADER_BYTES, file.length())
            assertArrayEquals(byteArrayOf(0x4b, 0x44, 0x41, 0x54, 0x02), file.readBytes())
        } finally {
            file.delete()
        }
    }

    @Test fun validHeaderIsIdempotent() {
        val file = File.createTempFile("kinetics-kdat", ".tmp")
        try {
            KdatFileHeader.ensure(file)
            val first = file.readBytes()
            KdatFileHeader.ensure(file)
            assertArrayEquals(first, file.readBytes())
        } finally {
            file.delete()
        }
    }

    @Test fun invalidNonEmptyFileIsRejectedWithoutTruncation() {
        val file = File.createTempFile("kinetics-kdat", ".tmp")
        val original = byteArrayOf(1, 2, 3, 4, 5, 6, 7, 8)
        try {
            file.writeBytes(original)
            assertThrows(IllegalStateException::class.java) { KdatFileHeader.ensure(file) }
            assertArrayEquals(original, file.readBytes())
        } finally {
            file.delete()
        }
    }

    @Test fun tornNonEmptyHeaderIsPreserved() {
        val file = File.createTempFile("kinetics-kdat", ".tmp")
        val original = byteArrayOf(0x4b, 0x44, 0x41)
        try {
            file.writeBytes(original)
            assertThrows(IllegalStateException::class.java) { KdatFileHeader.ensure(file) }
            assertArrayEquals(original, file.readBytes())
        } finally {
            file.delete()
        }
    }
}

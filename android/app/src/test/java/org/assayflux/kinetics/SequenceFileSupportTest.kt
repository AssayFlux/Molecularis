package org.assayflux.molecularis

import java.io.File
import java.nio.charset.StandardCharsets
import java.util.zip.GZIPOutputStream
import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class SequenceFileSupportTest {
    @Test
    fun readsPlainUtf8SequenceFile() {
        val file = File.createTempFile("kinetics-sequence-", ".fa")
        try {
            file.writeText(">sample\nACGT\n", StandardCharsets.UTF_8)
            assertEquals(">sample\nACGT\n", SequenceFileSupport.readText(file, false, 128, 128))
        } finally {
            file.delete()
        }
    }

    @Test
    fun decompressesGzipWithinExpandedLimit() {
        val file = File.createTempFile("kinetics-sequence-", ".fa.gz")
        try {
            GZIPOutputStream(file.outputStream()).use { it.write(">sample\nACGT\n".toByteArray(StandardCharsets.UTF_8)) }
            assertEquals(">sample\nACGT\n", SequenceFileSupport.readText(file, true, 128, 128))
        } finally {
            file.delete()
        }
    }

    @Test
    fun rejectsExpandedGzipBeyondLimit() {
        val file = File.createTempFile("kinetics-sequence-", ".fq.gz")
        try {
            GZIPOutputStream(file.outputStream()).use { it.write("A".repeat(256).toByteArray(StandardCharsets.UTF_8)) }
            assertThrows(IllegalArgumentException::class.java) {
                SequenceFileSupport.readText(file, true, 64, 64)
            }
        } finally {
            file.delete()
        }
    }

    @Test
    fun rejectsMalformedUtf8() {
        val file = File.createTempFile("kinetics-sequence-", ".fa")
        try {
            file.writeBytes(byteArrayOf(0xC3.toByte(), 0x28))
            assertThrows(Exception::class.java) {
                SequenceFileSupport.readText(file, false, 64, 64)
            }
        } finally {
            file.delete()
        }
    }
}

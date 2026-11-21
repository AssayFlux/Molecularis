package org.assayflux.molecularis

import java.io.File
import java.io.RandomAccessFile

/** Pure file-header boundary for the KDAT v2 encrypted container. */
internal object KdatFileHeader {
    const val HEADER_BYTES = 5L
    private val magic = byteArrayOf(0x4b, 0x44, 0x41, 0x54)
    private const val VERSION = 2

    /** Initializes only a new empty file; any non-empty invalid header is preserved and rejected. */
    fun ensure(file: File) {
        RandomAccessFile(file, "rw").use { output ->
            if (output.length() == 0L) {
                output.write(magic)
                output.writeByte(VERSION)
                output.fd.sync()
                return
            }
            val valid = try {
                val actualMagic = ByteArray(magic.size)
                output.seek(0)
                output.readFully(actualMagic)
                actualMagic.contentEquals(magic) && output.readUnsignedByte() == VERSION
            } catch (_: Exception) {
                false
            }
            check(valid) {
                "Encrypted staging header is invalid; ciphertext was preserved. " +
                    "Start a new import rather than overwriting this partial file"
            }
        }
    }
}

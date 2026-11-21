package org.assayflux.molecularis

import java.nio.file.Files
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class EncryptedOrphanScannerTest {
    @Test
    fun reportsUnreferencedFinalAndPartialCiphertextWithoutDeletingAnything() {
        val root = Files.createTempDirectory("kinetics-orphans").toFile()
        val finalized = root.resolve("research-inputs").apply { mkdirs() }
        val staging = root.resolve("research-imports").apply { mkdirs() }
        val referenced = finalized.resolve("kept.kdat").apply { writeBytes(byteArrayOf(1, 2, 3)) }
        val orphanFinal = finalized.resolve("lost.kdat").apply { writeBytes(byteArrayOf(4, 5)) }
        val orphanPartial = staging.resolve("deleted-job.encpart").apply { writeBytes(byteArrayOf(6)) }
        val activePartial = staging.resolve("active-job.encpart").apply { writeBytes(byteArrayOf(7)) }
        val stalePartial = staging.resolve("completed-job.encpart").apply { writeBytes(byteArrayOf(8)) }

        val findings = EncryptedOrphanScanner.scan(
            finalizedDirectory = finalized,
            stagingDirectory = staging,
            referencedFinalPaths = setOf(referenced.canonicalPath),
            knownJobIds = setOf("active-job", "completed-job", "kept"),
            jobsWithFinalStorage = setOf("kept", "completed-job"),
        )

        assertEquals(
            setOf(orphanFinal.canonicalPath, orphanPartial.canonicalPath, stalePartial.canonicalPath),
            findings.map { it.path }.toSet(),
        )
        assertEquals(3, findings.size)
        assertFalse(findings.any { it.path == activePartial.canonicalPath })
        assertEquals(2L, orphanFinal.length())
        assertEquals(1L, orphanPartial.length())
        assertEquals(1L, stalePartial.length())
        assertEquals(3L, referenced.length())
        assertEquals(1L, activePartial.length())
    }

    @Test
    fun ignoresSymlinksAndMissingDirectories() {
        val root = Files.createTempDirectory("kinetics-orphan-links").toFile()
        val staging = root.resolve("staging").apply { mkdirs() }
        val outside = root.resolve("outside.encpart").apply { writeBytes(byteArrayOf(1)) }
        Files.createSymbolicLink(staging.resolve("linked.encpart").toPath(), outside.toPath())

        val findings = EncryptedOrphanScanner.scan(
            finalizedDirectory = root.resolve("missing"),
            stagingDirectory = staging,
            referencedFinalPaths = emptySet(),
            knownJobIds = emptySet(),
            jobsWithFinalStorage = emptySet(),
        )

        assertEquals(emptyList<EncryptedOrphanFile>(), findings)
        assertEquals(1L, outside.length())
    }
}

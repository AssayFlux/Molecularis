package org.assayflux.molecularis

import java.io.File
import java.nio.file.Files
import java.nio.file.LinkOption

/** A report-only finding; inventory never deletes, renames, or decrypts ciphertext. */
data class EncryptedOrphanFile(
    val path: String,
    val kind: String,
    val sizeBytes: Long,
    val modifiedAtMillis: Long,
)

/**
 * Finds encrypted files which have no matching durable job/storage reference.
 *
 * Symbolic links and non-regular files are ignored. Callers must present the report
 * for review; automatic cleanup is deliberately not provided.
 */
object EncryptedOrphanScanner {
    private val jobIdPattern = Regex("[A-Za-z0-9_-]{1,80}")

    fun scan(
        finalizedDirectory: File,
        stagingDirectory: File,
        referencedFinalPaths: Set<String>,
        knownJobIds: Set<String>,
        jobsWithFinalStorage: Set<String>,
    ): List<EncryptedOrphanFile> {
        val findings = mutableListOf<EncryptedOrphanFile>()
        scanDirectory(finalizedDirectory, ".kdat") { file ->
            if (file.canonicalPath !in referencedFinalPaths) {
                findings += finding(file, "unreferenced_finalized")
            }
        }
        scanDirectory(stagingDirectory, ".encpart") { file ->
            val jobId = file.name.removeSuffix(".encpart")
            if (!jobIdPattern.matches(jobId) ||
                jobId !in knownJobIds || jobId in jobsWithFinalStorage
            ) {
                findings += finding(file, "unreferenced_partial")
            }
        }
        return findings.sortedWith(compareBy<EncryptedOrphanFile>({ it.kind }, { it.path }))
    }

    private fun scanDirectory(
        directory: File,
        extension: String,
        inspect: (File) -> Unit,
    ) {
        if (!Files.isDirectory(directory.toPath(), LinkOption.NOFOLLOW_LINKS)) return
        val root = directory.canonicalFile
        directory.listFiles()
            ?.filter { file ->
                file.name.endsWith(extension) &&
                    Files.isRegularFile(file.toPath(), LinkOption.NOFOLLOW_LINKS) &&
                    file.canonicalFile.parentFile == root
            }
            ?.forEach(inspect)
    }

    private fun finding(file: File, kind: String) = EncryptedOrphanFile(
        path = file.canonicalPath,
        kind = kind,
        sizeBytes = file.length(),
        modifiedAtMillis = file.lastModified(),
    )
}

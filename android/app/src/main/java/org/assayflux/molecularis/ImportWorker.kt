package org.assayflux.molecularis

import android.content.Context
import android.net.Uri
import androidx.work.Worker
import androidx.work.WorkerParameters
import java.io.File
import java.io.RandomAccessFile
import java.security.MessageDigest

/**
 * Streams SAF input into independently authenticated AES-GCM chunks in app-private
 * no-backup storage. Resume truncates only an incomplete final record and verifies
 * the source prefix before appending, without writing plaintext staging files.
 */
class ImportWorker(context: Context, parameters: WorkerParameters) : Worker(context, parameters) {
    override fun doWork(): Result {
        val jobId = inputData.getString(KEY_JOB_ID) ?: return Result.failure()
        if (!jobId.matches(Regex("[A-Za-z0-9_-]{1,80}"))) return Result.failure()
        val uri = Uri.parse(inputData.getString(KEY_URI) ?: return Result.failure())
        val store = ResearchStore(applicationContext)
        val stagingDirectory = File(applicationContext.noBackupFilesDir, "research-imports")
        val legacyPlaintextPartial = File(stagingDirectory, "$jobId.part")
        val partial = File(stagingDirectory, "$jobId.encpart")
        var byteCount = 0L
        var finalizedFile: File? = null
        var claimedImport = false
        return try {
            check(store.startImport(jobId)) {
                "Import is no longer queued; a cancelled, running or completed job cannot be started again"
            }
            claimedImport = true
            if (isStopped || store.isJobCancelled(jobId)) {
                return markCancelled(store, jobId, partial, byteCount)
            }
            check(stagingDirectory.isDirectory || stagingDirectory.mkdirs()) {
                "Private import staging directory could not be created"
            }
            if (legacyPlaintextPartial.exists() && !legacyPlaintextPartial.delete()) {
                store.updateJob(
                    jobId, "failed",
                    message = "Legacy plaintext staging file could not be removed",
                )
                return Result.failure()
            }
            val digest = MessageDigest.getInstance("SHA-256")
            val partialPrefixDigest = MessageDigest.getInstance("SHA-256")
            val chunkContext = "kinetics-import:$jobId"
            var chunkIndex = 0L

            // Restore the plaintext digest by authenticating each retained encrypted chunk.
            LocalCrypto.ensureChunkedFileHeader(partial)
            RandomAccessFile(partial, "rw").use { input ->
                input.seek(LocalCrypto.HEADER_BYTES)
                var lastGoodOffset = LocalCrypto.HEADER_BYTES
                while (input.filePointer < input.length()) {
                    if (isStopped) return markCancelled(store, jobId, partial, byteCount)
                    val remaining = input.length() - input.filePointer
                    if (remaining < 4) {
                        input.setLength(lastGoodOffset)
                        break
                    }
                    val length = input.readInt()
                    if (length !in MIN_ENCRYPTED_CHUNK..MAX_ENCRYPTED_CHUNK) {
                        throw IllegalStateException(
                            "Encrypted staging record has an invalid length; ciphertext was preserved",
                        )
                    }
                    if (input.length() - input.filePointer < length) {
                        input.setLength(lastGoodOffset)
                        break
                    }
                    val encrypted = ByteArray(length)
                    input.readFully(encrypted)
                    val plaintext = try {
                        LocalCrypto.decrypt(encrypted, LocalCrypto.associatedData(chunkContext, chunkIndex))
                    } catch (error: Exception) {
                        throw IllegalStateException(
                            "Encrypted staging authentication failed; ciphertext was preserved",
                            error,
                        )
                    }
                    if (plaintext.isEmpty()) {
                        throw IllegalStateException(
                            "Encrypted staging contains an empty chunk; ciphertext was preserved",
                        )
                    }
                    byteCount += plaintext.size
                    if (byteCount > MAX_IMPORT_BYTES) {
                        throw IllegalArgumentException(
                            "Partial input exceeds the 512 MiB import limit; encrypted data was preserved",
                        )
                    }
                    digest.update(plaintext)
                    partialPrefixDigest.update(plaintext)
                    lastGoodOffset = input.filePointer
                    chunkIndex++
                }
            }

            val source = applicationContext.contentResolver.openInputStream(uri)
                ?: throw IllegalStateException("Selected document could not be opened")
            source.use { input ->
                val sourcePrefixDigest = MessageDigest.getInstance("SHA-256")
                var verifiedBytes = 0L
                val buffer = ByteArray(LocalCrypto.CHUNK_BYTES)

                // Re-read and hash the source prefix; never trust InputStream.skip().
                while (verifiedBytes < byteCount) {
                    if (isStopped) return markCancelled(store, jobId, partial, byteCount)
                    val wanted = minOf(buffer.size.toLong(), byteCount - verifiedBytes).toInt()
                    val count = input.read(buffer, 0, wanted)
                    if (count < 0) throw IllegalStateException("Source became shorter during resume")
                    if (count == 0) continue
                    sourcePrefixDigest.update(buffer, 0, count)
                    verifiedBytes += count
                }
                if (!MessageDigest.isEqual(partialPrefixDigest.digest(), sourcePrefixDigest.digest())) {
                    throw IllegalStateException(
                        "Source content changed since partial import; encrypted partial was preserved. " +
                            "Start a new import to use the changed source",
                    )
                }

                while (true) {
                    if (isStopped) return markCancelled(store, jobId, partial, byteCount)
                    val count = input.read(buffer)
                    if (count < 0) break
                    if (count == 0) continue
                    if (byteCount + count > MAX_IMPORT_BYTES) {
                        throw IllegalArgumentException("Input exceeds the 512 MiB import limit")
                    }
                    val chunk = buffer.copyOf(count)
                    LocalCrypto.appendEncryptedChunk(partial, chunk, LocalCrypto.associatedData(chunkContext, chunkIndex))
                    chunkIndex++
                    digest.update(chunk)
                    byteCount += count
                    store.updateProgress(jobId, byteCount)
                    setProgressAsync(androidx.work.workDataOf("bytes" to byteCount))
                }
            }

            require(byteCount > 0L) { "Empty research inputs are not accepted" }
            if (isStopped || store.isJobCancelled(jobId)) {
                return markCancelled(store, jobId, partial, byteCount)
            }
            val hash = digest.digest().joinToString("") { "%02x".format(it) }
            val encryptedDirectory = File(applicationContext.noBackupFilesDir, "research-inputs")
                .apply { mkdirs() }
            val destination = File(encryptedDirectory, "$jobId.kdat")
            check(!destination.exists() || destination.delete()) {
                "Previous encrypted import could not be replaced"
            }
            check(partial.renameTo(destination)) { "Encrypted import could not be finalized" }
            finalizedFile = destination

            if (isStopped || store.isJobCancelled(jobId)) {
                check(destination.renameTo(partial)) {
                    "Cancelled encrypted import could not be restored to its resumable partial file"
                }
                finalizedFile = null
                return markCancelled(store, jobId, partial, byteCount)
            }
            store.completeImport(jobId, hash, byteCount, destination.absolutePath)
            finalizedFile = null
            Result.success()
        } catch (error: Exception) {
            // If metadata commit fails, restore the encrypted staging file for safe retry.
            finalizedFile?.let { file ->
                if (!file.renameTo(partial)) file.delete()
            }
            finalizedFile = null
            if (!claimedImport) return Result.failure()
            if (isStopped || store.isJobCancelled(jobId)) {
                return markCancelled(store, jobId, partial, byteCount)
            }
            val detail = error.message ?: error.javaClass.simpleName
            val state = if (
                detail.startsWith("Encrypted staging") ||
                detail.startsWith("Source content changed") ||
                detail.startsWith("Partial input exceeds")
            ) {
                "recovery_required"
            } else {
                "failed"
            }
            store.updateJob(jobId, state, bytes = byteCount, message = detail)
            Result.failure()
        } finally {
            store.close()
        }
    }

    private fun markCancelled(
        store: ResearchStore, jobId: String, partial: File, byteCount: Long,
    ): Result {
        store.updateProgress(jobId, byteCount)
        store.updateJob(
            jobId, "cancelled", bytes = byteCount,
            message = "Encrypted partial import retained in app-private no-backup storage; resume is available",
        )
        return Result.failure()
    }

    companion object {
        const val KEY_JOB_ID = "job_id"
        const val KEY_URI = "input_uri"
        const val MAX_IMPORT_BYTES = 512L * 1024L * 1024L
        private const val MIN_ENCRYPTED_CHUNK = 28
        private const val MAX_ENCRYPTED_CHUNK = LocalCrypto.CHUNK_BYTES + 28
    }
}

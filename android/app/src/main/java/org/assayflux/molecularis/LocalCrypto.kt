package org.assayflux.molecularis

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.io.File
import java.io.FileOutputStream
import java.io.RandomAccessFile
import java.security.KeyStore
import java.security.MessageDigest
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

/** Android Keystore AES-256-GCM with per-chunk identity and ordering authenticated as AAD. */
object LocalCrypto {
    private const val ALIAS = "kinetics-local-data-v1"
    private const val TRANSFORMATION = "AES/GCM/NoPadding"
    private const val IV_BYTES = 12
    private const val TAG_BYTES = 16
    private const val TAG_BITS = TAG_BYTES * 8
    const val CHUNK_BYTES = 4 * 1024 * 1024
    private const val MAX_FILE_BYTES = 512L * 1024L * 1024L
    private val FILE_MAGIC = byteArrayOf(0x4b, 0x44, 0x41, 0x54)
    const val HEADER_BYTES = KdatFileHeader.HEADER_BYTES
    private const val FILE_FORMAT_VERSION = 2

    private fun key(createIfMissing: Boolean): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val existing = store.getKey(ALIAS, null) as? SecretKey
        if (existing != null) return existing
        check(createIfMissing) {
            "Android Keystore key is missing; refusing to generate a replacement for existing ciphertext"
        }
        val generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        generator.init(
            KeyGenParameterSpec.Builder(
                ALIAS, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
            ).setKeySize(256)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setRandomizedEncryptionRequired(true)
                .build(),
        )
        return generator.generateKey()
    }

    /**
     * Tri-state check for startup recovery. False means the alias is definitely absent;
     * null means the Android Keystore could not be inspected and must not trigger recovery actions.
     */
    fun existingKeyStatus(): Boolean? = try {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        store.getKey(ALIAS, null) is SecretKey
    } catch (_: Exception) {
        null
    }

    fun associatedData(context: String, chunkIndex: Long): ByteArray {
        require(context.isNotBlank() && chunkIndex >= 0) { "Invalid encrypted chunk identity" }
        return ChunkIdentity.associatedData(context, chunkIndex)
    }

    fun encrypt(
        plainText: ByteArray, associatedData: ByteArray = byteArrayOf(),
        createKeyIfMissing: Boolean = true,
    ): ByteArray {
        require(plainText.size <= CHUNK_BYTES) { "AES-GCM chunk exceeds the 4 MiB limit" }
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key(createIfMissing = createKeyIfMissing))
        if (associatedData.isNotEmpty()) cipher.updateAAD(associatedData)
        return cipher.iv + cipher.doFinal(plainText)
    }

    fun decrypt(payload: ByteArray, associatedData: ByteArray = byteArrayOf()): ByteArray {
        require(payload.size in (IV_BYTES + TAG_BYTES)..(CHUNK_BYTES + IV_BYTES + TAG_BYTES)) {
            "Encrypted chunk is truncated or exceeds the 4 MiB limit"
        }
        val iv = payload.copyOfRange(0, IV_BYTES)
        val encrypted = payload.copyOfRange(IV_BYTES, payload.size)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.DECRYPT_MODE, key(createIfMissing = false), GCMParameterSpec(TAG_BITS, iv))
        if (associatedData.isNotEmpty()) cipher.updateAAD(associatedData)
        return cipher.doFinal(encrypted)
    }

    /** Initialize a new KDAT v2 file without truncating non-empty invalid ciphertext. */
    fun ensureChunkedFileHeader(file: File) = KdatFileHeader.ensure(file)

    fun appendEncryptedChunk(file: File, plainText: ByteArray, associatedData: ByteArray) {
        require(plainText.isNotEmpty()) { "Encrypted chunks cannot be empty" }
        require(file.isFile && file.length() >= HEADER_BYTES) {
            "KDAT v2 file header must be initialized before appending encrypted chunks"
        }
        val firstChunk = file.length() == HEADER_BYTES
        val payload = encrypt(
            plainText, associatedData, createKeyIfMissing = firstChunk,
        )
        RandomAccessFile(file, "rw").use { output ->
            output.seek(output.length())
            output.writeInt(payload.size)
            output.write(payload)
            output.fd.sync()
        }
    }

    /**
     * Export a verified encrypted input to a caller-owned SAF stream.
     * A full authentication/hash pass completes before any plaintext is written.
     * The second pass re-authenticates each chunk while streaming output.
     */
    fun decryptChunkedFileToStream(
        source: File, destination: java.io.OutputStream, context: String, expectedSha256: String,
    ) {
        require(source.isFile) { "Encrypted source file does not exist" }
        require(expectedSha256.matches(Regex("[a-fA-F0-9]{64}"))) { "Expected SHA-256 is invalid" }

        fun readChunks(write: (ByteArray) -> Unit): String {
            val digest = MessageDigest.getInstance("SHA-256")
            var total = 0L
            RandomAccessFile(source, "r").use { input ->
                val magic = ByteArray(FILE_MAGIC.size)
                input.readFully(magic)
                require(magic.contentEquals(FILE_MAGIC)) { "Unsupported encrypted file format" }
                require(input.readUnsignedByte() == FILE_FORMAT_VERSION) {
                    "Unsupported encrypted file version"
                }
                var chunkIndex = 0L
                while (input.filePointer < input.length()) {
                    require(input.length() - input.filePointer >= 4) { "Encrypted chunk header is truncated" }
                    val length = input.readInt()
                    require(length in (IV_BYTES + TAG_BYTES)..(CHUNK_BYTES + IV_BYTES + TAG_BYTES)) {
                        "Encrypted chunk length is invalid"
                    }
                    require(input.length() - input.filePointer >= length) {
                        "Encrypted chunk payload is truncated"
                    }
                    val payload = ByteArray(length)
                    input.readFully(payload)
                    val plaintext = decrypt(payload, associatedData(context, chunkIndex))
                    require(plaintext.isNotEmpty()) { "Encrypted file contains an empty chunk" }
                    total += plaintext.size
                    require(total <= MAX_FILE_BYTES) { "Decrypted research input exceeds the 512 MiB limit" }
                    digest.update(plaintext)
                    write(plaintext)
                    chunkIndex++
                }
            }
            return digest.digest().joinToString("") { "%02x".format(it) }
        }

        val verifiedHash = readChunks { }
        require(verifiedHash.equals(expectedSha256, ignoreCase = true)) {
            "Decrypted input SHA-256 does not match recorded provenance"
        }
        val secondPassHash = readChunks(destination::write)
        require(secondPassHash.equals(expectedSha256, ignoreCase = true)) {
            "Encrypted input changed during export"
        }
        destination.flush()
    }

    fun decryptChunkedFile(
        source: File, destination: File, context: String, expectedSha256: String,
    ) {
        require(source.isFile) { "Encrypted source file does not exist" }
        require(expectedSha256.matches(Regex("[a-fA-F0-9]{64}"))) { "Expected SHA-256 is invalid" }
        val temporary = File(destination.parentFile, destination.name + ".tmp")
        temporary.delete()
        val digest = MessageDigest.getInstance("SHA-256")
        try {
            RandomAccessFile(source, "r").use { input ->
                val magic = ByteArray(FILE_MAGIC.size)
                input.readFully(magic)
                require(magic.contentEquals(FILE_MAGIC)) { "Unsupported encrypted file format" }
                require(input.readUnsignedByte() == FILE_FORMAT_VERSION) {
                    "Unsupported encrypted file version"
                }
                FileOutputStream(temporary, false).use { output ->
                    var chunkIndex = 0L
                    while (input.filePointer < input.length()) {
                        val remaining = input.length() - input.filePointer
                        require(remaining >= 4) { "Encrypted chunk header is truncated" }
                        val length = input.readInt()
                        require(length in (IV_BYTES + TAG_BYTES)..(CHUNK_BYTES + IV_BYTES + TAG_BYTES)) {
                            "Encrypted chunk length is invalid"
                        }
                        require(input.length() - input.filePointer >= length) {
                            "Encrypted chunk payload is truncated"
                        }
                        val payload = ByteArray(length)
                        input.readFully(payload)
                        val plaintext = decrypt(payload, associatedData(context, chunkIndex))
                        require(plaintext.isNotEmpty()) { "Encrypted file contains an empty chunk" }
                        require(output.channel.position() + plaintext.size <= MAX_FILE_BYTES) {
                            "Decrypted research input exceeds the 512 MiB limit"
                        }
                        output.write(plaintext)
                        digest.update(plaintext)
                        chunkIndex++
                    }
                    output.fd.sync()
                }
            }
            val actual = digest.digest().joinToString("") { "%02x".format(it) }
            require(actual.equals(expectedSha256, ignoreCase = true)) {
                "Decrypted input SHA-256 does not match recorded provenance"
            }
            if (destination.exists()) {
                check(destination.delete()) { "Previous decrypted output could not be replaced" }
            }
            check(temporary.renameTo(destination)) { "Decrypted file could not be finalized" }
        } catch (error: Exception) {
            temporary.delete()
            throw error
        }
    }
}

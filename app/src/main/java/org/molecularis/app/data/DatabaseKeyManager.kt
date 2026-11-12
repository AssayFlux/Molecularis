package org.molecularis.app.data

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import java.security.KeyStore
import java.security.SecureRandom
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

/**
 * Wraps a random SQLCipher passphrase with a non-exportable Android Keystore AES key.
 * The passphrase itself is never stored in plaintext preferences or source code.
 */
internal object DatabaseKeyManager {
    private const val PREFS = "astronaut_secure_database"
    private const val ENCRYPTED_PASSPHRASE = "wrapped_passphrase"
    private const val KEY_ALIAS = "org.astronaut.agi.database.wrap.v1"
    private const val TRANSFORMATION = "AES/GCM/NoPadding"
    private const val IV_BYTES = 12
    private const val TAG_BITS = 128
    private const val PASSPHRASE_BYTES = 32

    fun getPassphrase(context: Context, allowCreateOrReset: Boolean): ByteArray {
        val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val encoded = prefs.getString(ENCRYPTED_PASSPHRASE, null)
        val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        var wrappingKey = keyStore.getKey(KEY_ALIAS, null) as? SecretKey

        if (encoded != null && wrappingKey != null) {
            try {
                val blob = Base64.decode(encoded, Base64.NO_WRAP)
                require(blob.size > IV_BYTES) { "Encrypted database key record is corrupt." }
                val iv = blob.copyOfRange(0, IV_BYTES)
                val ciphertext = blob.copyOfRange(IV_BYTES, blob.size)
                val cipher = Cipher.getInstance(TRANSFORMATION)
                cipher.init(Cipher.DECRYPT_MODE, wrappingKey, GCMParameterSpec(TAG_BITS, iv))
                return cipher.doFinal(ciphertext)
            } catch (error: Exception) {
                check(allowCreateOrReset) {
                    "The encrypted database key record cannot be opened. Existing encrypted chats will not be overwritten."
                }
                check(prefs.edit().remove(ENCRYPTED_PASSPHRASE).commit()) {
                    "Could not reset the damaged database key record."
                }
            }
        }

        check(allowCreateOrReset) {
            "The encrypted database key is unavailable. Refusing to create a new key because that would make existing chats unreadable."
        }

        if (encoded != null && wrappingKey == null) {
            check(prefs.edit().remove(ENCRYPTED_PASSPHRASE).commit()) {
                "Could not reset the unavailable database key record."
            }
        }

        if (wrappingKey == null) {
            val generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
            generator.init(
                KeyGenParameterSpec.Builder(
                    KEY_ALIAS,
                    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
                )
                    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                    .setRandomizedEncryptionRequired(true)
                    .build()
            )
            wrappingKey = generator.generateKey()
        }

        val passphrase = ByteArray(PASSPHRASE_BYTES).also(SecureRandom()::nextBytes)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, wrappingKey)
        val encrypted = cipher.iv + cipher.doFinal(passphrase)
        check(
            prefs.edit()
                .putString(ENCRYPTED_PASSPHRASE, Base64.encodeToString(encrypted, Base64.NO_WRAP))
                .commit()
        ) { "Could not persist the wrapped database key." }
        return passphrase
    }
}

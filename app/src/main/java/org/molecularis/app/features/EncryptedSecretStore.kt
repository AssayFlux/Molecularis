package org.molecularis.app.features

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

/** Stores API credentials as AES-GCM ciphertext; the AES key is non-exportable in Android Keystore. */
class EncryptedSecretStore(context: Context, private val alias: String = DEFAULT_ALIAS) {
    private val prefs = context.applicationContext.getSharedPreferences("astronaut_secure_secrets", Context.MODE_PRIVATE)

    fun put(name: String, value: String) {
        require(name.matches(Regex("^[a-zA-Z0-9._-]{1,80}$")))
        require(value.isNotBlank())
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, getOrCreateKey())
        cipher.updateAAD(name.toByteArray(Charsets.UTF_8))
        val encrypted = cipher.doFinal(value.toByteArray(Charsets.UTF_8))
        val encoded = Base64.encodeToString(cipher.iv, Base64.NO_WRAP) + "." +
            Base64.encodeToString(encrypted, Base64.NO_WRAP)
        check(prefs.edit().putString(name, encoded).commit()) { "Could not save encrypted credential." }
    }

    fun get(name: String): String? {
        val stored = prefs.getString(name, null) ?: return null
        val parts = stored.split('.', limit = 2)
        require(parts.size == 2) { "Stored credential is corrupted." }
        val iv = Base64.decode(parts[0], Base64.NO_WRAP)
        val ciphertext = Base64.decode(parts[1], Base64.NO_WRAP)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.DECRYPT_MODE, getOrCreateKey(), GCMParameterSpec(128, iv))
        cipher.updateAAD(name.toByteArray(Charsets.UTF_8))
        return String(cipher.doFinal(ciphertext), Charsets.UTF_8)
    }

    fun remove(name: String) {
        prefs.edit().remove(name).apply()
    }

    private fun getOrCreateKey(): SecretKey {
        val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (keyStore.getKey(alias, null) as? SecretKey)?.let { return it }
        val generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        generator.init(
            KeyGenParameterSpec.Builder(
                alias,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            ).setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setRandomizedEncryptionRequired(true)
                .build()
        )
        return generator.generateKey()
    }

    companion object {
        private const val DEFAULT_ALIAS = "astronaut.online.provider.key"
        private const val TRANSFORMATION = "AES/GCM/NoPadding"
    }
}

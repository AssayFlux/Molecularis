package org.molecularis.app.features

import android.content.Context
import android.util.Base64
import java.security.MessageDigest
import java.security.SecureRandom
import javax.crypto.SecretKeyFactory
import javax.crypto.spec.PBEKeySpec

/** A salted PBKDF2 verifier encrypted at rest by an AES-GCM Android Keystore key. */
class AppLockCredentialStore(context: Context) {
    private val secrets = EncryptedSecretStore(context, "molecularis.app-lock.credentials.key")

    fun isConfigured(): Boolean = secrets.get(SALT_KEY) != null && secrets.get(VERIFIER_KEY) != null

    fun setCredential(credential: CharArray) {
        require(credential.size in 6..128) { "Use between 6 and 128 characters." }
        val salt = ByteArray(16).also { SecureRandom().nextBytes(it) }
        val verifier = derive(credential, salt)
        try {
            secrets.put(SALT_KEY, Base64.encodeToString(salt, Base64.NO_WRAP))
            secrets.put(VERIFIER_KEY, Base64.encodeToString(verifier, Base64.NO_WRAP))
        } finally {
            credential.fill(' ')
            verifier.fill(0)
        }
    }

    fun verify(credential: CharArray): Boolean {
        val saltValue = secrets.get(SALT_KEY)
        val verifierValue = secrets.get(VERIFIER_KEY)
        if (saltValue == null || verifierValue == null) {
            credential.fill(' ')
            return false
        }
        return try {
            val expected = Base64.decode(verifierValue, Base64.NO_WRAP)
            val actual = derive(credential, Base64.decode(saltValue, Base64.NO_WRAP))
            try { MessageDigest.isEqual(expected, actual) }
            finally { expected.fill(0); actual.fill(0) }
        } finally {
            credential.fill(' ')
        }
    }

    fun clear() {
        secrets.remove(SALT_KEY)
        secrets.remove(VERIFIER_KEY)
    }

    private fun derive(credential: CharArray, salt: ByteArray): ByteArray {
        val spec = PBEKeySpec(credential, salt, ITERATIONS, 256)
        return try {
            SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).encoded
        } finally {
            spec.clearPassword()
        }
    }

    private companion object {
        const val SALT_KEY = "app_lock_salt"
        const val VERIFIER_KEY = "app_lock_verifier"
        const val ITERATIONS = 210_000
    }
}

package org.molecularis.app

import android.os.Bundle
import android.os.Build
import android.view.WindowManager
import androidx.activity.compose.setContent
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import org.molecularis.app.features.AppLockCredentialStore
import org.molecularis.app.ui.MessengerApp

class MainActivity : FragmentActivity() {
    private var unlocked by mutableStateOf(false)
    private var unlockMessage by mutableStateOf("Enter your app PIN or use biometrics.")
    private var pinEntry by mutableStateOf("")
    private var promptActive = false
    private lateinit var credentialStore: AppLockCredentialStore

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        credentialStore = AppLockCredentialStore(this)
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE)
        setContent {
            if (unlocked) {
                MessengerApp()
            } else {
                MaterialTheme {
                    Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                        Column(Modifier.fillMaxSize().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                            Text("MOLECULARIS", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.height(12.dp))
                            Text("Workspace locked", style = MaterialTheme.typography.headlineSmall)
                            Spacer(Modifier.height(8.dp))
                            Text(unlockMessage, style = MaterialTheme.typography.bodyMedium)
                            if (credentialStore.isConfigured()) {
                                Spacer(Modifier.height(20.dp))
                                OutlinedTextField(
                                    value = pinEntry,
                                    onValueChange = { pinEntry = it.take(128) },
                                    label = { Text("App PIN / password") },
                                    singleLine = true,
                                    visualTransformation = PasswordVisualTransformation(),
                                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                                    modifier = Modifier.fillMaxWidth()
                                )
                                Spacer(Modifier.height(8.dp))
                                Button(
                                    onClick = {
                                        val valid = runCatching { credentialStore.verify(pinEntry.toCharArray()) }.getOrDefault(false)
                                        pinEntry = ""
                                        if (valid) { unlockMessage = "Workspace unlocked."; unlocked = true }
                                        else unlockMessage = "Incorrect PIN or password. Try again or use biometrics."
                                    },
                                    enabled = pinEntry.length >= 6,
                                    modifier = Modifier.fillMaxWidth()
                                ) { Text("Unlock with PIN / password") }
                            }
                            if (getSharedPreferences("molecularis_security", MODE_PRIVATE).getBoolean("biometric_lock_enabled", false)) {
                                Spacer(Modifier.height(8.dp))
                                OutlinedButton(onClick = { requestUnlock() }, enabled = !promptActive, modifier = Modifier.fillMaxWidth()) {
                                    Text("Use fingerprint / device lock")
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        val prefs = getSharedPreferences("molecularis_security", MODE_PRIVATE)
        val locked = prefs.getBoolean("app_lock_enabled", false) || prefs.getBoolean("biometric_lock_enabled", false)
        if (locked) {
            unlocked = false
            if (prefs.getBoolean("biometric_lock_enabled", false)) requestUnlock()
        } else unlocked = true
    }

    override fun onPause() {
        val prefs = getSharedPreferences("molecularis_security", MODE_PRIVATE)
        if (prefs.getBoolean("app_lock_enabled", false) || prefs.getBoolean("biometric_lock_enabled", false)) unlocked = false
        super.onPause()
    }

    private fun requestUnlock() {
        if (promptActive) return
        val authenticators = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            BiometricManager.Authenticators.BIOMETRIC_STRONG or BiometricManager.Authenticators.DEVICE_CREDENTIAL
        } else BiometricManager.Authenticators.BIOMETRIC_STRONG
        if (BiometricManager.from(this).canAuthenticate(authenticators) != BiometricManager.BIOMETRIC_SUCCESS) {
            unlockMessage = "Biometrics are unavailable. Use your app PIN / password instead."
            return
        }
        promptActive = true
        val prompt = BiometricPrompt(this, ContextCompat.getMainExecutor(this), object : BiometricPrompt.AuthenticationCallback() {
            override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                promptActive = false
                unlockMessage = "Workspace unlocked."
                unlocked = true
            }
            override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                promptActive = false
                unlockMessage = errString.toString() + " You can enter your app PIN / password."
            }
            override fun onAuthenticationFailed() {
                unlockMessage = "That biometric was not recognized. Try again or enter your app PIN."
            }
        })
        val info = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Unlock Molecularis")
            .setSubtitle(if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) "Use your fingerprint or device screen lock" else "Use your fingerprint")
            .setAllowedAuthenticators(authenticators)
            .build()
        prompt.authenticate(info)
    }
}

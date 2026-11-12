package org.molecularis.app

import android.os.Bundle
import android.os.Build
import android.view.WindowManager
import androidx.activity.compose.setContent
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import org.molecularis.app.ui.MessengerApp

class MainActivity : FragmentActivity() {
    private var unlocked by mutableStateOf(false)
    private var unlockMessage by mutableStateOf("Authenticate to open your Molecularis workspace.")
    private var promptActive = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE)
        setContent {
            if (unlocked) {
                MessengerApp()
            } else {
                MaterialTheme {
                    Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                        Column(
                            Modifier.fillMaxSize().padding(24.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Text("MOLECULARIS", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.height(12.dp))
                            Text("Workspace locked", style = MaterialTheme.typography.headlineSmall)
                            Spacer(Modifier.height(8.dp))
                            Text(unlockMessage, style = MaterialTheme.typography.bodyMedium)
                            Spacer(Modifier.height(20.dp))
                            Button(onClick = { requestUnlock() }, enabled = !promptActive) { Text("Unlock with biometrics") }
                        }
                    }
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        val enabled = getSharedPreferences("molecularis_security", MODE_PRIVATE)
            .getBoolean("biometric_lock_enabled", false)
        if (enabled) {
            unlocked = false
            requestUnlock()
        } else {
            unlocked = true
        }
    }

    override fun onPause() {
        if (getSharedPreferences("molecularis_security", MODE_PRIVATE)
                .getBoolean("biometric_lock_enabled", false)) {
            unlocked = false
        }
        super.onPause()
    }

    private fun requestUnlock() {
        if (promptActive) return
        val authenticators = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            BiometricManager.Authenticators.BIOMETRIC_STRONG or BiometricManager.Authenticators.DEVICE_CREDENTIAL
        } else {
            BiometricManager.Authenticators.BIOMETRIC_STRONG
        }
        val availability = BiometricManager.from(this).canAuthenticate(authenticators)
        if (availability != BiometricManager.BIOMETRIC_SUCCESS) {
            unlockMessage = "Biometric or secure device-lock authentication is unavailable. Disable the app lock from device settings or enroll a supported method."
            return
        }
        promptActive = true
        val prompt = BiometricPrompt(
            this,
            ContextCompat.getMainExecutor(this),
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                    promptActive = false
                    unlockMessage = "Workspace unlocked."
                    unlocked = true
                }
                override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                    promptActive = false
                    unlockMessage = errString.toString()
                }
                override fun onAuthenticationFailed() {
                    unlockMessage = "That biometric was not recognized. Try again."
                }
            }
        )
        val info = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Unlock Molecularis")
            .setSubtitle(if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) "Use your fingerprint or device screen lock" else "Use your fingerprint")
            .setAllowedAuthenticators(authenticators)
            .build()
        prompt.authenticate(info)
    }
}

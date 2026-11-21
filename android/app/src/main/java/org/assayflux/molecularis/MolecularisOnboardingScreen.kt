package org.assayflux.molecularis

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import org.assayflux.designsystem.MolecularisPrimaryButton
import org.assayflux.designsystem.MolecularisTokens
import org.assayflux.designsystem.MolecularisTypography

/** First-run orientation for the real on-device workspace; not an account or cloud setup. */
@Composable
internal fun MolecularisOnboardingScreen(
    themeFamily: String,
    onComplete: () -> Unit,
) {
    var acknowledged by rememberSaveable { mutableStateOf(false) }
    val isDark = when (themeFamily) {
        "dark" -> true
        "light" -> false
        else -> isSystemInDarkTheme()
    }
    val palette = if (isDark) MolecularisTokens.MolecularisDarkClassic else MolecularisTokens.MolecularisLightClassic
    val scheme = if (isDark) {
        darkColorScheme(
            primary = palette.primary, onPrimary = palette.background,
            secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface,
            onSurface = palette.text, onBackground = palette.text,
            surfaceVariant = palette.surfaceAlt, onSurfaceVariant = palette.muted,
            outline = palette.outline, error = MolecularisTokens.StatusDark.error,
        )
    } else {
        lightColorScheme(
            primary = palette.primary, onPrimary = Color.White,
            secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface,
            onSurface = palette.text, onBackground = palette.text,
            surfaceVariant = palette.surfaceAlt, onSurfaceVariant = palette.muted,
            outline = palette.outline, error = MolecularisTokens.StatusLight.error,
        )
    }
    MaterialTheme(colorScheme = scheme, typography = MolecularisTypography) {
        Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
            Column(
                Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Column(
                    Modifier.fillMaxWidth().widthIn(max = 520.dp),
                    verticalArrangement = Arrangement.spacedBy(20.dp),
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("MOLECULARIS", style = MaterialTheme.typography.labelLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.SemiBold)
                        Text("Your research workspace.", style = MaterialTheme.typography.headlineLarge,
                            color = MaterialTheme.colorScheme.onSurface)
                        Text("A local-first computational research environment.",
                            style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    OutlinedCard(shape = RoundedCornerShape(12.dp)) {
                        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Text("LOCAL BY DESIGN", style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold)
                            Text("Research inputs are imported through Android's document picker and stored in this app's private workspace. Input encryption and integrity checks are applied by the import workflow.",
                                style = MaterialTheme.typography.bodyMedium)
                            Text("No cloud account or remote processing is configured by this onboarding flow. Files leave the device only when you explicitly export them.",
                                style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                    OutlinedCard(shape = RoundedCornerShape(12.dp)) {
                        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text("RESEARCH MODE ONLY", style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold)
                            Text("Use synthetic fixtures and appropriately licensed, non-patient research resources only. Do not import patient or clinical records.",
                                style = MaterialTheme.typography.bodyMedium)
                            Text("Molecularis does not provide diagnosis, patient-specific interpretation, treatment selection or dosing advice. Clinical functionality is not authorised.",
                                style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = acknowledged, onCheckedChange = { acknowledged = it })
                        Text("I understand the local-storage and Research Mode boundaries.",
                            modifier = Modifier.weight(1f), style = MaterialTheme.typography.bodyMedium)
                    }
                    MolecularisPrimaryButton(
                        label = "Continue to workspace",
                        onClick = onComplete,
                        enabled = acknowledged,
                        modifier = Modifier.fillMaxWidth(),
                    )
                    Spacer(Modifier.height(4.dp))
                    Text("You can review these boundaries in Settings. This is not a sign-in or identity-verification step.",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}

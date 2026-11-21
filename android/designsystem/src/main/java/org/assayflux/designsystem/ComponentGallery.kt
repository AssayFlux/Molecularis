package org.assayflux.designsystem

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/** Development-only live gallery for the owner V1 semantic system and reusable controls. */
@Composable
fun MolecularisComponentGallery() {
    val palettes = listOf(
        "Light" to (MolecularisTokens.MolecularisLightClassic to false),
        "Dark" to (MolecularisTokens.MolecularisDarkClassic to true),
    )
    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp),
    ) {
        item {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("KINETICS", style = MaterialTheme.typography.labelMedium)
                Text("Component gallery", style = MaterialTheme.typography.headlineMedium)
                Text(
                    "Owner V1 · monochrome · native Compose",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
        items(palettes, key = { it.first }) { (name, entry) ->
            val (palette, isDark) = entry
            val scheme = if (!isDark) {
                lightColorScheme(
                    primary = palette.primary, onPrimary = palette.background,
                    secondary = palette.secondary, tertiary = palette.tertiary,
                    background = palette.background, surface = palette.surface,
                    onSurface = palette.text, onBackground = palette.text,
                    surfaceVariant = palette.surfaceAlt, onSurfaceVariant = palette.muted,
                    outline = palette.outline,
                )
            } else {
                darkColorScheme(
                    primary = palette.primary, onPrimary = palette.background,
                    secondary = palette.secondary, tertiary = palette.tertiary,
                    background = palette.background, surface = palette.surface,
                    onSurface = palette.text, onBackground = palette.text,
                    surfaceVariant = palette.surfaceAlt, onSurfaceVariant = palette.muted,
                    outline = palette.outline,
                )
            }
            MaterialTheme(colorScheme = scheme, typography = MolecularisTypography) {
                var field by remember(name) { mutableStateOf("") }
                var pressed by remember(name) { mutableStateOf(false) }
                var chipSelected by remember(name) { mutableStateOf(false) }
                var showDialog by remember(name) { mutableStateOf(false) }
                var showSheet by remember(name) { mutableStateOf(false) }
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("$name appearance", style = MaterialTheme.typography.titleLarge)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Surface(
                            modifier = Modifier.weight(1f),
                            color = palette.primary,
                            shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp),
                        ) {
                            Text("Primary", Modifier.padding(12.dp), color = palette.background)
                        }
                        Surface(
                            modifier = Modifier.weight(1f),
                            color = palette.surfaceAlt,
                            shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp),
                        ) {
                            Text("Secondary", Modifier.padding(12.dp), color = palette.text)
                        }
                    }
                    MolecularisPrimaryButton(
                        label = if (pressed) "Action acknowledged" else "Primary action",
                        onClick = { pressed = !pressed },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    MolecularisSecondaryButton(
                        label = "Secondary action",
                        onClick = { field = "Secondary action selected" },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    MolecularisField(
                        value = field,
                        onValueChange = { field = it },
                        label = "Example input",
                        supportingText = "52 dp target · 10 dp radius",
                    )
                    MolecularisStatus(label = "Research Mode · local")
                    MolecularisDivider()
                    MolecularisListRow(
                        title = "Reusable list row",
                        supportingText = "56 dp minimum · optional leading and trailing slots",
                        trailing = { MolecularisStatus("Local") },
                        onClick = { pressed = !pressed },
                    )
                    MolecularisChip("Selected state", chipSelected, { chipSelected = !chipSelected })
                    MolecularisSecondaryButton("Preview confirmation dialog", { showDialog = true }, Modifier.fillMaxWidth())
                    MolecularisSecondaryButton("Preview bottom sheet", { showSheet = true }, Modifier.fillMaxWidth())
                }
                if (showDialog) MolecularisConfirmationDialog(
                    title = "Component preview",
                    message = "This is a reusable confirmation pattern. No data is changed by this gallery.",
                    confirmLabel = "Got it", dismissLabel = "Close",
                    onConfirm = { showDialog = false }, onDismiss = { showDialog = false },
                )
                if (showSheet) MolecularisBottomSheet(onDismissRequest = { showSheet = false }) {
                    Text("Contextual actions", style = MaterialTheme.typography.titleLarge)
                    Text("A restrained 20 dp top-corner sheet with 20 dp content padding.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant)
                    MolecularisPrimaryButton("Close sheet", { showSheet = false }, Modifier.fillMaxWidth())
                }
            }
        }
    }
}

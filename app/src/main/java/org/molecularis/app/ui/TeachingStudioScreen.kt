package org.molecularis.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import java.io.File

@Composable
fun TeachingStudioScreen() {
    val context = LocalContext.current
    var topic by remember { mutableStateOf("") }
    var level by remember { mutableStateOf("MBBS") }
    var minutes by remember { mutableFloatStateOf(30f) }
    var outline by remember { mutableStateOf("") }
    var status by remember { mutableStateOf("") }

    Column(
        modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(18.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.72f))) {
            Column(Modifier.fillMaxWidth().padding(18.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("MOLECULARIS TEACHING STUDIO", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Text("Turn a topic into a lesson.", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text("Choose the learner level and available time. Molecularis will prepare an editable teaching structure that can later be grounded in your imported books and local AI model.", style = MaterialTheme.typography.bodyMedium)
            }
        }

        OutlinedTextField(
            value = topic,
            onValueChange = { topic = it; outline = ""; status = "" },
            modifier = Modifier.fillMaxWidth(),
            label = { Text("Biochemistry topic") },
            placeholder = { Text("e.g. Glycolysis and its regulation") },
            minLines = 2
        )

        Text("Learner level", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf("MBBS", "MD / DNB", "PhD").forEach { option ->
                FilterChip(selected = level == option, onClick = { level = option; outline = "" }, label = { Text(option) })
            }
        }

        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Teaching time", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Text(minutes.toInt().toString() + " min", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
        }
        Slider(value = minutes, onValueChange = { minutes = it }, valueRange = 10f..90f, steps = 15)

        Button(
            onClick = {
                val cleanTopic = topic.trim()
                if (cleanTopic.isEmpty()) {
                    status = "Enter a topic to prepare a lesson."
                } else {
                    val depth = when (level) {
                        "PhD" -> "Molecular mechanisms, experimental evidence, regulation, pathway integration and research questions"
                        "MD / DNB" -> "Advanced mechanisms, clinical correlations, interpretation and applied problem-solving"
                        else -> "Core concepts, pathway logic, physiological context and clinical relevance"
                    }
                    outline = listOf(
                        "LESSON: " + cleanTopic,
                        "AUDIENCE: " + level,
                        "DURATION: " + minutes.toInt() + " minutes",
                        "",
                        "1. Learning outcomes",
                        "   - Define the central concepts and terminology",
                        "   - Explain the sequence of events and the underlying biochemical logic",
                        "   - Relate regulation to physiological and clinical context",
                        "",
                        "2. Prerequisites and orientation",
                        "   - Identify the essential molecules, compartments and prior concepts",
                        "   - Introduce the central question that the lesson will answer",
                        "",
                        "3. Core explanation",
                        "   - Build the mechanism in a clear stepwise sequence",
                        "   - Explain why each step occurs, not only what happens",
                        "   - Highlight key enzymes, substrates, products and control points",
                        "",
                        "4. Regulation and integration",
                        "   - Explain major regulatory signals and rate-controlling steps",
                        "   - Connect the topic with related metabolic pathways",
                        "",
                        "5. Clinical and applied relevance",
                        "   - Discuss relevant disorders, laboratory findings or therapeutic links",
                        "   - Work through one applied example appropriate to " + level,
                        "",
                        "6. Visual teaching plan",
                        "   - Create an overview diagram",
                        "   - Reveal the mechanism progressively, emphasizing control points",
                        "",
                        "7. Recap and retrieval",
                        "   - Summarize the three most important ideas",
                        "   - Ask short-answer and application questions",
                        "",
                        "TEACHING EMPHASIS: " + depth,
                        "",
                        "DRAFT STATUS: Structure generated locally. Populate and verify scientific detail against the professor's library before teaching."
                    ).joinToString("\n")
                    status = "Editable lesson structure prepared locally. Scientific content still needs source grounding and professor review."
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = topic.isNotBlank()
        ) {
            Icon(Icons.Default.AutoAwesome, contentDescription = null)
            Spacer(Modifier.width(8.dp))
            Text("Prepare lesson structure")
        }

        if (outline.isNotBlank()) {
            Card {
                Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("Your lesson outline", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Text(outline, style = MaterialTheme.typography.bodyMedium)
                    OutlinedButton(
                        onClick = {
                            runCatching {
                                val directory = File(context.filesDir, "lessons").apply { mkdirs() }
                                val safeName = topic.trim().lowercase().replace(Regex("[^a-z0-9]+"), "-").trim('-').take(48).ifBlank { "lesson" }
                                File(directory, safeName + "-" + System.currentTimeMillis() + ".md").writeText(outline)
                            }.onSuccess { status = "Lesson outline saved on this device." }
                                .onFailure { status = "Could not save outline: " + (it.message ?: "unknown error") }
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Icon(Icons.Default.Save, contentDescription = null)
                        Spacer(Modifier.width(8.dp))
                        Text("Save outline on this device")
                    }
                }
            }
        }
        if (status.isNotBlank()) Text(status, color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.bodySmall)
        Text("Next layers: import your textbooks, ground lesson sections in retrieved passages, generate editable slides, assemble progressive SVG diagrams and synchronize offline narration.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

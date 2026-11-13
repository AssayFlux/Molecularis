package org.molecularis.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun MolecularisDashboardScreen(
    bookCount: Int,
    reviewedBookCount: Int,
    chatCount: Int,
    modelCount: Int,
    activeModelName: String?,
    onNavigate: (String) -> Unit
) {
    Column(
        Modifier.fillMaxSize().padding(horizontal = 18.dp, vertical = 14.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Card(
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
            shape = MaterialTheme.shapes.extraLarge
        ) {
            Column(Modifier.fillMaxWidth().padding(22.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("YOUR BIOCHEMISTRY TEACHING WORKSPACE", style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Text("Teach with clarity.\nLearn from trusted sources.",
                    style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onPrimaryContainer)
                Text("Build lessons from reviewed textbooks, explain mechanisms visually and deliver offline teaching sessions.",
                    style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onPrimaryContainer)
                Button(onClick = { onNavigate("teach") }, modifier = Modifier.fillMaxWidth()) {
                    Icon(Icons.Default.School, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                    Text("Open Teaching Studio")
                }
            }
        }
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            DashboardMetric("Library", bookCount.toString(), Icons.Default.MenuBook, Modifier.weight(1f))
            DashboardMetric("Reviewed", reviewedBookCount.toString(), Icons.Default.Verified, Modifier.weight(1f))
            DashboardMetric("Chats", chatCount.toString(), Icons.Default.ChatBubbleOutline, Modifier.weight(1f))
            DashboardMetric("Models", modelCount.toString(), Icons.Default.Memory, Modifier.weight(1f))
        }
        Text("Workspace", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
        val actions = listOf(
            DashboardAction("Textbook Library", "Import and manage source PDFs", Icons.Default.MenuBook, "library"),
            DashboardAction("Knowledge Pool", "Review OCR, topics and citations", Icons.Default.AccountTree, "knowledge"),
            DashboardAction("Ask Molecularis", "Discuss concepts and source passages", Icons.Default.Chat, "chat"),
            DashboardAction("Scheduled Teaching", "Queue an offline lecture", Icons.Default.Schedule, "schedule"),
            DashboardAction("AI Models", "Manage local inference models", Icons.Default.Memory, "models"),
            DashboardAction("Settings", "Appearance, speech and privacy", Icons.Default.Settings, "settings")
        )
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.fillMaxWidth().weight(1f),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            items(actions) { action ->
                Card(
                    onClick = { onNavigate(action.destination) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = MaterialTheme.shapes.large,
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Column(Modifier.fillMaxWidth().padding(15.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Icon(action.icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(25.dp))
                        Text(action.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                        Text(action.subtitle, style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
        if (activeModelName == null) {
            Text("Offline AI is not active yet. Import a compatible LiteRT-LM model in AI Models to enable local generation.",
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        } else {
            Text("Local model ready · $activeModelName", style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
private fun DashboardMetric(label: String, value: String, icon: androidx.compose.ui.graphics.vector.ImageVector, modifier: Modifier = Modifier) {
    Card(modifier, colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
        Column(Modifier.fillMaxWidth().padding(vertical = 12.dp, horizontal = 8.dp),
            horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
            Text(value, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

private data class DashboardAction(
    val title: String,
    val subtitle: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val destination: String
)

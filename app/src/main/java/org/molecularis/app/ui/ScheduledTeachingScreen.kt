package org.molecularis.app.ui

import android.Manifest
import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import kotlinx.coroutines.launch
import org.molecularis.app.data.AppDatabase
import org.molecularis.app.data.ScheduledLectureEntity
import org.molecularis.app.features.ScheduledLecturePolicy
import org.molecularis.app.features.ScheduledLectureScheduler
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale
import java.util.UUID

@Composable
fun ScheduledTeachingScreen(database: AppDatabase) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val lessons by database.lessonDao().lessons().collectAsState(initial = emptyList())
    val scheduled by database.scheduledLectureDao().lectures().collectAsState(initial = emptyList())
    var selectedLessonId by remember(lessons) { mutableStateOf(lessons.firstOrNull()?.id.orEmpty()) }
    var scheduledAt by remember { mutableLongStateOf(System.currentTimeMillis() + 3_600_000L) }
    var duration by remember { mutableStateOf("45") }
    var language by remember { mutableStateOf(Locale.getDefault().toLanguageTag().ifBlank { "en-US" }) }
    var audience by remember { mutableStateOf("MBBS") }
    var message by remember { mutableStateOf("Choose a saved lesson and schedule a local offline narration.") }

    val scheduleNow: () -> Unit = {
        scope.launch {
            val lesson = lessons.firstOrNull { it.id == selectedLessonId }
            val minutes = duration.toIntOrNull() ?: -1
            val validation = ScheduledLecturePolicy.validate(
                lesson?.title.orEmpty(), minutes, language, scheduledAt, System.currentTimeMillis()
            )
            if (validation != null) {
                message = validation
            } else if (lesson == null) {
                message = "Save a lesson in Teaching Studio before scheduling it."
            } else {
                val row = ScheduledLectureEntity(
                    id = UUID.randomUUID().toString(),
                    lessonId = lesson.id,
                    title = lesson.title,
                    audienceLevel = audience,
                    durationMinutes = minutes,
                    languageTag = language.trim(),
                    scheduledAt = scheduledAt
                )
                runCatching {
                    database.scheduledLectureDao().save(row)
                    val workId = ScheduledLectureScheduler.enqueue(context, row)
                    database.scheduledLectureDao().save(row.copy(workId = workId.toString()))
                }.onSuccess {
                    message = "Lecture scheduled. Android will run the offline narration at the selected time when system conditions allow."
                }.onFailure {
                    message = "Could not schedule lecture: ${it.message ?: "unknown error"}"
                }
            }
        }
    }

    val notificationPermission = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) scheduleNow() else message = "Notifications are required for visible scheduled-lecture playback. Enable them in Android Settings."
    }

    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Text("Scheduled teaching", style = MaterialTheme.typography.headlineSmall)
        Text("Schedule a saved lesson for offline narration. Android may defer the start slightly under Doze, battery saver or OEM background limits.", style = MaterialTheme.typography.bodyMedium)
        if (lessons.isEmpty()) {
            Text("No saved lessons yet. Prepare and save a lesson in Teaching Studio first.", color = MaterialTheme.colorScheme.error)
        } else {
            Text("Saved lesson", style = MaterialTheme.typography.titleMedium)
            lessons.forEach { lesson ->
                FilterChip(
                    selected = selectedLessonId == lesson.id,
                    onClick = { selectedLessonId = lesson.id; audience = lesson.audienceLevel },
                    label = { Text(lesson.title, maxLines = 1) }
                )
            }
        }
        Text("Audience", style = MaterialTheme.typography.titleMedium)
        Row(Modifier.horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf("MBBS", "MD", "DNB", "PhD").forEach { level ->
                FilterChip(selected = audience == level, onClick = { audience = level }, label = { Text(level) })
            }
        }
        Text("Duration (minutes)", style = MaterialTheme.typography.titleMedium)
        OutlinedTextField(value = duration, onValueChange = { duration = it.filter(Char::isDigit).take(3) }, singleLine = true)
        Text("Narration language tag", style = MaterialTheme.typography.titleMedium)
        OutlinedTextField(value = language, onValueChange = { language = it.take(35) }, singleLine = true, placeholder = { Text("en-US") })
        val formattedTime = remember(scheduledAt) { SimpleDateFormat("EEE, d MMM yyyy • HH:mm", Locale.getDefault()).format(scheduledAt) }
        Text("Start time", style = MaterialTheme.typography.titleMedium)
        OutlinedButton(onClick = {
            val initial = Calendar.getInstance().apply { timeInMillis = scheduledAt }
            DatePickerDialog(context, { _, year, month, day ->
                val chosen = Calendar.getInstance().apply {
                    timeInMillis = scheduledAt
                    set(Calendar.YEAR, year); set(Calendar.MONTH, month); set(Calendar.DAY_OF_MONTH, day)
                }
                TimePickerDialog(context, { _, hour, minute ->
                    chosen.set(Calendar.HOUR_OF_DAY, hour); chosen.set(Calendar.MINUTE, minute); chosen.set(Calendar.SECOND, 0)
                    scheduledAt = chosen.timeInMillis
                }, initial.get(Calendar.HOUR_OF_DAY), initial.get(Calendar.MINUTE), true).show()
            }, initial.get(Calendar.YEAR), initial.get(Calendar.MONTH), initial.get(Calendar.DAY_OF_MONTH)).show()
        }) { Text(formattedTime) }

        Button(
            onClick = {
                if (Build.VERSION.SDK_INT >= 33 &&
                    ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
                ) notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS) else scheduleNow()
            },
            enabled = lessons.isNotEmpty(),
            modifier = Modifier.fillMaxWidth()
        ) { Text("Schedule offline lecture") }
        Text(message, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.secondary)

        HorizontalDivider()
        Text("Schedule history", style = MaterialTheme.typography.titleLarge)
        if (scheduled.isEmpty()) Text("No scheduled lectures yet.")
        scheduled.sortedByDescending { it.scheduledAt }.forEach { row ->
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(row.title, style = MaterialTheme.typography.titleMedium)
                    Text("${SimpleDateFormat("EEE, d MMM yyyy • HH:mm", Locale.getDefault()).format(row.scheduledAt)} · ${row.audienceLevel} · ${row.durationMinutes} min")
                    Text("Status: ${row.status}", color = MaterialTheme.colorScheme.secondary)
                    if (row.lastError != null) Text(row.lastError, color = MaterialTheme.colorScheme.error)
                    if (row.status == "scheduled") {
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            TextButton(onClick = {
                                scope.launch {
                                    val immediate = row.copy(scheduledAt = System.currentTimeMillis(), status = "scheduled", lastError = null)
                                    database.scheduledLectureDao().save(immediate)
                                    val workId = ScheduledLectureScheduler.enqueue(context, immediate)
                                    database.scheduledLectureDao().save(immediate.copy(workId = workId.toString()))
                                }
                            }) { Text("Start now") }
                            TextButton(onClick = {
                                scope.launch {
                                    ScheduledLectureScheduler.cancel(context, row.id)
                                    database.scheduledLectureDao().updateStatus(row.id, "cancelled", null)
                                }
                            }) { Text("Cancel") }
                        }
                    } else if (row.status == "running") {
                        TextButton(onClick = {
                            scope.launch {
                                ScheduledLectureScheduler.cancel(context, row.id)
                                database.scheduledLectureDao().updateStatus(row.id, "cancelled", null)
                            }
                        }) { Text("Stop lecture") }
                    }
                }
            }
        }
    }
}

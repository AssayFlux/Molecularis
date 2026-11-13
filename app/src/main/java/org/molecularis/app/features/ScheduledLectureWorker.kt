package org.molecularis.app.features

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.BroadcastReceiver
import android.media.AudioManager
import android.media.AudioFocusRequest
import android.os.StatFs
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioAttributes
import android.os.Build
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import androidx.work.CoroutineWorker
import androidx.work.ExistingWorkPolicy
import androidx.work.ForegroundInfo
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import androidx.work.workDataOf
import org.molecularis.app.MainActivity
import org.molecularis.app.R
import org.molecularis.app.data.DatabaseProvider
import org.molecularis.app.data.ScheduledLectureEntity
import java.util.Locale
import java.util.UUID
import java.util.concurrent.TimeUnit
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.withContext
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.withContext
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.suspendCancellableCoroutine

object ScheduledLecturePolicy {
    fun validate(title: String, durationMinutes: Int, languageTag: String, scheduledAt: Long, now: Long): String? {
        if (title.isBlank()) return "Choose a saved lesson."
        if (durationMinutes !in 5..240) return "Lecture duration must be between 5 and 240 minutes."
        if (languageTag.isBlank() || Locale.forLanguageTag(languageTag).language.isBlank()) return "Choose a valid narration language."
        if (scheduledAt < now + 60_000L) return "Choose a start time at least one minute in the future."
        return null
    }

    fun narrationText(outline: String): String = outline
        .replace(Regex("(?m)^\\s{0,3}#{1,6}\\s*"), "")
        .replace(Regex("[*_~`>]"), " ")
        .replace(Regex("\\s+"), " ")
        .trim()
        .take(100_000)

    fun chunks(text: String, maxChars: Int = 3_000): List<String> {
        require(maxChars in 500..3_500)
        val normalized = text.trim()
        if (normalized.isEmpty()) return emptyList()
        val result = mutableListOf<String>()
        var remaining = normalized
        while (remaining.length > maxChars) {
            var cut = remaining.lastIndexOf(' ', maxChars)
            if (cut < maxChars / 2) cut = maxChars
            result += remaining.substring(0, cut).trim()
            remaining = remaining.substring(cut).trim()
        }
        if (remaining.isNotEmpty()) result += remaining
        return result
    }
}

object ScheduledLectureScheduler {
    fun enqueue(context: Context, lecture: ScheduledLectureEntity): UUID {
        val delay = (lecture.scheduledAt - System.currentTimeMillis()).coerceAtLeast(0L)
        val request = OneTimeWorkRequestBuilder<ScheduledLectureWorker>()
            .setInitialDelay(delay, TimeUnit.MILLISECONDS)
            .setInputData(workDataOf(ScheduledLectureWorker.KEY_LECTURE_ID to lecture.id))
            .addTag(TAG)
            .build()
        WorkManager.getInstance(context).enqueueUniqueWork(uniqueName(lecture.id), ExistingWorkPolicy.REPLACE, request)
        return request.id
    }

    fun cancel(context: Context, id: String) {
        WorkManager.getInstance(context).cancelUniqueWork(uniqueName(id))
    }

    fun uniqueName(id: String) = "molecularis-scheduled-lecture-$id"
    const val TAG = "molecularis-scheduled-lecture"
}

class ScheduledLectureWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {
    private val db by lazy { DatabaseProvider.get(applicationContext) }
    private var engine: TextToSpeech? = null
    private var audioManager: AudioManager? = null
    private var focusRequest: AudioFocusRequest? = null
    private var legacyFocusListener: AudioManager.OnAudioFocusChangeListener? = null
    private var audioManager: AudioManager? = null
    private var focusRequest: AudioFocusRequest? = null
    private var legacyFocusListener: AudioManager.OnAudioFocusChangeListener? = null

    override suspend fun getForegroundInfo(): ForegroundInfo {
        val manager = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= 26) manager.createNotificationChannel(
            NotificationChannel(CHANNEL_ID, "Scheduled teaching", NotificationManager.IMPORTANCE_LOW)
        )
        val id = inputData.getString(KEY_LECTURE_ID).orEmpty()
        val row = if (id.isNotBlank()) db.scheduledLectureDao().lecture(id) else null
        val open = PendingIntent.getActivity(
            applicationContext, 8402, Intent(applicationContext, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val stopIntent = Intent(applicationContext, ScheduledLectureActionReceiver::class.java).setAction(ScheduledLectureActionReceiver.ACTION_STOP).putExtra(ScheduledLectureActionReceiver.EXTRA_ID, id)
        val stopPending = PendingIntent.getBroadcast(applicationContext, id.hashCode(), stopIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        val notification = NotificationCompat.Builder(applicationContext, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle(row?.title ?: "Molecularis scheduled lecture")
            .setContentText("Preparing offline narration")
            .setContentIntent(open)
            .setOngoing(true)
            .addAction(android.R.drawable.ic_media_pause, "Stop", stopPending)
            .setOnlyAlertOnce(true)
            .build()
        val type = if (Build.VERSION.SDK_INT >= 29) android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK else 0
        return ForegroundInfo(NOTIFICATION_ID, notification, type)
    }

    override suspend fun doWork(): Result {
        val id = inputData.getString(KEY_LECTURE_ID) ?: return Result.failure()
        val lecture = db.scheduledLectureDao().lecture(id) ?: return Result.failure()
        if (lecture.scheduledAt > System.currentTimeMillis() + 30_000L) return Result.retry()
        return try {
            setForeground(getForegroundInfo())
            if (Build.VERSION.SDK_INT >= 33 &&
                ContextCompat.checkSelfPermission(applicationContext, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
            ) {
                error("Notification permission is disabled. Enable notifications and schedule the lecture again.")
            }
            val lesson = db.lessonDao().lesson(lecture.lessonId) ?: error("The saved lesson no longer exists.")
            val text = ScheduledLecturePolicy.narrationText(lesson.outline)
            require(text.isNotBlank()) { "The saved lesson has no narration text." }
            db.scheduledLectureDao().updateStatus(id, "running", null)
            val tts = createOfflineEngine(Locale.forLanguageTag(lecture.languageTag))
            engine = tts
            check(requestAudioFocus()) { "Audio focus is unavailable; another app may be using the audio output." }
            check(requestAudioFocus()) { "Audio focus is unavailable; another app may be using the audio output." }
            val chunks = ScheduledLecturePolicy.chunks(text)
            chunks.forEachIndexed { index, chunk ->
                currentCoroutineContext().ensureActive()
                speakChunk(tts, chunk, "$id-$index")
                setProgress(workDataOf("completed_chunks" to index + 1, "total_chunks" to chunks.size))
            }
            db.scheduledLectureDao().updateStatus(id, "completed", null)
            Result.success()
        } catch (cancelled: CancellationException) {
            withContext(NonCancellable) { db.scheduledLectureDao().updateStatus(id, "interrupted", "Stopped or interrupted by the user.") }
            throw cancelled
        } catch (error: Throwable) {
            db.scheduledLectureDao().updateStatus(id, "failed", error.message ?: "Lecture playback failed.")
            Result.failure(workDataOf("error" to (error.message ?: "Lecture playback failed.")))
        } finally {
            engine?.stop()
            engine?.shutdown()
            engine = null
            abandonAudioFocus()
            abandonAudioFocus()
        }
    }


    private fun requestAudioFocus(): Boolean {
        val manager = applicationContext.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        audioManager = manager
        val attributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_MEDIA)
            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
            .build()
        val listener = AudioManager.OnAudioFocusChangeListener { change ->
            if (change == AudioManager.AUDIOFOCUS_LOSS || change == AudioManager.AUDIOFOCUS_LOSS_TRANSIENT) {
                engine?.stop()
            }
        }
        return if (Build.VERSION.SDK_INT >= 26) {
            val request = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
                .setAudioAttributes(attributes)
                .setOnAudioFocusChangeListener(listener)
                .build()
            focusRequest = request
            manager.requestAudioFocus(request) == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
        } else {
            legacyFocusListener = listener
            manager.requestAudioFocus(listener, AudioManager.STREAM_MUSIC, AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK) == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
        }
    }

    private fun abandonAudioFocus() {
        val manager = audioManager ?: return
        if (Build.VERSION.SDK_INT >= 26) focusRequest?.let(manager::abandonAudioFocusRequest)
        else legacyFocusListener?.let(manager::abandonAudioFocus)
        focusRequest = null
        legacyFocusListener = null
        audioManager = null
    }


    private fun requestAudioFocus(): Boolean {
        val manager = applicationContext.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        audioManager = manager
        val attributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_MEDIA)
            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
            .build()
        val listener = AudioManager.OnAudioFocusChangeListener { change ->
            if (change == AudioManager.AUDIOFOCUS_LOSS || change == AudioManager.AUDIOFOCUS_LOSS_TRANSIENT) {
                engine?.stop()
            }
        }
        return if (Build.VERSION.SDK_INT >= 26) {
            val request = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
                .setAudioAttributes(attributes)
                .setOnAudioFocusChangeListener(listener)
                .build()
            focusRequest = request
            manager.requestAudioFocus(request) == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
        } else {
            legacyFocusListener = listener
            manager.requestAudioFocus(listener, AudioManager.STREAM_MUSIC, AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK) == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
        }
    }

    private fun abandonAudioFocus() {
        val manager = audioManager ?: return
        if (Build.VERSION.SDK_INT >= 26) focusRequest?.let { manager.abandonAudioFocusRequest(it) }
        else legacyFocusListener?.let { manager.abandonAudioFocus(it) }
        focusRequest = null
        legacyFocusListener = null
        audioManager = null
    }

    private suspend fun createOfflineEngine(locale: Locale): TextToSpeech =
        suspendCancellableCoroutine { continuation ->
            val holder = java.util.concurrent.atomic.AtomicReference<TextToSpeech?>()
            val created = TextToSpeech(applicationContext) { status ->
                val tts = holder.get()
                if (!continuation.isActive) {
                    tts?.shutdown()
                } else if (status != TextToSpeech.SUCCESS || tts == null) {
                    continuation.resumeWithException(IllegalStateException("Android text-to-speech initialization failed."))
                } else {
                    val offlineVoice = tts.voices
                        ?.filter { !it.isNetworkConnectionRequired }
                        ?.filter { it.locale.language == locale.language }
                        ?.maxByOrNull { if (it.locale.country == locale.country) 2 else 1 }
                    if (offlineVoice == null) {
                        continuation.resumeWithException(IllegalStateException("No installed offline voice is available for ${locale.toLanguageTag()}."))
                    } else {
                        tts.voice = offlineVoice
                        tts.setAudioAttributes(
                            AudioAttributes.Builder()
                                .setUsage(AudioAttributes.USAGE_MEDIA)
                                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                                .build()
                        )
                        continuation.resume(tts)
                    }
                }
            }
            holder.set(created)
            continuation.invokeOnCancellation { created.stop(); created.shutdown() }
        }

    private suspend fun speakChunk(tts: TextToSpeech, text: String, utteranceId: String) {
        suspendCancellableCoroutine { continuation ->
            tts.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(id: String?) = Unit
                override fun onDone(id: String?) {
                    if (id == utteranceId && continuation.isActive) continuation.resume(Unit)
                }
                @Deprecated("Deprecated in Java")
                override fun onError(id: String?) {
                    if (id == utteranceId && continuation.isActive) continuation.resumeWithException(IllegalStateException("Speech engine failed during narration."))
                }
                override fun onError(id: String?, errorCode: Int) {
                    if (id == utteranceId && continuation.isActive) continuation.resumeWithException(IllegalStateException("Speech engine error: $errorCode"))
                }
            })
            val result = tts.speak(text, TextToSpeech.QUEUE_FLUSH, Bundle(), utteranceId)
            if (result != TextToSpeech.SUCCESS && continuation.isActive) {
                continuation.resumeWithException(IllegalStateException("Android could not start speech playback."))
            }
            continuation.invokeOnCancellation { tts.stop() }
        }
    }

    companion object {
        const val KEY_LECTURE_ID = "scheduled_lecture_id"
        private const val CHANNEL_ID = "molecularis_scheduled_teaching"
        private const val NOTIFICATION_ID = 8401
    }
}

class ScheduledLectureActionReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != ACTION_STOP) return
        val id = intent.getStringExtra(EXTRA_ID) ?: return
        WorkManager.getInstance(context).cancelUniqueWork(ScheduledLectureScheduler.uniqueName(id))
    }

    companion object {
        const val ACTION_STOP = "org.molecularis.app.action.STOP_SCHEDULED_LECTURE"
        const val EXTRA_ID = "scheduled_lecture_id"
    }
}

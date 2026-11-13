package org.molecularis.app.features

import android.annotation.TargetApi
import android.content.Context
import android.content.Intent
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioManager
import android.os.Build
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognitionSupport
import android.speech.RecognitionSupportCallback
import android.speech.ModelDownloadListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.speech.tts.Voice
import java.io.Closeable
import java.util.Locale

data class OfflineTtsVoice(
    val name: String,
    val languageTag: String,
    val quality: Int
) {
    val label: String get() {
        val locale = Locale.forLanguageTag(languageTag)
        val language = locale.getDisplayLanguage(Locale.getDefault())
            .replaceFirstChar { if (it.isLowerCase()) it.titlecase(Locale.getDefault()) else it.toString() }
        val region = locale.getDisplayCountry(Locale.getDefault())
        val qualityLabel = when {
            quality >= 400 -> "High quality"
            quality >= 300 -> "Standard quality"
            quality > 0 -> "Basic quality"
            else -> "Default quality"
        }
        return buildString {
            append(language.ifBlank { "Unknown language" })
            if (region.isNotBlank()) append(" (").append(region).append(")")
            append(" · ").append(qualityLabel)
        }
    }
}

data class OfflineRecognitionLanguages(
    val installed: List<String>,
    val downloadable: List<String>,
    val pending: List<String>
)

/**
 * Offline-only speech controller.
 *
 * ASR uses Android's on-device recognizer exclusively (API 31+). API 33+ can
 * report installed/supported language packs and request downloads from the
 * platform recognizer. TTS only selects voices explicitly marked as local.
 */
class OfflineVoiceController(
    context: Context,
    private val onResult: (String) -> Unit,
    private val onError: (String) -> Unit,
    private val onListeningChanged: (Boolean) -> Unit = {},
    initialLanguageTag: String = Locale.getDefault().toLanguageTag(),
    initialTtsVoiceName: String? = null,
    private val onVoiceCatalogChanged: (List<OfflineTtsVoice>) -> Unit = {}
) : Closeable {
    private val appContext = context.applicationContext
    private val audioManager = appContext.getSystemService(Context.AUDIO_SERVICE) as AudioManager
    private var audioFocusRequest: AudioFocusRequest? = null
    private var narrationRate = 1.0f
    private var recognizer: SpeechRecognizer? = null
    private var textToSpeech: TextToSpeech? = null
    private var offlineVoices: List<Voice> = emptyList()
    private var selectedVoice: Voice? = null
    private var selectedVoiceName: String? = initialTtsVoiceName
    private var languageTag: String = normalizeLanguageTag(initialLanguageTag)
    private var closed = false
    private var narrationChunks: List<NarrationChunk> = emptyList()
    private var narrationIndex = 0
    private var narrationPaused = false
    private var narrationUtteranceId: String? = null
    private var narrationOnSegmentStarted: (Int) -> Unit = {}
    private var narrationOnDone: () -> Unit = {}
    private var narrationOnStateChanged: (Boolean, Boolean) -> Unit = { _, _ -> }

    init {
        textToSpeech = TextToSpeech(appContext) { status ->
            if (closed) return@TextToSpeech
            if (status != TextToSpeech.SUCCESS) {
                onError("Text-to-speech could not be initialized.")
                return@TextToSpeech
            }
            engineProgressListener()
            refreshOfflineVoices()
        }
    }

    fun setLanguageTag(value: String) {
        val normalized = normalizeLanguageTag(value)
        languageTag = normalized
        val language = Locale.forLanguageTag(normalized).language
        selectedVoice = offlineVoices.firstOrNull { it.locale.toLanguageTag().equals(normalized, true) }
            ?: offlineVoices.firstOrNull { it.locale.language.equals(language, true) }
            ?: offlineVoices.firstOrNull { it.name == selectedVoiceName }
            ?: offlineVoices.firstOrNull()
        selectedVoiceName = selectedVoice?.name
        selectedVoice?.let { textToSpeech?.voice = it }
    }

    fun setTtsVoice(name: String) {
        val voice = offlineVoices.firstOrNull { it.name == name }
            ?: error("The selected offline TTS voice is no longer installed.")
        selectedVoice = voice
        selectedVoiceName = voice.name
        textToSpeech?.voice = voice
    }

    fun selectedTtsVoiceName(): String? = selectedVoice?.name

    fun refreshOfflineVoices(): List<OfflineTtsVoice> {
        val engine = textToSpeech ?: return emptyList()
        offlineVoices = engine.voices.orEmpty()
            .filterNot { it.isNetworkConnectionRequired }
            .sortedWith(compareBy<Voice>({ it.locale.displayName }, { -it.quality }, { it.name }))
        val language = Locale.forLanguageTag(languageTag).language
        selectedVoice = offlineVoices.firstOrNull { it.locale.toLanguageTag().equals(languageTag, true) }
            ?: offlineVoices.firstOrNull { it.locale.language.equals(language, true) }
            ?: offlineVoices.firstOrNull { it.name == selectedVoiceName }
            ?: offlineVoices.firstOrNull()
        selectedVoiceName = selectedVoice?.name
        selectedVoice?.let { engine.voice = it }
        val catalog = offlineVoices.map {
            OfflineTtsVoice(it.name, it.locale.toLanguageTag(), it.quality)
        }
        onVoiceCatalogChanged(catalog)
        return catalog
    }

    fun checkRecognitionSupport(callback: (OfflineRecognitionLanguages) -> Unit) {
        if (Build.VERSION.SDK_INT < 33) {
            onError("Speech language-pack discovery requires Android 13 or newer. On-device recognition still requires Android 12+.")
            callback(OfflineRecognitionLanguages(emptyList(), emptyList(), emptyList()))
            return
        }
        if (!SpeechRecognizer.isOnDeviceRecognitionAvailable(appContext)) {
            onError("This device has no on-device speech recognition service.")
            callback(OfflineRecognitionLanguages(emptyList(), emptyList(), emptyList()))
            return
        }
        try {
            val service = getOrCreateRecognizer()
            service.checkRecognitionSupport(recognitionIntent(), appContext.mainExecutor,
                object : RecognitionSupportCallback {
                    override fun onSupportResult(support: RecognitionSupport) {
                        callback(
                            OfflineRecognitionLanguages(
                                support.installedOnDeviceLanguages.sorted(),
                                support.supportedOnDeviceLanguages.sorted(),
                                support.pendingOnDeviceLanguages.sorted()
                            )
                        )
                    }

                    override fun onError(error: Int) {
                        this@OfflineVoiceController.onError("Could not inspect offline speech languages (code $error).")
                    }
                }
            )
        } catch (error: Throwable) {
            onError("Could not inspect offline speech languages: ${error.message ?: error.javaClass.simpleName}")
        }
    }

    fun downloadRecognitionLanguage(onStatus: (String) -> Unit) {
        if (Build.VERSION.SDK_INT < 33) {
            onStatus("Platform-managed language downloads require Android 13 or newer.")
            return
        }
        if (!SpeechRecognizer.isOnDeviceRecognitionAvailable(appContext)) {
            onStatus("No on-device speech recognizer is installed.")
            return
        }
        try {
            val service = getOrCreateRecognizer()
            if (Build.VERSION.SDK_INT >= 34) {
                service.triggerModelDownload(recognitionIntent(), appContext.mainExecutor,
                    object : ModelDownloadListener {
                        override fun onProgress(progress: Int) {
                            onStatus("Downloading offline speech language pack: $progress%")
                        }
                        override fun onSuccess() {
                            onStatus("Offline speech language pack is installed.")
                            checkRecognitionSupport { }
                        }
                        override fun onScheduled() {
                            onStatus("Speech language download was scheduled by Android. Check status again later.")
                        }
                        override fun onError(error: Int) {
                            onStatus("Speech language download failed (code $error).")
                        }
                    }
                )
            } else {
                service.triggerModelDownload(recognitionIntent())
                onStatus("Android was asked to download this language pack. Check language support again after the system download.")
            }
        } catch (error: Throwable) {
            onStatus("Could not request language download: ${error.message ?: error.javaClass.simpleName}")
        }
    }

    fun startListening() {
        if (closed) return
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.S) {
            onError("Offline speech recognition requires Android 12 or newer.")
            return
        }
        if (!SpeechRecognizer.isOnDeviceRecognitionAvailable(appContext)) {
            onError("This device has no on-device speech recognition service installed.")
            return
        }
        try {
            getOrCreateRecognizer().startListening(recognitionIntent())
        } catch (error: Throwable) {
            onListeningChanged(false)
            onError("Could not start offline speech recognition: ${error.message ?: error.javaClass.simpleName}")
        }
    }

    fun stopListening() {
        recognizer?.stopListening()
        onListeningChanged(false)
    }

    /** Speak long teaching scripts as resumable slide-sized segments. */
    fun speak(text: String) = speakSegments(listOf(text))

    fun speakSegments(
        segments: List<String>,
        onSegmentStarted: (Int) -> Unit = {},
        onDone: () -> Unit = {},
        onStateChanged: (playing: Boolean, paused: Boolean) -> Unit = { _, _ -> }
    ) {
        if (closed) return
        val engine = textToSpeech ?: run { onError("Speech output is not ready yet."); return }
        val voice = selectedVoice ?: run {
            onError("No offline speech voice is installed. Install a local voice in Android text-to-speech settings.")
            return
        }
        val safeSegments = segments.map { it.trim() }.filter { it.isNotBlank() }
        if (safeSegments.isEmpty()) { onError("There is no lesson text to narrate."); return }
        engine.voice = voice
        stopSpeaking()
        narrationChunks = LessonNarrationTimeline.build(safeSegments)
        narrationIndex = 0
        narrationPaused = false
        narrationOnSegmentStarted = onSegmentStarted
        narrationOnDone = onDone
        narrationOnStateChanged = onStateChanged
        if (!requestNarrationAudioFocus()) {
            clearNarration()
            onError("Audio focus is unavailable. Pause other audio and try again.")
            return
        }
        engine.setSpeechRate(narrationRate)
        speakCurrentSegment()
    }

    private fun speakCurrentSegment() {
        if (closed || narrationPaused) return
        val engine = textToSpeech ?: return
        if (narrationIndex !in narrationChunks.indices) {
            narrationOnStateChanged(false, false)
            val done = narrationOnDone
            clearNarration()
            done()
            return
        }
        val id = "molecularis-narration-${narrationIndex}-${System.nanoTime()}"
        narrationUtteranceId = id
        engine.speak(narrationChunks[narrationIndex].text, TextToSpeech.QUEUE_FLUSH, null, id)
    }

    fun setSpeechRate(rate: Float) {
        require(rate in 0.75f..1.35f) { "Narration speed must be between 0.75× and 1.35×." }
        narrationRate = rate
        textToSpeech?.setSpeechRate(rate)
    }

    private fun requestNarrationAudioFocus(): Boolean {
        val request = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
            .setAudioAttributes(AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                .build())
            .setWillPauseWhenDucked(true)
            .setOnAudioFocusChangeListener { change ->
                when (change) {
                    AudioManager.AUDIOFOCUS_LOSS_TRANSIENT, AudioManager.AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK -> pauseSpeaking()
                    AudioManager.AUDIOFOCUS_GAIN -> if (narrationPaused) resumeSpeaking()
                    AudioManager.AUDIOFOCUS_LOSS -> stopSpeaking()
                }
            }
            .build()
        audioFocusRequest = request
        return audioManager.requestAudioFocus(request) == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
    }

    private fun abandonNarrationAudioFocus() {
        audioFocusRequest?.let { runCatching { audioManager.abandonAudioFocusRequest(it) } }
        audioFocusRequest = null
    }

    fun pauseSpeaking() {
        if (narrationChunks.isEmpty() || narrationPaused) return
        narrationPaused = true
        textToSpeech?.stop()
        narrationOnStateChanged(false, true)
    }

    fun resumeSpeaking() {
        if (!narrationPaused || narrationChunks.isEmpty()) return
        narrationPaused = false
        narrationOnStateChanged(true, false)
        speakCurrentSegment()
    }

    fun seekSpeakingTo(slideIndex: Int) {
        if (narrationChunks.isEmpty()) return
        textToSpeech?.stop()
        narrationIndex = LessonNarrationTimeline.firstChunkForSlide(narrationChunks, slideIndex)
        narrationPaused = false
        narrationOnStateChanged(true, false)
        speakCurrentSegment()
    }

    fun stopSpeaking() {
        val stateChanged = narrationOnStateChanged
        textToSpeech?.stop()
        clearNarration()
        stateChanged(false, false)
    }

    private fun clearNarration() {
        narrationChunks = emptyList()
        narrationIndex = 0
        narrationPaused = false
        narrationUtteranceId = null
        narrationOnSegmentStarted = {}
        narrationOnDone = {}
        narrationOnStateChanged = { _, _ -> }
        abandonNarrationAudioFocus()
    }

    private fun engineProgressListener() {
        textToSpeech?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {
                if (utteranceId != narrationUtteranceId || narrationPaused) return
                narrationOnSegmentStarted(narrationChunks.getOrNull(narrationIndex)?.slideIndex ?: narrationIndex)
                narrationOnStateChanged(true, false)
            }
            override fun onDone(utteranceId: String?) {
                if (utteranceId != narrationUtteranceId || narrationPaused || closed) return
                narrationIndex += 1
                speakCurrentSegment()
            }
            @Deprecated("Deprecated in Android")
            override fun onError(utteranceId: String?) {
                if (utteranceId == narrationUtteranceId && !narrationPaused) {
                    onError("Narration stopped because the Android speech engine reported an error.")
                    stopSpeaking()
                }
            }
            override fun onError(utteranceId: String?, errorCode: Int) {
                if (utteranceId == narrationUtteranceId && !narrationPaused) {
                    onError("Narration failed (speech engine code $errorCode).")
                    stopSpeaking()
                }
            }
        })
    }

    @TargetApi(Build.VERSION_CODES.S)
    private fun getOrCreateRecognizer(): SpeechRecognizer {
        return recognizer ?: SpeechRecognizer.createOnDeviceSpeechRecognizer(appContext).also {
            it.setRecognitionListener(listener)
            recognizer = it
        }
    }

    private fun recognitionIntent() = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        putExtra(RecognizerIntent.EXTRA_LANGUAGE, languageTag)
        putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)
        putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE, true)
    }

    private val listener = object : RecognitionListener {
        override fun onReadyForSpeech(params: Bundle?) { onListeningChanged(true) }
        override fun onBeginningOfSpeech() = Unit
        override fun onRmsChanged(rmsdB: Float) = Unit
        override fun onBufferReceived(buffer: ByteArray?) = Unit
        override fun onEndOfSpeech() { onListeningChanged(false) }
        override fun onError(error: Int) {
            onListeningChanged(false)
            onError(
                when (error) {
                    SpeechRecognizer.ERROR_AUDIO -> "Microphone audio error."
                    SpeechRecognizer.ERROR_CLIENT -> "Speech recognition was cancelled."
                    SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "Microphone permission is required."
                    SpeechRecognizer.ERROR_NETWORK, SpeechRecognizer.ERROR_NETWORK_TIMEOUT ->
                        "The on-device recognizer reported a network error; no network fallback was requested."
                    SpeechRecognizer.ERROR_NO_MATCH -> "No speech was recognised. Try again."
                    SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "Speech recognition is busy. Try again shortly."
                    SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "No speech was detected."
                    SpeechRecognizer.ERROR_LANGUAGE_NOT_SUPPORTED -> "This language is not supported by the on-device recognizer."
                    SpeechRecognizer.ERROR_LANGUAGE_UNAVAILABLE -> "This language pack is not installed yet. Download it in Voice settings."
                    else -> "Offline speech recognition failed (code $error)."
                }
            )
        }
        override fun onResults(results: Bundle?) {
            onListeningChanged(false)
            val text = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull().orEmpty()
            if (text.isBlank()) onError("No speech was recognised.") else onResult(text)
        }
        override fun onPartialResults(partialResults: Bundle?) = Unit
        override fun onEvent(eventType: Int, params: Bundle?) = Unit
    }

    override fun close() {
        if (closed) return
        closed = true
        runCatching { recognizer?.cancel() }
        runCatching { recognizer?.destroy() }
        recognizer = null
        runCatching { textToSpeech?.stop() }
        clearNarration()
        runCatching { textToSpeech?.shutdown() }
        textToSpeech = null
        offlineVoices = emptyList()
        selectedVoice = null
    }

    companion object {
        fun normalizeLanguageTag(value: String): String {
            require(value.matches(Regex("(?i)^[a-z]{2,8}(-[a-z0-9]{1,8})*$"))) {
                "Enter a valid BCP-47 language tag, such as en-US, hi-IN or bn-IN."
            }
            val locale = Locale.forLanguageTag(value)
            require(locale.language.isNotBlank()) { "The language tag is not valid." }
            return locale.toLanguageTag()
        }
    }
}

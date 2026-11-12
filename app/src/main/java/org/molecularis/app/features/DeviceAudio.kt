package org.molecularis.app.features

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import java.util.Locale

/** Android system speech recognition wrapper. Caller must request RECORD_AUDIO at runtime. */
class DeviceSpeechInput(context: Context, private val onResult: (String) -> Unit, private val onError: (String) -> Unit) {
    private val recognizer: SpeechRecognizer
    init {
        require(SpeechRecognizer.isRecognitionAvailable(context)) { "No speech recognition service is installed." }
        recognizer = SpeechRecognizer.createSpeechRecognizer(context).apply {
            setRecognitionListener(object : RecognitionListener {
                override fun onReadyForSpeech(params: Bundle?) = Unit
                override fun onBeginningOfSpeech() = Unit
                override fun onRmsChanged(rmsdB: Float) = Unit
                override fun onBufferReceived(buffer: ByteArray?) = Unit
                override fun onEndOfSpeech() = Unit
                override fun onEvent(eventType: Int, params: Bundle?) = Unit
                override fun onPartialResults(partialResults: Bundle?) = Unit
                override fun onResults(results: Bundle?) {
                    val text = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull()
                    if (text.isNullOrBlank()) onError("Speech was not recognized.") else onResult(text)
                }
                override fun onError(error: Int) { onError("Speech recognition error ($error). Check that an offline recognition language pack is installed.") }
            })
        }
    }

    fun start(locale: Locale = Locale.getDefault()) {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, locale.toLanguageTag())
            putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE, true)
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
        }
        recognizer.startListening(intent)
    }
    fun stop() = recognizer.stopListening()
    fun cancel() = recognizer.cancel()
    fun close() = recognizer.destroy()
}

/** Text-to-speech uses the installed Android TTS engine; offline voice availability varies by device. */
class DeviceSpeechOutput(context: Context, private val onReady: (Boolean) -> Unit = {}) : TextToSpeech.OnInitListener {
    private var engine: TextToSpeech? = TextToSpeech(context.applicationContext, this)
    override fun onInit(status: Int) { onReady(status == TextToSpeech.SUCCESS) }
    fun speak(text: String, locale: Locale = Locale.getDefault()) {
        require(text.isNotBlank())
        val tts = engine ?: error("Speech engine is closed")
        tts.language = locale
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "astronaut-${System.nanoTime()}")
    }
    fun stop() { engine?.stop() }
    fun close() { engine?.stop(); engine?.shutdown(); engine = null }
}

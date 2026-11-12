package org.molecularis.app.features

import android.content.Context
import android.net.Uri
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.label.ImageLabeling
import com.google.mlkit.vision.label.defaults.ImageLabelerOptions
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.withContext
import java.io.Closeable

/** Bundled on-device ML Kit image labels. This describes visible categories, not free-form vision reasoning. */
class OfflineImageAnalyzer(context: Context) : Closeable {
    private val appContext = context.applicationContext
    private val labeler = ImageLabeling.getClient(ImageLabelerOptions.DEFAULT_OPTIONS)

    suspend fun analyze(uri: Uri): String = withContext(Dispatchers.IO) {
        val image = InputImage.fromFilePath(appContext, uri)
        val labels = labeler.process(image).await()
            .sortedByDescending { it.confidence }
            .take(8)
        if (labels.isEmpty()) {
            "Image analysis: no recognizable object labels were returned."
        } else {
            "Visible image labels: " + labels.joinToString(", ") {
                it.text + " (" + "%.2f".format(it.confidence) + ")"
            }
        }
    }

    override fun close() {
        labeler.close()
    }
}

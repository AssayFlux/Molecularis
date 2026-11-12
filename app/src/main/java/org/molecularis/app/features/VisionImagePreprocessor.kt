package org.molecularis.app.features

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.FileOutputStream
import java.util.UUID

/**
 * Bounds image memory before sending pixels to a local vision-language model.
 * Source URIs are read locally and converted to a private, downsampled JPEG cache file.
 */
object VisionImagePreprocessor {
    const val MAX_DIMENSION = 1536
    const val MAX_ENCODED_BYTES = 8 * 1024 * 1024

    fun calculateSampleSize(width: Int, height: Int, maxDimension: Int = MAX_DIMENSION): Int {
        require(width > 0 && height > 0) { "Image dimensions are invalid." }
        require(maxDimension > 0) { "Maximum image dimension must be positive." }
        var sample = 1
        while ((width + sample - 1) / sample > maxDimension ||
            (height + sample - 1) / sample > maxDimension
        ) {
            sample *= 2
        }
        return sample
    }

    fun prepare(context: Context, uri: Uri, displayName: String): File {
        val resolver = context.contentResolver
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        resolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, bounds) }
            ?: error("Cannot open the selected image.")
        require(bounds.outWidth > 0 && bounds.outHeight > 0) {
            "The selected file is not a supported image."
        }

        val options = BitmapFactory.Options().apply {
            inSampleSize = calculateSampleSize(bounds.outWidth, bounds.outHeight)
            inPreferredConfig = Bitmap.Config.ARGB_8888
        }
        val bitmap = resolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, options) }
            ?: error("Could not decode the selected image.")
        try {
            val encoded = ByteArrayOutputStream()
            var quality = 88
            bitmap.compress(Bitmap.CompressFormat.JPEG, quality, encoded)
            while (encoded.size() > MAX_ENCODED_BYTES && quality > 60) {
                quality -= 8
                encoded.reset()
                bitmap.compress(Bitmap.CompressFormat.JPEG, quality, encoded)
            }
            require(encoded.size() in 1..MAX_ENCODED_BYTES) {
                "Image is too large for the configured on-device vision memory budget."
            }

            val safeName = displayName.substringAfterLast('/').take(48)
                .replace(Regex("[^A-Za-z0-9._-]"), "_")
                .ifBlank { "image" }
            val directory = File(context.cacheDir, "vision-inputs").apply { mkdirs() }
            val output = File(directory, UUID.randomUUID().toString() + "-" + safeName + ".jpg")
            FileOutputStream(output).use { encoded.writeTo(it) }
            return output
        } finally {
            bitmap.recycle()
        }
    }
}

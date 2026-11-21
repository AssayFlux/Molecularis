package org.assayflux.molecularis

import java.io.ByteArrayOutputStream
import java.io.File
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.util.zip.GZIPInputStream

/** Strict UTF-8 decoding with a hard cap on expanded bytes to prevent compressed-input bombs. */
internal object SequenceFileSupport {
    fun readText(file: File, gzip: Boolean, maxBytes: Long, maxChars: Int): String {
        val source = file.inputStream()
        val decoded = if (gzip) GZIPInputStream(source) else source
        val bytes = decoded.use { stream ->
            val output = ByteArrayOutputStream()
            val buffer = ByteArray(16 * 1024)
            var total = 0L
            while (true) {
                val count = stream.read(buffer)
                if (count < 0) break
                total += count
                require(total <= maxBytes) { "Expanded sequence input exceeds the supported size limit" }
                output.write(buffer, 0, count)
            }
            output.toByteArray()
        }
        val text = Charsets.UTF_8.newDecoder()
            .onMalformedInput(CodingErrorAction.REPORT)
            .onUnmappableCharacter(CodingErrorAction.REPORT)
            .decode(ByteBuffer.wrap(bytes)).toString()
        require(!text.contains('\u0000')) { "Sequence input contains a NUL byte" }
        require(text.length <= maxChars) { "Sequence input exceeds the supported character limit" }
        return text
    }
}

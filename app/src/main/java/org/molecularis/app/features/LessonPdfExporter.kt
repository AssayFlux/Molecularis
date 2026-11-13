package org.molecularis.app.features

import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import java.io.OutputStream

/** Offline landscape PDF export, one readable slide per page. */
object LessonPdfExporter {
    fun write(slides: List<LessonSlide>, topic: String, audience: String, theme: SlideTheme, output: OutputStream) {
        require(slides.isNotEmpty()) { "There are no slides to export." }
        val doc = PdfDocument()
        try {
            slides.forEachIndexed { index, slide ->
                val page = doc.startPage(PdfDocument.PageInfo.Builder(1280, 720, index + 1).create())
                val canvas = page.canvas
                canvas.drawColor(android.graphics.Color.parseColor(theme.backgroundHex))
                val accent = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = android.graphics.Color.parseColor(theme.accentHex); strokeWidth = 10f }
                val title = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = android.graphics.Color.parseColor(theme.foregroundHex); textSize = 42f; typeface = Typeface.create("sans-serif", Typeface.BOLD) }
                val body = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = android.graphics.Color.parseColor(theme.foregroundHex); textSize = 27f }
                val meta = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = android.graphics.Color.parseColor(theme.accentHex); textSize = 18f }
                canvas.drawRect(72f, 70f, 82f, 650f, accent)
                canvas.drawText(topic.take(90), 112f, 48f, meta)
                wrap(slide.title, title, 1050f).take(2).forEachIndexed { line, text -> canvas.drawText(text, 112f, 145f + line * 52f, title) }
                var y = 250f
                slide.points.take(7).forEach { point ->
                    val lines = wrap(point, body, 1000f)
                    canvas.drawCircle(125f, y - 9f, 6f, accent)
                    lines.forEach { line -> canvas.drawText(line, 150f, y, body); y += 38f }
                    y += 18f
                }
                canvas.drawText(audience + "  ·  " + (index + 1) + " / " + slides.size, 112f, 675f, meta)
                doc.finishPage(page)
            }
            doc.writeTo(output)
        } finally { doc.close() }
    }
    private fun wrap(text: String, paint: Paint, width: Float): List<String> {
        val result = mutableListOf<String>()
        var line = ""
        text.split(Regex("\\s+")).forEach { word ->
            val candidate = if (line.isEmpty()) word else line + " " + word
            if (line.isNotEmpty() && paint.measureText(candidate) > width) { result += line; line = word } else line = candidate
        }
        if (line.isNotEmpty()) result += line
        return result
    }
}

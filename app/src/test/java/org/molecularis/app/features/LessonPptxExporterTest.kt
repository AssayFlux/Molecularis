package org.molecularis.app.features

import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.ByteArrayInputStream
import java.util.zip.ZipInputStream

class LessonPptxExporterTest {
    @Test fun createsEditablePresentationPackage() {
        val bytes = LessonPptxExporter.create(listOf(LessonSlide("Glycolysis", listOf("ATP is invested"))), SlideTheme.BOTANICAL)
        val files = mutableMapOf<String, String>()
        ZipInputStream(ByteArrayInputStream(bytes)).use { zip ->
            while (true) { val entry = zip.nextEntry ?: break; files[entry.name] = zip.readBytes().toString(Charsets.UTF_8) }
        }
        assertTrue(files.containsKey("[Content_Types].xml"))
        assertTrue(files.containsKey("ppt/presentation.xml"))
        assertTrue(files["ppt/slides/slide1.xml"]!!.contains("Glycolysis"))
        assertTrue(files["ppt/slides/slide1.xml"]!!.contains("ATP is invested"))
        assertTrue(files["ppt/slides/slide1.xml"]!!.contains("F2F7F1"))
    }
    @Test fun escapesXmlText() {
        val bytes = LessonPptxExporter.create(listOf(LessonSlide("A & B", listOf("x < y"))), SlideTheme.CLASSIC)
        val xml = ZipInputStream(ByteArrayInputStream(bytes)).use { zip ->
            var value = ""
            while (true) { val entry = zip.nextEntry ?: break; if (entry.name == "ppt/slides/slide1.xml") value = zip.readBytes().toString(Charsets.UTF_8) }
            value
        }
        assertTrue(xml.contains("A &amp; B")); assertTrue(xml.contains("x &lt; y"))
    }
    @Test fun rejectsEmptySlideDeck() {
        try { LessonPptxExporter.create(emptyList(), SlideTheme.CLASSIC); throw AssertionError("Expected rejection") }
        catch (_: IllegalArgumentException) { }
    }
}

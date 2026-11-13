package org.molecularis.app.features

data class PronunciationEntry(val term: String, val spokenAs: String)

/** Explicit, professor-editable pronunciation substitutions for local TTS. */
object BiochemistryPronunciationDictionary {
    val defaults = listOf(
        PronunciationEntry("ATP", "A T P"),
        PronunciationEntry("ADP", "A D P"),
        PronunciationEntry("AMP", "A M P"),
        PronunciationEntry("NADH", "N A D H"),
        PronunciationEntry("NADPH", "N A D P H"),
        PronunciationEntry("FADH2", "F A D H two"),
        PronunciationEntry("CoA", "coenzyme A"),
        PronunciationEntry("cAMP", "cyclic A M P"),
        PronunciationEntry("GTP", "G T P"),
        PronunciationEntry("DNA", "D N A"),
        PronunciationEntry("RNA", "R N A")
    )

    /** One entry per line: term=spoken form. Blank lines and # comments are ignored. */
    fun parse(source: String): List<PronunciationEntry> {
        require(source.length <= 8_000) { "Pronunciation dictionary is too large." }
        val entries = linkedMapOf<String, PronunciationEntry>()
        source.lineSequence().forEachIndexed { lineIndex, raw ->
            val line = raw.trim()
            if (line.isBlank() || line.startsWith("#")) return@forEachIndexed
            val separator = line.indexOf('=')
            require(separator in 1 until line.lastIndex) { "Invalid pronunciation entry on line ${lineIndex + 1}." }
            val term = line.substring(0, separator).trim()
            val spoken = line.substring(separator + 1).trim()
            require(term.length in 1..64 && spoken.length in 1..120) {
                "Pronunciation entry on line ${lineIndex + 1} is outside the allowed length."
            }
            require(term.none { it == '\n' || it == '\r' } && spoken.none { it == '\n' || it == '\r' })
            entries[term.lowercase()] = PronunciationEntry(term, spoken)
            require(entries.size <= 100) { "A maximum of 100 pronunciation entries is supported." }
        }
        return entries.values.sortedByDescending { it.term.length }
    }

    fun apply(text: String, entries: List<PronunciationEntry> = defaults): String {
        var result = text
        entries.sortedByDescending { it.term.length }.forEach { entry ->
            val pattern = Regex(
                "(?i)(?<![\\p{L}\\p{N}])${Regex.escape(entry.term)}(?![\\p{L}\\p{N}])"
            )
            result = pattern.replace(result) { entry.spokenAs }
        }
        return result
    }
}

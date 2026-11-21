package org.assayflux.molecularis

import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import java.security.MessageDigest
import java.time.Instant

data class PublicDatabaseHit(
    val source: String, val accession: String, val title: String,
    val organism: String? = null, val description: String? = null,
    val database: String? = null,
)

data class PublicScientificRecord(
    val source: String, val accession: String, val format: String,
    val sourceUrl: String, val retrievedAt: String, val sha256: String,
    val content: String,
)

/**
 * Bounded HTTPS adapters for public reference records. Call from Dispatchers.IO.
 * Only public search terms/accessions are accepted; never submit patient sequences,
 * VCFs, sample identifiers or private research-job metadata to public endpoints.
 */
internal class PublicDatabaseClient {
    fun searchNcbiGene(query: String, limit: Int = 20): List<PublicDatabaseHit> {
        val term = checkedQuery(query)
        val count = checkedLimit(limit)
        val searchUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" +
            "?db=gene&term=${encode(term)}&retmode=json&retmax=$count&tool=kinetics"
        val search = JSONObject(request(searchUrl, MAX_METADATA_BYTES))
        val ids = search.getJSONObject("esearchresult").optJSONArray("idlist") ?: return emptyList()
        if (ids.length() == 0) return emptyList()
        val idList = (0 until ids.length()).joinToString(",") { ids.getString(it) }
        val summaryUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" +
            "?db=gene&id=${encode(idList)}&retmode=json&tool=kinetics"
        val summary = JSONObject(request(summaryUrl, MAX_METADATA_BYTES)).getJSONObject("result")
        return (0 until ids.length()).mapNotNull { index ->
            val id = ids.getString(index)
            val item = summary.optJSONObject(id) ?: return@mapNotNull null
            PublicDatabaseHit(
                source = "NCBI Gene", accession = id,
                title = item.optString("name", "Gene $id"),
                organism = item.optJSONObject("organism")?.optString("scientificname"),
                description = item.optString("description").takeIf(String::isNotBlank),
            )
        }
    }

    fun searchNcbiSequence(database: String, query: String, limit: Int = 20): List<PublicDatabaseHit> {
        require(database in setOf("nuccore", "protein")) { "Choose NCBI nucleotide or protein records" }
        val term = checkedQuery(query)
        val count = checkedLimit(limit)
        val searchUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" +
            "?db=$database&term=${encode(term)}&retmode=json&retmax=$count&tool=kinetics"
        val search = JSONObject(request(searchUrl, MAX_METADATA_BYTES))
        val ids = search.getJSONObject("esearchresult").optJSONArray("idlist") ?: return emptyList()
        if (ids.length() == 0) return emptyList()
        val idList = (0 until ids.length()).joinToString(",") { ids.getString(it) }
        val summaryUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" +
            "?db=$database&id=${encode(idList)}&retmode=json&tool=kinetics"
        val summary = JSONObject(request(summaryUrl, MAX_METADATA_BYTES)).getJSONObject("result")
        return (0 until ids.length()).mapNotNull { index ->
            val id = ids.getString(index)
            val item = summary.optJSONObject(id) ?: return@mapNotNull null
            PublicDatabaseHit(
                source = if (database == "nuccore") "NCBI Nucleotide" else "NCBI Protein",
                accession = item.optString("accessionversion").takeIf(String::isNotBlank) ?: id,
                title = item.optString("title", "NCBI record $id"),
                organism = item.optString("organism").takeIf(String::isNotBlank),
                description = "NCBI $database reference record",
                database = database,
            )
        }
    }

    fun searchNcbiGeneLinkedSequences(geneId: String, database: String, limit: Int = 20): List<PublicDatabaseHit> {
        require(database in setOf("nuccore", "protein")) { "Choose nucleotide or protein gene links" }
        val id = geneId.trim()
        require(id.matches(Regex("[0-9]{1,12}"))) { "NCBI Gene identifier must be numeric" }
        val count = checkedLimit(limit)
        val linkUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi" +
            "?dbfrom=gene&db=$database&id=${encode(id)}&retmode=json&tool=kinetics"
        val linkSets = JSONObject(request(linkUrl, MAX_METADATA_BYTES))
            .optJSONArray("linksets") ?: return emptyList()
        val linkedIds = LinkedHashSet<String>()
        for (index in 0 until linkSets.length()) {
            val databases = linkSets.getJSONObject(index).optJSONArray("linksetdbs") ?: continue
            for (dbIndex in 0 until databases.length()) {
                val db = databases.getJSONObject(dbIndex)
                if (db.optString("dbto") != database) continue
                val links = db.optJSONArray("links") ?: continue
                for (linkIndex in 0 until links.length()) {
                    linkedIds.add(links.getString(linkIndex))
                    if (linkedIds.size >= count) break
                }
                if (linkedIds.size >= count) break
            }
            if (linkedIds.size >= count) break
        }
        if (linkedIds.isEmpty()) return emptyList()
        val joinedIds = linkedIds.joinToString(",")
        val summaryUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" +
            "?db=$database&id=${encode(joinedIds)}&retmode=json&tool=kinetics"
        val summary = JSONObject(request(summaryUrl, MAX_METADATA_BYTES)).getJSONObject("result")
        return linkedIds.mapNotNull { linkedId ->
            val item = summary.optJSONObject(linkedId) ?: return@mapNotNull null
            PublicDatabaseHit(
                source = if (database == "nuccore") "NCBI Nucleotide" else "NCBI Protein",
                accession = item.optString("accessionversion").takeIf(String::isNotBlank) ?: linkedId,
                title = item.optString("title", "NCBI record $linkedId"),
                organism = item.optString("organism").takeIf(String::isNotBlank),
                description = "Linked from NCBI Gene $id",
                database = database,
            )
        }
    }

    fun fetchNcbiFasta(database: String, accession: String): PublicScientificRecord {
        require(database in setOf("nuccore", "protein")) { "Only NCBI nuccore or protein records are supported" }
        val id = checkedAccession(accession)
        val url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi" +
            "?db=$database&id=${encode(id)}&rettype=fasta&retmode=text&tool=kinetics"
        val body = request(url, MAX_SEQUENCE_BYTES)
        require(body.lineSequence().firstOrNull()?.startsWith(">") == true) {
            "NCBI did not return a FASTA record for this accession"
        }
        return record("NCBI", id, "FASTA", url, body)
    }

    fun searchUniProt(query: String, limit: Int = 20): List<PublicDatabaseHit> {
        val term = checkedQuery(query)
        val count = checkedLimit(limit)
        val fields = "accession,id,protein_name,gene_names,organism_name"
        val url = "https://rest.uniprot.org/uniprotkb/search?query=${encode(term)}&format=json&size=$count&fields=$fields"
        val root = JSONObject(request(url, MAX_METADATA_BYTES))
        val results = root.optJSONArray("results") ?: return emptyList()
        return (0 until results.length()).map { index ->
            val item = results.getJSONObject(index)
            val accession = item.getString("primaryAccession")
            val organism = item.optJSONObject("organism")?.optString("scientificName")
            val protein = item.optJSONObject("proteinDescription")
                ?.optJSONObject("recommendedName")?.optJSONObject("fullName")?.optString("value")
            val geneName = item.optJSONArray("genes")?.optJSONObject(0)
                ?.optJSONObject("geneName")?.optString("value")
            PublicDatabaseHit(
                source = "UniProtKB", accession = accession,
                title = protein?.takeIf(String::isNotBlank) ?: item.optString("uniProtkbId", accession),
                organism = organism, description = geneName?.let { "Gene: $it" },
            )
        }
    }

    fun fetchUniProtFasta(accession: String): PublicScientificRecord {
        val id = checkedAccession(accession)
        val url = "https://rest.uniprot.org/uniprotkb/${encode(id)}.fasta"
        val body = request(url, MAX_SEQUENCE_BYTES)
        require(body.lineSequence().firstOrNull()?.startsWith(">") == true) {
            "UniProtKB did not return a FASTA record for this accession"
        }
        return record("UniProtKB", id, "FASTA", url, body)
    }

    /** Fetch a four-character RCSB PDB entry as mmCIF. */
    fun fetchRcsbMmcif(entryId: String): PublicScientificRecord {
        val id = entryId.trim().uppercase()
        require(id.matches(Regex("[0-9][A-Z0-9]{3}"))) { "Enter a valid four-character PDB entry ID" }
        val url = "https://files.rcsb.org/download/$id.cif"
        val body = request(url, MAX_STRUCTURE_BYTES)
        require(body.contains("_atom_site.") || body.contains("data_$id", ignoreCase = true)) {
            "RCSB did not return a recognised mmCIF entry"
        }
        return record("RCSB PDB", id, "mmCIF", url, body)
    }

    private fun record(source: String, accession: String, format: String, url: String, content: String) =
        PublicScientificRecord(
            source, accession, format, url, Instant.now().toString(),
            MessageDigest.getInstance("SHA-256").digest(content.toByteArray(Charsets.UTF_8))
                .joinToString("") { "%02x".format(it) },
            content,
        )

    private fun request(address: String, maximumBytes: Int): String {
        var lastFailure: java.io.IOException? = null
        for (attempt in 0..MAX_RETRIES) {
            val url = URL(address)
            require(url.protocol == "https" && url.host in ALLOWED_HOSTS) {
                "Public database host is not allow-listed"
            }
            val connection = (url.openConnection() as HttpURLConnection).apply {
                requestMethod = "GET"
                connectTimeout = CONNECT_TIMEOUT_MS
                readTimeout = READ_TIMEOUT_MS
                instanceFollowRedirects = false
                setRequestProperty("Accept", "application/json, text/plain, chemical/x-mmcif")
                setRequestProperty("User-Agent", "Molecularis-Android/0.1 (public reference retrieval)")
            }
            try {
                val status = connection.responseCode
                if (status == 429 || status in 500..599) {
                    if (attempt == MAX_RETRIES) {
                        throw java.io.IOException("Public database request failed (HTTP $status)")
                    }
                    Thread.sleep(retryDelayMillis(attempt, connection.getHeaderField("Retry-After")))
                    continue
                }
                require(status in 200..299) { "Public database request failed (HTTP $status)" }
                val declaredLength = connection.contentLengthLong
                require(declaredLength < 0 || declaredLength <= maximumBytes) {
                    "Public database response exceeds the Molecularis size limit"
                }
                val output = ByteArrayOutputStream()
                connection.inputStream.use { input ->
                    val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                    var total = 0
                    while (true) {
                        if (Thread.currentThread().isInterrupted) {
                            throw java.io.InterruptedIOException("Public database retrieval was cancelled")
                        }
                        val count = input.read(buffer)
                        if (count < 0) break
                        total += count
                        require(total <= maximumBytes) {
                            "Public database response exceeds the Molecularis size limit"
                        }
                        output.write(buffer, 0, count)
                    }
                }
                return Charsets.UTF_8.newDecoder()
                    .onMalformedInput(CodingErrorAction.REPORT)
                    .onUnmappableCharacter(CodingErrorAction.REPORT)
                    .decode(ByteBuffer.wrap(output.toByteArray()))
                    .toString()
            } catch (error: java.io.IOException) {
                lastFailure = error
                if (attempt == MAX_RETRIES) throw error
                Thread.sleep(retryDelayMillis(attempt, null))
            } finally {
                connection.disconnect()
            }
        }
        throw lastFailure ?: java.io.IOException("Public database request failed")
    }

    private fun checkedQuery(value: String): String {
        val result = value.trim()
        require(result.length in 2..160 && result.none { it.isISOControl() }) {
            "Enter a search term between 2 and 160 characters"
        }
        require(!result.startsWith(">") && !result.contains("#CHROM", ignoreCase = true)) {
            "Enter a public gene/protein name or accession, not a FASTA/VCF record"
        }
        val aminoAcids = Regex("[ACDEFGHIKLMNPQRSTVWYBXZJUOacdefghiklmnpqrstvwybxzjuo]+")
        require(result.length < 25 || !aminoAcids.matches(result)) {
            "Do not submit raw biological sequences to public search providers; use a public accession"
        }
        return result
    }

    private fun checkedAccession(value: String): String {
        val result = value.trim()
        require(result.matches(Regex("[A-Za-z0-9_.-]{1,40}"))) { "Invalid public accession" }
        return result
    }

    private fun checkedLimit(value: Int): Int {
        require(value in 1..50) { "Search result limit must be between 1 and 50" }
        return value
    }

    private fun encode(value: String) = URLEncoder.encode(value, Charsets.UTF_8.name())

    companion object {
        private val ALLOWED_HOSTS = setOf("eutils.ncbi.nlm.nih.gov", "rest.uniprot.org", "files.rcsb.org")
        private const val MAX_RETRIES = 2
        internal fun retryDelayMillis(attempt: Int, retryAfterSeconds: String?): Long {
            require(attempt in 0..MAX_RETRIES)
            val serverDelay = retryAfterSeconds?.trim()?.toLongOrNull()
                ?.coerceIn(0L, 2L)?.times(1_000L)
            return serverDelay ?: (250L shl attempt)
        }
        private const val CONNECT_TIMEOUT_MS = 10_000
        private const val READ_TIMEOUT_MS = 20_000
        private const val MAX_METADATA_BYTES = 2 * 1024 * 1024
        private const val MAX_SEQUENCE_BYTES = 5 * 1024 * 1024
        private const val MAX_STRUCTURE_BYTES = 16 * 1024 * 1024
    }
}

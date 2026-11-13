package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.json.JSONObject

class CommonsImageSearchClientTest {
    private fun payload(license: String = "CC BY-SA 4.0", thumbnail: String = "https://upload.wikimedia.org/thumb.jpg") =
        JSONObject().put("query", JSONObject().put("pages", org.json.JSONArray().put(
            JSONObject().put("title", "File:Metabolic pathway.png").put("imageinfo", org.json.JSONArray().put(
                JSONObject().put("thumburl", thumbnail)
                    .put("url", "https://upload.wikimedia.org/original.png")
                    .put("extmetadata", JSONObject()
                        .put("LicenseShortName", JSONObject().put("value", license))
                        .put("LicenseUrl", JSONObject().put("value", "https://creativecommons.org/licenses/by-sa/4.0/"))
                        .put("Artist", JSONObject().put("value", "<a href='https://example.org'>A. Researcher</a>")))
            ))
        ))).toString()

    @Test fun parsesLicenseAndAttributionMetadata() {
        val result = CommonsImageSearchClient.parseResponse(payload()).single()
        assertEquals("CC BY-SA 4.0", result.licenseName)
        assertEquals("A. Researcher", result.attribution)
        assertTrue(result.sourcePageUrl.startsWith("https://commons.wikimedia.org/wiki/"))
    }

    @Test fun excludesUnknownLicenseAndUntrustedImageHosts() {
        assertTrue(CommonsImageSearchClient.parseResponse(payload(license = "")).isEmpty())
        assertTrue(CommonsImageSearchClient.parseResponse(payload(thumbnail = "https://evil.example/image.png")).isEmpty())
    }

    @Test fun boundedReaderRejectsOversizedPayload() {
        val error = runCatching { CommonsImageSearchClient.readBounded("12345".byteInputStream(), 4) }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }
}

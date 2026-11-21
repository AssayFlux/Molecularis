package org.assayflux.molecularis

import android.annotation.SuppressLint
import android.graphics.Bitmap
import android.graphics.Canvas
import android.database.Cursor
import android.net.Uri
import android.provider.OpenableColumns
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.widget.FrameLayout
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material3.Button
import androidx.compose.material3.Surface
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.webkit.WebViewAssetLoader
import androidx.webkit.WebViewClientCompat
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.util.zip.GZIPInputStream

private const val VIEWER_URL = "https://appassets.androidplatform.net/assets/structure-viewer/structure-viewer.html"
private const val MAX_STRUCTURE_SOURCE_BYTES = 16 * 1024 * 1024

private data class ImportedStructure(
    val payloadJson: String,
    val name: String,
    val sourceHash: String,
    val sessionJson: String,
)

private fun readDisplayName(context: android.content.Context, uri: Uri): String {
    val cursor: Cursor? = context.contentResolver.query(
        uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
    )
    return cursor.use {
        if (it != null && it.moveToFirst()) it.getString(0) ?: "structure"
        else uri.lastPathSegment ?: "structure"
    }
}

private fun readBounded(context: android.content.Context, uri: Uri, gzip: Boolean): ByteArray {
    val input = context.contentResolver.openInputStream(uri)
        ?: error("The selected document could not be opened")
    val decoded = if (gzip) GZIPInputStream(input) else input
    return decoded.use { stream ->
        val output = ByteArrayOutputStream()
        val buffer = ByteArray(32 * 1024)
        var total = 0
        while (true) {
            val count = stream.read(buffer)
            if (count < 0) break
            total += count
            require(total <= MAX_STRUCTURE_SOURCE_BYTES) {
                "Structure file exceeds the 16 MiB import limit"
            }
            output.write(buffer, 0, count)
        }
        output.toByteArray()
    }
}

/** Offline-first structure viewer with bounded SAF import; no network or generic JS bridge. */
@SuppressLint("SetJavaScriptEnabled")
@Composable
internal fun StructureViewerPreview(publicRecord: PublicScientificRecord? = null) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var payloadJson by remember { mutableStateOf<String?>(null) }
    var sessionExportJson by remember { mutableStateOf<String?>(null) }
    var pendingSessionJson by remember { mutableStateOf<String?>(null) }
    var pendingSvg by remember { mutableStateOf<String?>(null) }
    var viewerStateJson by remember { mutableStateOf<String?>(null) }
    var viewerWebView by remember { mutableStateOf<WebView?>(null) }
    var fullScreen by remember { mutableStateOf(false) }
    var pendingPngBitmap by remember { mutableStateOf<Bitmap?>(null) }
    var sourceLabel by remember { mutableStateOf("Synthetic preview fixture") }
    var importMessage by remember {
        mutableStateOf("Choose a local PDB or mmCIF file to inspect it offline.")
    }
    LaunchedEffect(publicRecord?.sha256) {
        val fetched = publicRecord
        if (fetched != null && fetched.format.equals("mmCIF", ignoreCase = true)) {
            importMessage = "Preparing retrieved public structure for the offline viewer..."
            val result = withContext(Dispatchers.IO) {
                runCatching {
                    require(fetched.content.toByteArray(Charsets.UTF_8).size <= MAX_STRUCTURE_SOURCE_BYTES) {
                        "Retrieved structure exceeds the 16 MiB viewer parser limit"
                    }
                    if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
                    val envelope = JSONObject(
                        Python.getInstance().getModule("molecularis_probe")
                            .callAttr("prepare_structure_viewer_import", fetched.content, "mmcif")
                            .toString(),
                    )
                    ImportedStructure(
                        payloadJson = envelope.getJSONObject("payload").toString(),
                        name = "RCSB PDB ${fetched.accession}",
                        sourceHash = envelope.getJSONObject("preparation").getString("source_sha256"),
                        sessionJson = envelope.getString("session_export_json"),
                    )
                }
            }
            result.fold(
                { imported ->
                    payloadJson = imported.payloadJson
                    sessionExportJson = imported.sessionJson
                    viewerStateJson = null
                    sourceLabel = imported.name
                    importMessage = "Retrieved from RCSB PDB · parsed and validated · SHA-256 ${imported.sourceHash.take(16)}…"
                },
                { error ->
                    importMessage = "Public structure parsing failed: ${error.message ?: error.javaClass.simpleName}"
                },
            )
        }
    }
    val exportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/json"),
    ) { uri ->
        val export = pendingSessionJson
        pendingSessionJson = null
        if (uri != null && export != null) {
            scope.launch {
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        context.contentResolver.openOutputStream(uri, "w")?.use { output ->
                            output.write(export.toByteArray(Charsets.UTF_8))
                        } ?: error("The selected export destination could not be opened")
                    }
                }
                importMessage = result.fold(
                    { "Session exported successfully." },
                    { error -> "Export failed: " + (error.message ?: error.javaClass.simpleName) },
                )
            }
        }
    }
    val svgExportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("image/svg+xml"),
    ) { uri ->
        val svg = pendingSvg
        pendingSvg = null
        if (uri != null && svg != null) {
            scope.launch {
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        context.contentResolver.openOutputStream(uri, "w")?.use { output ->
                            output.write(svg.toByteArray(Charsets.UTF_8))
                        } ?: error("The selected SVG destination could not be opened")
                    }
                }
                importMessage = result.fold(
                    { "SVG snapshot exported successfully." },
                    { error -> "SVG export failed: " + (error.message ?: error.javaClass.simpleName) },
                )
            }
        }
    }
    val pngExportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("image/png"),
    ) { uri ->
        val bitmap = pendingPngBitmap
        pendingPngBitmap = null
        if (uri != null && bitmap != null) {
            scope.launch {
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        context.contentResolver.openOutputStream(uri, "w")?.use { output ->
                            check(bitmap.compress(Bitmap.CompressFormat.PNG, 100, output)) {
                                "PNG encoding failed"
                            }
                        } ?: error("The selected PNG destination could not be opened")
                    }
                }
                bitmap.recycle()
                importMessage = result.fold(
                    { "PNG snapshot exported successfully." },
                    { error -> "PNG export failed: " + (error.message ?: error.javaClass.simpleName) },
                )
            }
        } else {
            bitmap?.recycle()
        }
    }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            scope.launch {
                importMessage = "Reading and validating structure..."
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        val name = readDisplayName(context, uri)
                        val lowerName = name.lowercase(java.util.Locale.ROOT).removeSuffix(".gz")
                        val format = when {
                            lowerName.endsWith(".pdb") || lowerName.endsWith(".ent") -> "pdb"
                            lowerName.endsWith(".cif") || lowerName.endsWith(".mmcif") -> "mmcif"
                            else -> error(
                                "Unsupported file extension. Select PDB, ENT, CIF, mmCIF or a .gz-compressed version.",
                            )
                        }
                        val bytes = readBounded(context, uri, name.endsWith(".gz", ignoreCase = true))
                        val sourceText = Charsets.UTF_8.newDecoder()
                            .onMalformedInput(CodingErrorAction.REPORT)
                            .onUnmappableCharacter(CodingErrorAction.REPORT)
                            .decode(ByteBuffer.wrap(bytes)).toString()
                        require(!sourceText.contains('\u0000')) {
                            "Structure file is not valid UTF-8 text"
                        }
                        if (!Python.isStarted()) {
                            Python.start(AndroidPlatform(context.applicationContext))
                        }
                        val envelope = JSONObject(
                            Python.getInstance().getModule("molecularis_probe")
                                .callAttr("prepare_structure_viewer_import", sourceText, format)
                                .toString(),
                        )
                        val payload = envelope.getJSONObject("payload")
                        val sourceHash = envelope.getJSONObject("preparation")
                            .getString("source_sha256")
                        val sessionJson = envelope.getString("session_export_json")
                        ImportedStructure(payload.toString(), name, sourceHash, sessionJson)
                    }
                }
                result.fold(
                    { imported ->
                        payloadJson = imported.payloadJson
                        sessionExportJson = imported.sessionJson
                        viewerStateJson = null
                        sourceLabel = imported.name
                        importMessage = "Imported ${imported.name} · SHA-256 ${imported.sourceHash.take(16)}…"
                    },
                    { error ->
                        importMessage = "Import failed: " +
                            (error.message ?: error.javaClass.simpleName)
                    },
                )
            }
        }
    }
    val fallbackPayload = remember {
        """{"schema":"kinetics.structure-view.v1","source_format":"pdb","coordinate_unit":"angstrom","atom_count":8,"atoms":[{"serial":1,"name":"N","residue":"GLY","chain":"A","residue_number":1,"element":"N","xyz":[0.0,0.0,0.0]},{"serial":2,"name":"CA","residue":"GLY","chain":"A","residue_number":1,"element":"C","xyz":[1.45,0.1,0.0]},{"serial":3,"name":"C","residue":"GLY","chain":"A","residue_number":1,"element":"C","xyz":[2.0,1.48,0.1]},{"serial":4,"name":"O","residue":"GLY","chain":"A","residue_number":1,"element":"O","xyz":[1.35,2.45,0.1]},{"serial":5,"name":"N","residue":"ALA","chain":"A","residue_number":2,"element":"N","xyz":[3.25,1.55,0.0]},{"serial":6,"name":"CA","residue":"ALA","chain":"A","residue_number":2,"element":"C","xyz":[4.0,2.8,0.2]},{"serial":7,"name":"C","residue":"ALA","chain":"A","residue_number":2,"element":"C","xyz":[5.45,2.55,0.0]},{"serial":8,"name":"O","residue":"ALA","chain":"A","residue_number":2,"element":"O","xyz":[6.1,3.5,0.1]}],"limitations":["Synthetic UI preview fixture only; not experimental structure data.","Coordinates and annotations only; no inferred bonds or biological interpretation."]}"""
    }
    val activePayload = payloadJson ?: fallbackPayload
    val assetLoader = remember(context) {
        WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(context))
            .build()
    }
    val webView = remember(context, activePayload) {
        WebView(context).apply {
            settings.javaScriptEnabled = true
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            settings.domStorageEnabled = false
            settings.javaScriptCanOpenWindowsAutomatically = false
            settings.setSupportMultipleWindows(false)
            settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_NEVER_ALLOW
            settings.loadsImagesAutomatically = false
            settings.blockNetworkLoads = true
            webViewClient = object : WebViewClientCompat() {
                override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest) =
                    assetLoader.shouldInterceptRequest(request.url)

                override fun shouldOverrideUrlLoading(
                    view: WebView, request: WebResourceRequest,
                ): Boolean = true

                override fun onPageFinished(view: WebView, url: String) {
                    if (url == VIEWER_URL) {
                        val encoded = JSONObject.quote(activePayload)
                        view.evaluateJavascript(
                            "window.MolecularisStructureViewer.load(JSON.parse($encoded));",
                        ) {
                            val savedState = viewerStateJson
                            if (savedState != null) {
                                val stateLiteral = JSONObject.quote(savedState)
                                view.evaluateJavascript(
                                    "window.MolecularisStructureViewer.setState(JSON.parse($stateLiteral));",
                                    null,
                                )
                            }
                        }
                    }
                }
            }
            loadUrl(VIEWER_URL)
        }
    }
    DisposableEffect(webView) {
        onDispose {
            if (viewerWebView === webView) viewerWebView = null
            pendingPngBitmap?.recycle()
            pendingPngBitmap = null
            pendingSvg = null
            pendingSessionJson = null
            webView.stopLoading()
            webView.loadUrl("about:blank")
            webView.destroy()
        }
    }
    Card {
        Column(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(
                "Offline-first structure viewer",
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.onSurface,
            )
            Text(sourceLabel, style = MaterialTheme.typography.labelMedium)
            Text(importMessage, style = MaterialTheme.typography.bodySmall)
            Button(onClick = { picker.launch(arrayOf("*/*")) }) {
                Text("Import PDB / mmCIF / .gz")
            }
            Button(onClick = { fullScreen = true }, enabled = payloadJson != null) {
                Text("Open full-screen structure viewer")
            }
            Button(
                onClick = {
                    val view = viewerWebView
                    val base = sessionExportJson
                    if (view == null || base == null) {
                        importMessage = "Session export is unavailable until a structure is loaded."
                    } else {
                        view.evaluateJavascript("window.MolecularisStructureViewer.getState()") { rawState ->
                            runCatching {
                                val state = JSONObject(rawState ?: error("Viewer state is unavailable"))
                                viewerStateJson = state.toString()
                                val session = JSONObject(base)
                                session.put("viewer_state", state)
                                session.put("render_state", "viewer_state_saved")
                                val limitations = JSONArray()
                                val previous = session.optJSONArray("export_limitations")
                                if (previous != null) {
                                    for (index in 0 until previous.length()) {
                                        val item = previous.optString(index)
                                        if (!item.contains("interactive viewer state")) {
                                            limitations.put(item)
                                        }
                                    }
                                }
                                limitations.put("PNG and SVG snapshots are separate files, not embedded images.")
                                session.put("export_limitations", limitations)
                                val encoded = session.toString()
                                require(encoded.toByteArray(Charsets.UTF_8).size <= 64 * 1024 * 1024) {
                                    "Session export exceeds the 64 MiB limit."
                                }
                                pendingSessionJson = encoded
                                val baseName = sourceLabel.substringBeforeLast('.', sourceLabel)
                                exportPicker.launch("$baseName.molecularis-session.json")
                            }.onFailure { error ->
                                importMessage = "Session state capture failed: " +
                                    (error.message ?: error.javaClass.simpleName)
                            }
                        }
                    }
                },
                enabled = sessionExportJson != null,
            ) {
                Text("Export session JSON + view state")
            }
            Button(
                onClick = {
                    val view = viewerWebView
                    if (view == null) {
                        importMessage = "SVG export is unavailable until the viewer is ready."
                    } else {
                        view.evaluateJavascript("window.MolecularisStructureViewer.exportSvg()") { rawSvg ->
                            runCatching {
                                val raw = rawSvg ?: error("Viewer did not return an SVG snapshot")
                                val svg = JSONArray("[$raw]").getString(0)
                                require(svg.startsWith("<svg") && svg.endsWith("</svg>")) {
                                    "Viewer returned an invalid SVG snapshot."
                                }
                                require(svg.toByteArray(Charsets.UTF_8).size <= 32 * 1024 * 1024) {
                                    "SVG export exceeds the 32 MiB limit."
                                }
                                pendingSvg = svg
                                val baseName = sourceLabel.substringBeforeLast('.', sourceLabel)
                                svgExportPicker.launch("$baseName.svg")
                            }.onFailure { error ->
                                importMessage = "SVG capture failed: " +
                                    (error.message ?: error.javaClass.simpleName)
                            }
                        }
                    }
                },
                enabled = payloadJson != null,
            ) {
                Text("Export viewer SVG")
            }
            Button(
                onClick = {
                    val view = viewerWebView
                    val state = viewerStateJson
                    if (view != null && state != null) {
                        val literal = JSONObject.quote(state)
                        view.evaluateJavascript(
                            "window.MolecularisStructureViewer.setState(JSON.parse($literal));",
                            null,
                        )
                    }
                },
                enabled = payloadJson != null && viewerStateJson != null,
            ) {
                Text("Restore saved view state")
            }
            Button(
                onClick = {
                    val view = viewerWebView
                    if (view == null || view.width < 1 || view.height < 1) {
                        importMessage = "PNG export unavailable until the viewer is laid out."
                    } else if (view.width.toLong() * view.height.toLong() > 16_777_216L) {
                        importMessage = "PNG snapshot exceeds the 16-megapixel safety limit."
                    } else {
                        runCatching {
                            Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
                                .also { bitmap -> view.draw(Canvas(bitmap)) }
                        }.onSuccess { bitmap ->
                            pendingPngBitmap = bitmap
                            val baseName = sourceLabel.substringBeforeLast('.', sourceLabel)
                            pngExportPicker.launch("$baseName.png")
                        }.onFailure { error ->
                            importMessage = "PNG capture failed: " +
                                (error.message ?: error.javaClass.simpleName)
                        }
                    }
                },
                enabled = payloadJson != null,
            ) {
                Text("Export viewer PNG")
            }
            if (fullScreen) {
                Dialog(
                    onDismissRequest = { fullScreen = false },
                    properties = DialogProperties(usePlatformDefaultWidth = false),
                ) {
                    Surface(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing), color = MaterialTheme.colorScheme.background) {
                        Column(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Structure viewer", style = MaterialTheme.typography.titleLarge)
                                Button(onClick = { fullScreen = false }) { Text("Close") }
                            }
                            AndroidView(
                                factory = { FrameLayout(it).apply { viewerWebView = webView; addView(webView) } },
                                update = { frame ->
                                    viewerWebView = webView
                                    if (frame.childCount != 1 || frame.getChildAt(0) !== webView) {
                                        frame.removeAllViews()
                                        frame.addView(webView)
                                    }
                                },
                                modifier = Modifier.fillMaxWidth().weight(1f),
                            )
                        }
                    }
                }
            } else {
                AndroidView(
                    factory = { FrameLayout(it).apply { viewerWebView = webView; addView(webView) } },
                    update = { frame ->
                        viewerWebView = webView
                        if (frame.childCount != 1 || frame.getChildAt(0) !== webView) {
                            frame.removeAllViews()
                            frame.addView(webView)
                        }
                    },
                    modifier = Modifier.fillMaxWidth().height(440.dp),
                )
            }
        }
    }
}

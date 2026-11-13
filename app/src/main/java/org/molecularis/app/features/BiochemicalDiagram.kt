package org.molecularis.app.features

enum class BiochemicalDiagramTemplate(val label: String) {
    METABOLIC_PATHWAY("Metabolic pathway"), REACTION_MECHANISM("Reaction mechanism"),
    FEEDBACK_REGULATION("Feedback regulation"), MOLECULAR_INTERACTION("Molecular interaction")
}
enum class DiagramNodeKind { METABOLITE, ENZYME, REGULATOR, COMPLEX, COMPARTMENT }
enum class DiagramConnectionKind { REACTION, ACTIVATION, INHIBITION, BINDING, TRANSPORT }

data class DiagramNode(
    val id: String, val label: String, val detail: String = "", val revealStep: Int,
    val kind: DiagramNodeKind = DiagramNodeKind.METABOLITE,
    /** Center coordinates in the 0–1000 SVG design grid. */
    val x: Float? = null, val y: Float? = null
)
data class DiagramConnection(
    val fromId: String, val toId: String, val label: String = "",
    val kind: DiagramConnectionKind = DiagramConnectionKind.REACTION
)
data class DiagramStep(val index: Int, val title: String, val explanation: String)
data class BiochemicalDiagram(
    val id: String, val title: String, val nodes: List<DiagramNode>,
    val connections: List<DiagramConnection>, val steps: List<DiagramStep>,
    val template: BiochemicalDiagramTemplate = BiochemicalDiagramTemplate.METABOLIC_PATHWAY
)

object BiochemicalDiagramTemplates {
    fun create(template: BiochemicalDiagramTemplate, title: String, components: List<String>, details: List<String> = emptyList()): BiochemicalDiagram {
        val names = components.map { it.trim() }.filter(String::isNotBlank)
        require(names.size in 2..10) { "Enter between 2 and 10 diagram components." }
        val nodes = mutableListOf<DiagramNode>()
        val edges = mutableListOf<DiagramConnection>()
        val steps = mutableListOf<DiagramStep>()
        fun node(id: String, label: String, kind: DiagramNodeKind, x: Float, y: Float, detail: String = "") {
            val index = nodes.size
            nodes += DiagramNode(id, label.take(160), detail.take(500), index, kind, x, y)
            steps += DiagramStep(index, label.take(160), detail.ifBlank { "Introduce $label." }.take(1000))
        }
        when (template) {
            BiochemicalDiagramTemplate.METABOLIC_PATHWAY -> {
                names.forEachIndexed { i, name ->
                    node("metabolite-$i", name, DiagramNodeKind.METABOLITE, 500f, 110f + i * 165f)
                    if (i > 0) edges += DiagramConnection("metabolite-${i - 1}", "metabolite-$i", details.getOrNull(i - 1).orEmpty())
                }
            }
            BiochemicalDiagramTemplate.REACTION_MECHANISM -> {
                require(names.size in 3..4) { "A reaction mechanism needs substrate, enzyme, product and optionally a cofactor." }
                node("substrate", names[0], DiagramNodeKind.METABOLITE, 170f, 360f)
                node("enzyme", names[1], DiagramNodeKind.ENZYME, 500f, 150f, details.getOrNull(0).orEmpty())
                node("product", names[2], DiagramNodeKind.METABOLITE, 830f, 360f)
                edges += DiagramConnection("substrate", "product", details.getOrNull(1).orEmpty().ifBlank { "conversion" })
                edges += DiagramConnection("enzyme", "product", "catalyses", DiagramConnectionKind.ACTIVATION)
                if (names.size == 4) {
                    node("cofactor", names[3], DiagramNodeKind.COMPARTMENT, 500f, 650f)
                    edges += DiagramConnection("cofactor", "product", "cofactor", DiagramConnectionKind.TRANSPORT)
                }
            }
            BiochemicalDiagramTemplate.FEEDBACK_REGULATION -> {
                require(names.size in 3..4) { "Feedback regulation needs input, control enzyme, end product and optionally a regulator." }
                node("input", names[0], DiagramNodeKind.METABOLITE, 160f, 360f)
                node("control-enzyme", names[1], DiagramNodeKind.ENZYME, 500f, 360f, details.getOrNull(0).orEmpty())
                node("end-product", names[2], DiagramNodeKind.METABOLITE, 840f, 360f)
                edges += DiagramConnection("input", "control-enzyme", "substrate")
                edges += DiagramConnection("control-enzyme", "end-product", "pathway output")
                edges += DiagramConnection("end-product", "control-enzyme", "feedback inhibition", DiagramConnectionKind.INHIBITION)
                if (names.size == 4) {
                    node("regulator", names[3], DiagramNodeKind.REGULATOR, 500f, 650f)
                    edges += DiagramConnection("regulator", "control-enzyme", "regulation", DiagramConnectionKind.ACTIVATION)
                }
            }
            BiochemicalDiagramTemplate.MOLECULAR_INTERACTION -> {
                require(names.size in 3..4) { "Molecular interaction needs two molecules, a complex and optionally a regulator." }
                node("molecule-a", names[0], DiagramNodeKind.METABOLITE, 190f, 250f)
                node("molecule-b", names[1], DiagramNodeKind.METABOLITE, 810f, 250f)
                node("complex", names[2], DiagramNodeKind.COMPLEX, 500f, 570f, details.getOrNull(0).orEmpty())
                edges += DiagramConnection("molecule-a", "complex", "binding", DiagramConnectionKind.BINDING)
                edges += DiagramConnection("molecule-b", "complex", "binding", DiagramConnectionKind.BINDING)
                if (names.size == 4) {
                    node("regulator", names[3], DiagramNodeKind.REGULATOR, 500f, 100f)
                    edges += DiagramConnection("regulator", "complex", "modulates", DiagramConnectionKind.ACTIVATION)
                }
            }
        }
        return BiochemicalDiagram("diagram-${template.name.lowercase()}", title.trim().ifBlank { template.label }.take(160), nodes, edges, steps, template)
    }
}

object BiochemicalDiagramValidator {
    fun validate(diagram: BiochemicalDiagram): List<String> {
        val errors = mutableListOf<String>()
        if (diagram.id.isBlank() || diagram.id.length > 80) errors += "Diagram ID must contain 1–80 characters."
        if (diagram.title.isBlank() || diagram.title.length > 160) errors += "Diagram title must contain 1–160 characters."
        if (diagram.nodes.isEmpty() || diagram.nodes.size > 40) errors += "A diagram must contain 1–40 nodes."
        if (diagram.steps.isEmpty() || diagram.steps.size > 40) errors += "A diagram must contain 1–40 reveal steps."
        val ids = diagram.nodes.map { it.id }
        if (ids.any { it.isBlank() || it.length > 64 }) errors += "Node IDs must contain 1–64 characters."
        if (ids.distinct().size != ids.size) errors += "Node IDs must be unique."
        if (diagram.nodes.any { it.label.isBlank() || it.label.length > 160 || it.detail.length > 500 }) errors += "Node labels must contain 1–160 characters and details must not exceed 500."
        if (diagram.nodes.any { n -> (n.x != null && (!n.x.isFinite() || n.x !in 0f..1000f)) || (n.y != null && (!n.y.isFinite() || n.y !in 0f..1000f)) }) errors += "Node coordinates must be finite values between 0 and 1000."
        val indices = diagram.steps.map { it.index }.sorted()
        if (indices != diagram.steps.indices.toList()) errors += "Reveal step indices must be contiguous and zero-based."
        if (diagram.nodes.any { it.revealStep !in indices }) errors += "Every node must reference an existing reveal step."
        if (diagram.connections.size > 80) errors += "A diagram cannot contain more than 80 connections."
        diagram.connections.forEach { e ->
            if (e.fromId !in ids || e.toId !in ids) errors += "A connection references an unknown node."
            if (e.fromId == e.toId) errors += "A node cannot connect to itself."
            if (e.label.length > 120) errors += "Connection labels must not exceed 120 characters."
        }
        if (diagram.steps.any { it.title.isBlank() || it.title.length > 160 || it.explanation.length > 1000 }) errors += "Reveal step titles must contain 1–160 characters and explanations must not exceed 1000."
        return errors.distinct()
    }
}

object BiochemicalSvgRenderer {
    fun render(diagram: BiochemicalDiagram, visibleThroughStep: Int = Int.MAX_VALUE): String {
        val errors = BiochemicalDiagramValidator.validate(diagram)
        require(errors.isEmpty()) { errors.joinToString(" ") }
        val visible = diagram.nodes.filter { it.revealStep <= visibleThroughStep }
        val ids = visible.map { it.id }.toSet()
        val positions = visible.mapIndexed { i, n -> n.id to Pair(n.x ?: 500f, n.y ?: (110f + i * 165f)) }.toMap()
        val height = ((positions.values.maxOfOrNull { it.second } ?: 650f) + 150f).toInt().coerceAtLeast(800)
        val body = buildString {
            append("<title>").append(escape(diagram.title)).append("</title><defs>")
            append("<marker id=\"arrow\" markerWidth=\"12\" markerHeight=\"12\" refX=\"10\" refY=\"4\" orient=\"auto\"><path d=\"M0,0 L0,8 L11,4 z\" fill=\"#526579\"/></marker>")
            append("<marker id=\"greenArrow\" markerWidth=\"12\" markerHeight=\"12\" refX=\"10\" refY=\"4\" orient=\"auto\"><path d=\"M0,0 L0,8 L11,4 z\" fill=\"#16845b\"/></marker>")
            append("<marker id=\"redBar\" markerWidth=\"8\" markerHeight=\"16\" refX=\"4\" refY=\"8\" orient=\"auto\"><path d=\"M4,1 L4,15\" stroke=\"#c2413b\" stroke-width=\"3\"/></marker></defs>")
            diagram.connections.filter { it.fromId in ids && it.toId in ids }.forEach { e ->
                val a = positions.getValue(e.fromId); val b = positions.getValue(e.toId)
                val color = when (e.kind) { DiagramConnectionKind.INHIBITION -> "#c2413b"; DiagramConnectionKind.ACTIVATION -> "#16845b"; DiagramConnectionKind.BINDING -> "#7654a8"; DiagramConnectionKind.TRANSPORT -> "#2477a8"; else -> "#526579" }
                val marker = when (e.kind) { DiagramConnectionKind.INHIBITION -> "redBar"; DiagramConnectionKind.ACTIVATION -> "greenArrow"; else -> "arrow" }
                val dash = if (e.kind == DiagramConnectionKind.INHIBITION) " stroke-dasharray=\"9 7\"" else ""
                if (e.kind == DiagramConnectionKind.INHIBITION) {
                    val controlY = maxOf(a.second, b.second) + 150f
                    append("<path d=\"M").append(a.first).append(" ").append(a.second).append(" Q").append((a.first + b.first) / 2f).append(" ").append(controlY).append(" ").append(b.first).append(" ").append(b.second)
                        .append("\" fill=\"none\" stroke=\"").append(color).append("\" stroke-width=\"4\"").append(dash).append(" marker-end=\"url(#").append(marker).append(")\"/>")
                    if (e.label.isNotBlank()) append("<text x=\"").append((a.first + b.first) / 2f).append("\" y=\"").append(controlY - 8f)
                        .append("\" text-anchor=\"middle\" font-size=\"18\" fill=\"").append(color).append("\">").append(escape(e.label)).append("</text>")
                } else {
                    append("<line x1=\"").append(a.first).append("\" y1=\"").append(a.second).append("\" x2=\"").append(b.first).append("\" y2=\"").append(b.second)
                        .append("\" stroke=\"").append(color).append("\" stroke-width=\"4\"").append(dash).append(" marker-end=\"url(#").append(marker).append(")\"/>")
                    if (e.label.isNotBlank()) append("<text x=\"").append((a.first + b.first) / 2f).append("\" y=\"").append((a.second + b.second) / 2f - 12f)
                        .append("\" text-anchor=\"middle\" font-size=\"18\" fill=\"").append(color).append("\">").append(escape(e.label)).append("</text>")
                }
            }
            visible.forEach { n ->
                val c = positions.getValue(n.id); val x = c.first - 120f; val y = c.second - 52f
                when (n.kind) {
                    DiagramNodeKind.METABOLITE -> append("<rect x=\"$x\" y=\"$y\" width=\"240\" height=\"104\" rx=\"22\" fill=\"#e8f2fa\" stroke=\"#39749a\" stroke-width=\"3\"/>")
                    DiagramNodeKind.ENZYME -> append("<rect x=\"$x\" y=\"$y\" width=\"240\" height=\"104\" rx=\"48\" fill=\"#e9f5ec\" stroke=\"#39845a\" stroke-width=\"3\"/>")
                    DiagramNodeKind.COMPLEX -> append("<ellipse cx=\"").append(c.first).append("\" cy=\"").append(c.second).append("\" rx=\"120\" ry=\"52\" fill=\"#f2eafa\" stroke=\"#7654a8\" stroke-width=\"3\"/>")
                    DiagramNodeKind.COMPARTMENT -> append("<rect x=\"$x\" y=\"$y\" width=\"240\" height=\"104\" rx=\"8\" fill=\"#fff4df\" stroke=\"#b7791f\" stroke-width=\"3\" stroke-dasharray=\"8 5\"/>")
                    DiagramNodeKind.REGULATOR -> append("<polygon points=\"").append(c.first).append(",").append(c.second - 62f).append(" ").append(c.first + 130f).append(",").append(c.second).append(" ").append(c.first).append(",").append(c.second + 62f).append(" ").append(c.first - 130f).append(",").append(c.second).append("\" fill=\"#fff0e8\" stroke=\"#c16b3b\" stroke-width=\"3\"/>")
                }
                val titleY = c.second + (if (n.detail.isBlank()) 7f else -8f)
                val titleSize = when { n.label.length > 42 -> 13; n.label.length > 30 -> 16; n.label.length > 22 -> 19; else -> 22 }
                append("<text x=\"").append(c.first).append("\" y=\"").append(titleY)
                    .append("\" text-anchor=\"middle\" font-size=\"").append(titleSize).append("\" font-weight=\"600\" fill=\"#172b3a\">").append(escape(n.label.take(70))).append("</text>")
                if (n.detail.isNotBlank()) append("<text x=\"").append(c.first).append("\" y=\"").append(c.second + 24f)
                    .append("\" text-anchor=\"middle\" font-size=\"13\" fill=\"#40576a\">").append(escape(n.detail.take(45))).append("</text>")
            }
        }
        return "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1000 $height\" role=\"img\">$body</svg>"
    }
    private fun escape(value: String) = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")
}

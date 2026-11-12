package org.molecularis.app.features

data class DiagramNode(
    val id: String,
    val label: String,
    val detail: String = "",
    val revealStep: Int
)

data class DiagramConnection(
    val fromId: String,
    val toId: String,
    val label: String = ""
)

data class DiagramStep(
    val index: Int,
    val title: String,
    val explanation: String
)

data class BiochemicalDiagram(
    val id: String,
    val title: String,
    val nodes: List<DiagramNode>,
    val connections: List<DiagramConnection>,
    val steps: List<DiagramStep>
)

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
        if (diagram.nodes.any { it.label.isBlank() || it.label.length > 160 || it.detail.length > 500 }) {
            errors += "Node labels must contain 1–160 characters and details must not exceed 500."
        }
        val stepIndices = diagram.steps.map { it.index }.sorted()
        if (stepIndices != diagram.steps.indices.toList()) errors += "Reveal step indices must be contiguous and zero-based."
        if (diagram.nodes.any { it.revealStep !in stepIndices }) errors += "Every node must reference an existing reveal step."
        if (diagram.connections.size > 80) errors += "A diagram cannot contain more than 80 connections."
        diagram.connections.forEach { edge ->
            if (edge.fromId !in ids || edge.toId !in ids) errors += "A connection references an unknown node."
            if (edge.fromId == edge.toId) errors += "A node cannot connect to itself."
            if (edge.label.length > 120) errors += "Connection labels must not exceed 120 characters."
        }
        if (diagram.steps.any { it.title.isBlank() || it.title.length > 160 || it.explanation.length > 1000 }) {
            errors += "Reveal step titles must contain 1–160 characters and explanations must not exceed 1000."
        }
        return errors.distinct()
    }
}

/**
 * Renders only the supported diagram primitives. All user-authored labels are XML-escaped;
 * arbitrary SVG, HTML, CSS, scripts, images and external references are never accepted.
 */
object BiochemicalSvgRenderer {
    fun render(diagram: BiochemicalDiagram, visibleThroughStep: Int = Int.MAX_VALUE): String {
        val errors = BiochemicalDiagramValidator.validate(diagram)
        require(errors.isEmpty()) { errors.joinToString(" ") }
        val visible = diagram.nodes.filter { it.revealStep <= visibleThroughStep }
        val visibleIds = visible.map { it.id }.toSet()
        val width = 900
        val nodeHeight = 88
        val gap = 54
        val height = (visible.size * (nodeHeight + gap) + 40).coerceAtLeast(180)
        val positions = visible.mapIndexed { index, node ->
            node.id to (30 + index * (nodeHeight + gap))
        }.toMap()
        val body = buildString {
            append("<title>").append(escape(diagram.title)).append("</title>")
            append("<defs><marker id=\"arrow\" markerWidth=\"10\" markerHeight=\"10\" refX=\"8\" refY=\"3\" orient=\"auto\"><path d=\"M0,0 L0,6 L9,3 z\" fill=\"#526579\"/></marker></defs>")
            diagram.connections.filter { it.fromId in visibleIds && it.toId in visibleIds }.forEach { edge ->
                val fromY = positions.getValue(edge.fromId)
                val toY = positions.getValue(edge.toId)
                append("<line x1=\"450\" y1=\"").append(fromY + nodeHeight)
                    .append("\" x2=\"450\" y2=\"").append(toY)
                    .append("\" stroke=\"#526579\" stroke-width=\"3\" marker-end=\"url(#arrow)\"/>")
                if (edge.label.isNotBlank()) {
                    append("<text x=\"470\" y=\"").append((fromY + nodeHeight + toY) / 2)
                        .append("\" font-size=\"18\" fill=\"#334155\">")
                        .append(escape(edge.label)).append("</text>")
                }
            }
            visible.forEach { node ->
                val y = positions.getValue(node.id)
                append("<rect x=\"120\" y=\"").append(y)
                    .append("\" width=\"660\" height=\"").append(nodeHeight)
                    .append("\" rx=\"16\" fill=\"#eef4f8\" stroke=\"#52738a\" stroke-width=\"2\"/>")
                append("<text x=\"450\" y=\"").append(y + 38)
                    .append("\" text-anchor=\"middle\" font-size=\"23\" font-weight=\"600\" fill=\"#172b3a\">")
                    .append(escape(node.label)).append("</text>")
                if (node.detail.isNotBlank()) {
                    append("<text x=\"450\" y=\"").append(y + 65)
                        .append("\" text-anchor=\"middle\" font-size=\"15\" fill=\"#40576a\">")
                        .append(escape(node.detail)).append("</text>")
                }
            }
        }
        return "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 $width $height\" role=\"img\">$body</svg>"
    }

    private fun escape(value: String): String = value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&apos;")
}

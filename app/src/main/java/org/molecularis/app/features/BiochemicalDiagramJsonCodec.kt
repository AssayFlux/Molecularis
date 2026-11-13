package org.molecularis.app.features

import org.json.JSONArray
import org.json.JSONObject

/** Stable, explicit JSON format for saving professor-edited diagrams on-device. */
object BiochemicalDiagramJsonCodec {
    private const val FORMAT_VERSION = 1

    fun encode(diagram: BiochemicalDiagram): String {
        require(BiochemicalDiagramValidator.validate(diagram).isEmpty()) { "Only valid diagrams can be saved." }
        val root = JSONObject()
            .put("formatVersion", FORMAT_VERSION)
            .put("id", diagram.id)
            .put("title", diagram.title)
            .put("template", diagram.template.name)
        root.put("nodes", JSONArray().apply {
            diagram.nodes.forEach { node ->
                put(JSONObject()
                    .put("id", node.id)
                    .put("label", node.label)
                    .put("detail", node.detail)
                    .put("revealStep", node.revealStep)
                    .put("kind", node.kind.name)
                    .put("x", node.x ?: JSONObject.NULL)
                    .put("y", node.y ?: JSONObject.NULL))
            }
        })
        root.put("connections", JSONArray().apply {
            diagram.connections.forEach { edge ->
                put(JSONObject()
                    .put("fromId", edge.fromId)
                    .put("toId", edge.toId)
                    .put("label", edge.label)
                    .put("kind", edge.kind.name))
            }
        })
        root.put("steps", JSONArray().apply {
            diagram.steps.forEach { step ->
                put(JSONObject().put("index", step.index).put("title", step.title).put("explanation", step.explanation))
            }
        })
        return root.toString()
    }

    fun decode(json: String): BiochemicalDiagram {
        require(json.length <= 256_000) { "Saved diagram data is too large." }
        val root = JSONObject(json)
        require(root.optInt("formatVersion", -1) == FORMAT_VERSION) { "This saved diagram format is not supported." }
        val nodesJson = root.getJSONArray("nodes")
        val edgesJson = root.getJSONArray("connections")
        val stepsJson = root.getJSONArray("steps")
        require(nodesJson.length() <= 40 && edgesJson.length() <= 80 && stepsJson.length() <= 40) { "Saved diagram exceeds supported limits." }
        val diagram = BiochemicalDiagram(
            id = root.getString("id"),
            title = root.getString("title"),
            template = BiochemicalDiagramTemplate.valueOf(root.getString("template")),
            nodes = (0 until nodesJson.length()).map { i ->
                val n = nodesJson.getJSONObject(i)
                DiagramNode(
                    id = n.getString("id"),
                    label = n.getString("label"),
                    detail = n.optString("detail"),
                    revealStep = n.getInt("revealStep"),
                    kind = DiagramNodeKind.valueOf(n.getString("kind")),
                    x = if (n.isNull("x")) null else n.getDouble("x").toFloat(),
                    y = if (n.isNull("y")) null else n.getDouble("y").toFloat()
                )
            },
            connections = (0 until edgesJson.length()).map { i ->
                val e = edgesJson.getJSONObject(i)
                DiagramConnection(e.getString("fromId"), e.getString("toId"), e.optString("label"), DiagramConnectionKind.valueOf(e.getString("kind")))
            },
            steps = (0 until stepsJson.length()).map { i ->
                val s = stepsJson.getJSONObject(i)
                DiagramStep(s.getInt("index"), s.getString("title"), s.optString("explanation"))
            }
        )
        val errors = BiochemicalDiagramValidator.validate(diagram)
        require(errors.isEmpty()) { "Saved diagram failed validation: " + errors.joinToString(" ") }
        return diagram
    }
}

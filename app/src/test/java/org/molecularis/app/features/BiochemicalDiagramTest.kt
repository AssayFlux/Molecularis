package org.molecularis.app.features

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class BiochemicalDiagramTest {
    private fun sample() = BiochemicalDiagram(
        id = "glycolysis-step",
        title = "Glycolysis",
        nodes = listOf(
            DiagramNode("glucose", "Glucose", "Starting substrate", 0),
            DiagramNode("g6p", "Glucose-6-phosphate", "Hexokinase", 1),
            DiagramNode("f6p", "Fructose-6-phosphate", "Phosphoglucose isomerase", 2)
        ),
        connections = listOf(
            DiagramConnection("glucose", "g6p", "ATP → ADP"),
            DiagramConnection("g6p", "f6p")
        ),
        steps = listOf(
            DiagramStep(0, "Substrate", "Introduce glucose."),
            DiagramStep(1, "Phosphorylation", "Hexokinase uses ATP."),
            DiagramStep(2, "Isomerization", "The sugar phosphate is rearranged.")
        )
    )

    @Test fun rendersOnlyNodesRevealedSoFar() {
        val first = BiochemicalSvgRenderer.render(sample(), visibleThroughStep = 0)
        assertTrue(first.contains("Glucose"))
        assertFalse(first.contains("Glucose-6-phosphate"))
        val second = BiochemicalSvgRenderer.render(sample(), visibleThroughStep = 1)
        assertTrue(second.contains("Glucose-6-phosphate"))
        assertFalse(second.contains("Fructose-6-phosphate"))
    }

    @Test fun escapesAllUserSuppliedSvgText() {
        val unsafe = sample().copy(
            title = "<script>alert(1)</script>",
            nodes = sample().nodes.mapIndexed { index, node ->
                if (index == 0) node.copy(label = "<img src=x onerror=alert(1)> & ATP") else node
            }
        )
        val svg = BiochemicalSvgRenderer.render(unsafe)
        assertFalse(svg.contains("<script>"))
        assertFalse(svg.contains("<img"))
        assertTrue(svg.contains("&lt;script&gt;"))
        assertTrue(svg.contains("&amp;"))
    }

    @Test fun rejectsDuplicateNodeIdsAndUnknownConnections() {
        val invalid = sample().copy(
            nodes = sample().nodes + sample().nodes.first(),
            connections = listOf(DiagramConnection("missing", "glucose"))
        )
        val errors = BiochemicalDiagramValidator.validate(invalid)
        assertTrue(errors.any { it.contains("unique") })
        assertTrue(errors.any { it.contains("unknown node") })
    }

    @Test fun rejectsTooManyNodesAndInvalidRevealStep() {
        val invalid = sample().copy(
            nodes = (0..40).map { DiagramNode("n$it", "Node $it", revealStep = 0) } +
                listOf(DiagramNode("bad-step", "Bad", revealStep = 99))
        )
        val errors = BiochemicalDiagramValidator.validate(invalid)
        assertTrue(errors.any { it.contains("1–40 nodes") })
        assertTrue(errors.any { it.contains("existing reveal step") })
    }
}

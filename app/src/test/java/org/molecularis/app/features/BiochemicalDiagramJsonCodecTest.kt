package org.molecularis.app.features

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class BiochemicalDiagramJsonCodecTest {
    @Test fun roundTripPreservesEditedNodesEdgesAndSteps() {
        val original = BiochemicalDiagramTemplates.create(
            BiochemicalDiagramTemplate.FEEDBACK_REGULATION,
            "Feedback control",
            listOf("Substrate", "PFK-1", "ATP", "Citrate"),
            listOf("rate-limiting enzyme")
        ).let { diagram ->
            diagram.copy(
                nodes = diagram.nodes.map { if (it.id == "control-enzyme") it.copy(label = "PFK-1 (edited)", detail = "Allosteric control") else it },
                connections = diagram.connections.map { if (it.kind == DiagramConnectionKind.INHIBITION) it.copy(label = "ATP-mediated inhibition") else it }
            )
        }
        val restored = BiochemicalDiagramJsonCodec.decode(BiochemicalDiagramJsonCodec.encode(original))
        assertEquals(original, restored)
    }

    @Test fun rejectsUnsupportedFormatVersion() {
        assertThrows(IllegalArgumentException::class.java) {
            BiochemicalDiagramJsonCodec.decode("""{"formatVersion":99}""")
        }
    }

    @Test fun rejectsInvalidDiagramOnEncode() {
        val invalid = BiochemicalDiagram("bad", "Bad", emptyList(), emptyList(), emptyList())
        assertThrows(IllegalArgumentException::class.java) { BiochemicalDiagramJsonCodec.encode(invalid) }
    }
}

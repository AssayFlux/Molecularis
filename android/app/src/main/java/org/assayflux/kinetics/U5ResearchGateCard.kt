package org.assayflux.molecularis

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/** Visible dependency boundary: unavailable PGx and host-only engines are not fake launch actions. */
@Composable
internal fun U5ResearchGateCard() {
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("PGx · NOT ENABLED", style = MaterialTheme.typography.titleSmall)
            Text(
                "Genetic variant parsers and phased-definition matching remain research software foundations. The project owner declares institutional approval for research testing; use patient-derived data only within the approval scope and with required safeguards. Individual genotype interpretation, star-allele/diplotype/phenotype assignment and guideline recommendations are not enabled by this notice.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text("IN-SILICO ENGINES · HOST ONLY", style = MaterialTheme.typography.titleSmall)
            Text(
                "Docking and OpenMM adapters remain host-side research tools. No secured compute node is deployed, no validated force-field package is selected, and no ADMET model or dataset is approved. These engines are not bundled or presented as runnable on Android.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                "RESEARCH TESTING · OWNER AUTHORIZED",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                "Institutional approval is declared by the project owner; approval reference, scope and conditions must be retained in the project record. Use only datasets covered by that approval. The VCF panel returns aggregate syntax/QC counts only and is not a clinical decision tool.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

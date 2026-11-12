package org.molecularis.app.backend
data class BackendEndpoint(val label: String, val baseUrl: String)
interface BackendHealthCheck { suspend fun check(endpoint: BackendEndpoint): Boolean }
// Backend use must be opt-in and disclose data sent off-device.

package org.assayflux.molecularis

/** Pure, deterministic identity binding for independently authenticated encrypted chunks. */
internal object ChunkIdentity {
    fun associatedData(context: String, chunkIndex: Long): ByteArray {
        require(context.isNotBlank() && chunkIndex >= 0) { "Invalid encrypted chunk identity" }
        return "$context:$chunkIndex".toByteArray(Charsets.UTF_8)
    }
}

package org.assayflux.molecularis

import java.io.File

/**
 * Owns a short-lived plaintext temporary across both materialization and use.
 * The file is deleted even when decryption/materialization or the consumer throws.
 */
internal fun <T> withPrivateTemporaryFile(
    file: File,
    materialize: (File) -> Boolean,
    action: (File) -> T,
): T? {
    return try {
        if (!materialize(file)) return null
        action(file)
    } finally {
        file.delete()
    }
}

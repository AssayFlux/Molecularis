package org.assayflux.molecularis

/** R1-only JNI/FFI smoke-test bridge; not a production scientific API. */
class NativeProbe {
    external fun rustSumSquares(x: Double, y: Double): Double
    external fun cppSumSquares(x: Double, y: Double): Double

    companion object {
        init {
            System.loadLibrary("kinetics_native")
        }
    }
}

#include <jni.h>

extern "C" double molecularis_rust_sum_squares(double x, double y);

extern "C" JNIEXPORT jdouble JNICALL
Java_org_assayflux_molecularis_NativeProbe_rustSumSquares(
    JNIEnv*, jobject, jdouble x, jdouble y) {
    return molecularis_rust_sum_squares(x, y);
}

extern "C" JNIEXPORT jdouble JNICALL
Java_org_assayflux_molecularis_NativeProbe_cppSumSquares(
    JNIEnv*, jobject, jdouble x, jdouble y) {
    return x * x + y * y;
}

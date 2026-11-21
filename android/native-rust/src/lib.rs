//! Minimal R1 Rust-to-JNI FFI experiment; not a scientific capability.

#[no_mangle]
pub extern "C" fn molecularis_rust_sum_squares(x: f64, y: f64) -> f64 {
    x * x + y * y
}

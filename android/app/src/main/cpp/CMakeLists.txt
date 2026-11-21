cmake_minimum_required(VERSION 3.22.1)
project(molecularis_native LANGUAGES C CXX)

add_library(molecularis_rust STATIC IMPORTED)
set_target_properties(molecularis_rust PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/../../../../native-rust/target/aarch64-linux-android/release/libmolecularis_rust.a"
)

add_library(molecularis_native SHARED molecularis_native.cpp)
target_compile_features(molecularis_native PRIVATE cxx_std_17)
target_link_options(molecularis_native PRIVATE "-Wl,-z,max-page-size=16384")
target_link_libraries(molecularis_native PRIVATE molecularis_rust)

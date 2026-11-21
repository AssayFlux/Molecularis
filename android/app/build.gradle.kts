plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
    id("com.chaquo.python")
}

android {
    namespace = "org.assayflux.molecularis"
    compileSdk = 36
    ndkVersion = "28.2.13676358"

    defaultConfig {
        applicationId = "org.assayflux.molecularis"
        minSdk = 29
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
        ndk {
            abiFilters += "arm64-v8a"
        }
        externalNativeBuild {
            cmake {
                cppFlags += "-std=c++17"
            }
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = "3.22.1"
        }
    }

    packaging {
        jniLibs {
            useLegacyPackaging = false
        }
    }

    testOptions {
        unitTests.isIncludeAndroidResources = true
    }
}

chaquopy {
    // Include the repository package in the embedded Python source set.
    sourceSets {
        getByName("main") {
            srcDir("../../python")
        }
    }
    defaultConfig {
        version = "3.11"
        pip {
            options("--find-links", "libs/python-wheels")
            install("biopython==1.88")
            install("numpy==1.26.2")
        }
    }
}

dependencies {
    implementation(project(":designsystem"))
    val composeBom = platform("androidx.compose:compose-bom:2025.10.01")
    implementation(composeBom)
    androidTestImplementation(composeBom)
    implementation("androidx.activity:activity-compose:1.11.0")
    implementation("androidx.biometric:biometric:1.1.0")
    implementation("androidx.fragment:fragment-ktx:1.8.9")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    debugImplementation("androidx.compose.ui:ui-tooling")
    implementation("androidx.work:work-runtime-ktx:2.10.1")
    implementation("androidx.webkit:webkit:1.12.1")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.robolectric:robolectric:4.14.1")
    testImplementation("androidx.work:work-testing:2.10.1")
}


kotlin {
    compilerOptions {
        jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
    }
}

val verifyOwnerBrandAssets by tasks.registering {
    group = "verification"
    description = "Fail release builds while owner-approved Molecularis brand assets are placeholders."
    doLast {
        val brandDir = rootProject.file("../assets/brand")
        val required = listOf(
            "app-logo.svg",
            "app-logo-foreground.svg",
            "app-logo-monochrome.svg",
            "brand-logo.svg",
            "brand-logo-light.svg",
            "brand-logo-dark.svg",
            "brand-usage.md",
        )
        val missing = required.filterNot { File(brandDir, it).isFile }
        val placeholders = required.filter { name ->
            val f = File(brandDir, name)
            f.isFile && f.readText().contains("PLACEHOLDER", ignoreCase = true)
        }
        val backgroundText = File(brandDir, "app-logo-background.txt")
        val backgroundSvg = File(brandDir, "app-logo-background.svg")
        val missingBackground = !backgroundText.isFile && !backgroundSvg.isFile
        val backgroundPlaceholder = backgroundText.isFile &&
            backgroundText.readText().contains("PLACEHOLDER", ignoreCase = true)
        if (missing.isNotEmpty() || placeholders.isNotEmpty() ||
            missingBackground || backgroundPlaceholder) {
            throw GradleException(
                "Release blocked: supply approved owner brand assets. " +
                    "Missing=$missing; placeholders=$placeholders; " +
                    "missingBackground=$missingBackground; backgroundPlaceholder=$backgroundPlaceholder"
            )
        }
    }
}

tasks.configureEach {
    if (name.contains("Release", ignoreCase = true) && name != "verifyOwnerBrandAssets") {
        dependsOn(verifyOwnerBrandAssets)
    }
}

plugins {
 id("com.android.application")
 id("org.jetbrains.kotlin.android")
 id("org.jetbrains.kotlin.plugin.compose")
 id("com.google.devtools.ksp")
}
val releaseKeystorePath = providers.environmentVariable("ANDROID_KEYSTORE_PATH").orNull
val releaseStorePassword = providers.environmentVariable("ANDROID_KEYSTORE_PASSWORD").orNull
val releaseKeyAlias = providers.environmentVariable("ANDROID_KEY_ALIAS").orNull
val releaseKeyPassword = providers.environmentVariable("ANDROID_KEY_PASSWORD").orNull
val modelCatalogUrl = providers.gradleProperty("MOLECULARIS_CATALOG_URL").orElse("").get().replace("\\", "\\\\").replace("\"", "\\\"")
val modelCatalogPublicKey = providers.gradleProperty("MOLECULARIS_CATALOG_PUBLIC_KEY").orElse("").get().replace("\\", "\\\\").replace("\"", "\\\"")

android {
 namespace="org.molecularis.app"
 compileSdk=36
 defaultConfig {
  applicationId="org.molecularis.app"
  minSdk=26
  targetSdk=35
  versionCode=7
  versionName="0.1.0"
  buildConfigField("String", "MODEL_CATALOG_URL", "\"${modelCatalogUrl}\"")
  buildConfigField("String", "MODEL_CATALOG_PUBLIC_KEY", "\"${modelCatalogPublicKey}\"")
  testInstrumentationRunner="androidx.test.runner.AndroidJUnitRunner"
 }
 signingConfigs {
  create("release") {
   if (!releaseKeystorePath.isNullOrBlank()) {
    storeFile = file(releaseKeystorePath)
    storePassword = releaseStorePassword
    keyAlias = releaseKeyAlias
    keyPassword = releaseKeyPassword
   }
  }
 }
 buildTypes {
  getByName("release") {
   isMinifyEnabled = false
   if (!releaseKeystorePath.isNullOrBlank() && !releaseStorePassword.isNullOrBlank() &&
       !releaseKeyAlias.isNullOrBlank() && !releaseKeyPassword.isNullOrBlank()) {
    signingConfig = signingConfigs.getByName("release")
   }
  }
 }
 buildFeatures { compose=true; buildConfig=true }
 compileOptions { sourceCompatibility=JavaVersion.VERSION_17; targetCompatibility=JavaVersion.VERSION_17 }
}
kotlin {
 compilerOptions {
  jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
 }
}
dependencies {
 val bom=platform("androidx.compose:compose-bom:2024.12.01")
 val roomVersion="2.8.5"
 implementation(bom)
 implementation("androidx.core:core-ktx:1.15.0")
 implementation("androidx.activity:activity-compose:1.10.0")
 implementation("androidx.compose.ui:ui")
 implementation("androidx.compose.ui:ui-tooling-preview")
 implementation("androidx.compose.material3:material3")
 implementation("androidx.compose.material:material-icons-extended")
 implementation("androidx.documentfile:documentfile:1.0.1")
 implementation("androidx.room:room-runtime:$roomVersion")
 implementation("androidx.room:room-ktx:$roomVersion")
 implementation("net.zetetic:sqlcipher-android:4.20.0")
 implementation("androidx.sqlite:sqlite:2.7.0")
 ksp("androidx.room:room-compiler:$roomVersion")
 implementation("androidx.datastore:datastore-preferences:1.1.1")
 implementation("androidx.work:work-runtime-ktx:2.10.0")
 implementation("io.coil-kt:coil-compose:2.7.0")
 implementation("androidx.media3:media3-exoplayer:1.5.1")
 implementation("com.google.ai.edge.litertlm:litertlm-android:0.18.1")
 implementation("net.i2p.crypto:eddsa:0.3.0")
 implementation("com.microsoft.onnxruntime:onnxruntime-android:1.20.0")
 implementation("com.google.mlkit:text-recognition:16.0.1")
 implementation("com.google.mlkit:image-labeling:17.0.9")
 implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.10.2")
 testImplementation("junit:junit:4.13.2")
 testImplementation("org.json:json:20250517")
 androidTestImplementation("androidx.test:runner:1.6.2")
 androidTestImplementation("androidx.test.ext:junit:1.2.1")
 androidTestImplementation("androidx.test:core:1.6.1")
}

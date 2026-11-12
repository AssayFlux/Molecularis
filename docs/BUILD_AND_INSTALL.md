# Build and install Molecularis

## Requirements

- Android Studio with Android SDK Platform 36 and Android Build Tools installed.
- JDK 17 (Android Studio's bundled JBR 17 is suitable).
- Android 8.0 (API 26) or newer for the current app minimum.
- A physical Android device is recommended for testing OCR, local model inference, text-to-speech and memory behavior.

## Build locally

From the repository root:

```bash
./gradlew --version
./gradlew :app:testDebugUnitTest
./gradlew :app:lintDebug
./gradlew :app:assembleDebug
```

The debug APK is written to:

```text
app/build/outputs/apk/debug/app-debug.apk
```

Install over USB with Android Debug Bridge:

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

On Windows, use `gradlew.bat` instead of `./gradlew`.

## Install from CI

Open the repository's [Android build workflow](https://github.com/AssayFlux/Molecularis/actions/workflows/android-build.yml), select a successful run on `main`, and download the `molecularis-debug-apk` artifact. CI artifacts are temporary and retained for 14 days.

## First launch

1. Open **Library** and import a PDF textbook that you are permitted to use.
2. Wait for on-device OCR and passage indexing to finish. The initial importer is foreground-only and currently limits each PDF to 500 pages and 5 million extracted characters.
3. Open **Teaching Studio**, enter a topic, choose MBBS, MD / DNB or PhD, and set the teaching duration.
4. Prepare the editable outline. If a compatible LiteRT-LM model is installed and loaded from **Models**, optionally request a local-AI lesson draft.
5. Review every generated scientific statement against the original textbook before teaching.
6. Preview the outline-derived slides. Use **Read this slide aloud** for manual per-slide narration when an Android TTS voice is available offline.

## Models and offline behavior

No generative language model is bundled with the APK. Import a compatible, properly licensed `.litertlm` model through **Models** and load it before requesting AI-authored lesson text. Model compatibility, memory needs and inference speed depend on the specific model and device.

Android text-to-speech is supplied by the device's speech engine. Install the desired language voice pack and verify its offline availability. A displayed voice does not guarantee that the engine will work without a network connection on every device.

The textbook OCR pipeline, local database and local-model path are designed for on-device use. Verify airplane-mode behavior on the target device before relying on it in a classroom.

## Current limitations

- PDF import and OCR run in the foreground; resumable background import is not implemented.
- Search is local keyword matching, not a complete semantic/FTS5 knowledge engine.
- AI lesson generation is an optional local-model draft and can be wrong or incomplete.
- Slide preview is derived from numbered outline sections; rich slide authoring and PDF/PPTX export are not yet implemented.
- Slide narration is manually started one slide at a time; automatic timeline synchronization and scientific diagram reveals are not yet implemented.
- Physical-device, offline, accessibility, performance and professor acceptance testing remain release gates.

See [ROADMAP.md](ROADMAP.md) for implementation status and remaining milestones.

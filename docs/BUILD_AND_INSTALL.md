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
2. Start Knowledge Pool processing. The foreground WorkManager job reports progress, supports cancellation and resumes from its last committed page after process interruption. The current limits are 5,000 pages and 25 million extracted characters.
3. Open **Teaching Studio**, enter a topic, choose MBBS, MD / DNB or PhD, and set the teaching duration.
4. Prepare the editable outline. If a compatible LiteRT-LM model is installed and loaded from **Models**, optionally request a local-AI lesson draft.
5. Review every generated scientific statement against the original textbook before teaching.
6. Preview slides and diagrams. Use synchronized lesson narration when a compatible offline Android TTS voice is installed; confirm voice availability and behavior in airplane mode on your device.

## Models and offline behavior

No generative language model is bundled with the APK. Import a compatible, properly licensed `.litertlm` model through **Models** and load it before requesting AI-authored lesson text. Model compatibility, memory needs and inference speed depend on the specific model and device.

Android text-to-speech is supplied by the device's speech engine. Install the desired language voice pack and verify its offline availability. A displayed voice does not guarantee that the engine will work without a network connection on every device.

The textbook OCR pipeline, local database and local-model path are designed for on-device use. Verify airplane-mode behavior on the target device before relying on it in a classroom.

## Current limitations

- PDF import and Knowledge Pool OCR use WorkManager foreground processing with checkpoints; direct PDF text-layer extraction and device stress tests remain open.
- Search combines local lexical retrieval with optional model-backed embedding components; semantic relevance needs professor-curated evaluation.
- AI lesson generation is an optional local-model draft and can be wrong or incomplete.
- Slides are outline-derived; advanced layouts, full-screen presenter mode and speaker notes remain open. PDF and editable PPTX export are implemented but require viewer compatibility testing.
- Narration synchronization is implemented in software; pronunciation dictionaries, pause/emphasis controls and physical-device audio timing tests remain open.
- Scheduled autonomous lectures, production authentication/backend, textbook-based scientific acceptance and production signing are not yet complete.
- Physical-device, offline, accessibility, performance and professor acceptance testing remain release gates.

See [ROADMAP.md](ROADMAP.md) for implementation status and remaining milestones.

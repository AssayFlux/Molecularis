# Molecularis device acceptance and release checklist

This document separates repository-verifiable checks from tests that require physical Android hardware, licensed teaching references or the owner's release key. Do not mark a manual test complete based only on a successful CI run.

## CI gates

- [ ] Run `./gradlew --no-daemon :app:testDebugUnitTest`.
- [ ] Run `./gradlew --no-daemon :app:lintDebug`.
- [ ] Run `./gradlew --no-daemon :app:assembleDebug`.
- [ ] Install the produced APK on at least one API 26+ physical device.
- [ ] Retain the workflow run URL and APK SHA-256 with each acceptance report.

## Device matrix

Run on at least one device from each available category; record exact manufacturer, model, Android/API version, RAM, free storage and battery state.

| Category | Android coverage | Required checks |
|---|---|---|
| Minimum supported | API 26–28 | Install/upgrade, PDF SAF import, OCR, local DB, TTS, lock |
| Modern baseline | API 29–32 | WorkManager resume, notification, foreground playback, audio focus |
| Notification permission | API 33 | Permission denied/granted, scheduled playback visibility |
| Foreground-service policy | API 34 | Media playback foreground service and stop action |
| Current target | API 35 | Background-start/Doze behavior, notification and FGS compliance |
| Low-resource device | Any supported API, low RAM | Large PDF, model unload/recovery, thermal/memory behavior |

## Scheduled teaching

- [ ] Schedule a saved lesson 2–5 minutes ahead; confirm it starts without the app open.
- [ ] Confirm offline voice selection in airplane mode.
- [ ] Confirm notification title, stop action, cancellation and final status.
- [ ] Kill the app process before start and during playback; confirm WorkManager recovery and recorded state.
- [ ] Reboot the device and verify scheduled work persistence.
- [ ] Repeat with battery saver, Doze, OEM background restrictions and low battery.
- [ ] Verify missing voice, missing notification permission and insufficient storage produce visible failures.
- [ ] Verify speech output is audible through speaker, wired headset and Bluetooth; verify interruptions and focus behavior.
- [ ] Confirm actual start-time drift and record it. WorkManager is inexact; do not promise exact alarms.

## Knowledge Pool and science

- [ ] Import one born-digital PDF and one scanned PDF (at least 100 pages each).
- [ ] Import a mixed-quality PDF with rotated, blank, image-heavy and repeated pages.
- [ ] Interrupt processing mid-book; relaunch and confirm checkpoint recovery without missing/duplicated pages.
- [ ] Stress-test a large document on low/mid/high-tier devices; record peak memory, duration, battery and thermal behavior.
- [ ] Compare OCR passages and page references against the supplied source.
- [ ] Professor-review lesson claims, citations, nomenclature, equations and audience-level adaptation for MBBS, MD, DNB and PhD.
- [ ] Validate reaction direction, stoichiometry, compartments and pathway semantics against the supplied textbook/reference before using diagrams in teaching.

## Presentation, accessibility and privacy

- [ ] Check Unicode: Greek letters, superscripts/subscripts, arrows, charge states, equations and common biochemical abbreviations.
- [ ] Check exported PDF and PPTX in at least two independent viewers.
- [ ] Check 100%, 130%, 200% font scaling, TalkBack labels/focus order, contrast and landscape orientation.
- [ ] Test app lock, biometric fallback, encrypted database migration and deletion flows.
- [ ] Confirm local crash diagnostics are off by default, contain no chat/file content, remain on device and export only after user action.
- [ ] Inspect network traffic in airplane mode and verify no local-only workflow requires a cloud account.
- [ ] Review API credentials and ensure no secret is committed to the repository.

## Release

- [ ] Configure a private Android signing keystore and passwords as GitHub Actions secrets; never commit or paste them into chat.
- [ ] Build and verify a signed release APK/AAB; record SHA-256 and version.
- [ ] Test upgrade from the previous installed release while preserving encrypted user data.
- [ ] Prepare privacy policy, store listing, data-safety declarations and support contact before Play publication.

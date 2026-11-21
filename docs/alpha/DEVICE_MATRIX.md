# Alpha Device and Platform Matrix

## Product principle
One product experience, adapted to device capabilities. Browser/PWA is the default client. Heavy computation is routed to a local node, hosted worker or institutional scheduler rather than assumed to run locally on every device.

| Device | Client | Local capability | Primary test focus |
|---|---|---|---|
| Phone | Responsive browser/PWA | Lightweight analysis, upload and result inspection; optional paired node | Touch, small viewport, memory, battery, offline transitions |
| Tablet | Responsive browser/PWA | Same client; optional local/remote compute | Split view, touch + keyboard, orientation, accessibility |
| Laptop | Browser/PWA | Optional Molecularis Node | Keyboard, file upload, local CPU/GPU pairing, suspend/resume |
| Desktop | Browser/PWA or optional desktop shell | Local node, GPU and filesystem integration | Multi-window, large datasets, GPU drivers, updates |
| Workstation | Browser/PWA + node | Native CPU/GPU and large storage | Performance, isolation, scheduling, reproducibility |
| Institutional/HPC | Browser/PWA + institution connector | Scheduler-managed jobs | Authentication, queues, data residency, audit and quota |

Define a supported browser/version policy during M1. Test current stable Chromium, Firefox and Safari/WebKit families where PWA requirements permit. Provide graceful fallback and explicit feature detection.

## Offline behavior
- Cache the application shell and selected project metadata.
- Do not silently download large datasets or model weights.
- Show pending uploads, sync conflicts, stale data and compute location.
- Queue offline jobs only where a deterministic local target exists.
- Use idempotent operations and explicit conflict resolution; never silently overwrite.

## Accessibility
Target WCAG 2.2 AA. Test keyboard navigation, semantic landmarks, contrast, reduced motion, screen-reader labels, focus management, zoom/reflow and touch targets.

## Acceptance evidence
Record hardware, OS, browser version, viewport, network state, build SHA, test cases, failures and reviewer. A responsive screenshot is not device validation.
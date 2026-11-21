# Molecularis UI specification — owner-supplied V1

**Authority:** D-024, 2026-11-17. This 20-section specification is the active visual and interaction contract for Track U.  
**Platform:** Native Android Jetpack Compose.  
**Product scope:** MOLECULARIS Research Mode only; no clinical or fabricated functionality.

## 1. Design philosophy
Minimalist, elegant, professional, monochromatic, readable and functional. Use refined typography, generous whitespace, thin line icons, subtle borders, consistent dimensions and native mobile interaction patterns. Avoid excessive gradients, shadows, rounding, decorative illustrations, colour, crowded screens and unnecessary animation.

## 2. Viewport and grid
Reference viewport: **393 × 852 dp**. Responsive targets: compact 360 × 800 dp; large 430 × 932 dp; tablets 600 dp and wider. Use responsive constraints, not fixed coordinates.

Horizontal measurements:
- Main screen padding: 20 dp standard, 16 dp compact, 24 dp large.
- Section spacing: 24 dp standard, 16 dp compact.
- Card padding: 16 dp.
- Component spacing: 8 dp small, 12 dp standard, 20 dp large.

4 dp spacing rhythm: 4, 8, 12, 16, 20, 24, 32 and 40 dp.

## 3. Typography
Use a refined, readable sans-serif with system fallback and font scaling. Large title 28 sp semibold; page title 24 sp semibold; section 20 sp semibold; subheading 16 sp medium; body 14 sp regular; secondary 13 sp regular; caption 12 sp regular; metadata 11 sp medium; button 14 sp medium. Align baselines, use comfortable line height and tabular numerals for statistics. Avoid unnecessary uppercase; allow natural wrapping.

## 4. Exact monochrome colour system
### Light
| Role | Hex |
|---|---|
| Main background | #FAF9F6 |
| Primary surface | #FFFFFF |
| Secondary surface | #F2F1ED |
| Primary text | #171717 |
| Secondary text | #686868 |
| Disabled text | #A3A3A3 |
| Border | #E5E3DE |
| Divider | #ECEAE6 |
| Icon | #292929 |

### Dark
| Role | Hex |
|---|---|
| Main background | #121212 |
| Primary surface | #1B1B1B |
| Secondary surface | #242424 |
| Primary text | #F5F5F5 |
| Secondary text | #A5A5A5 |
| Disabled text | #686868 |
| Border | #333333 |
| Divider | #292929 |
| Icon | #E8E8E8 |

Semantic colours are reserved for success (muted green), warning (muted amber), error (muted red) and information (muted blue). Pair status colour with text/icon. Appearance modes: System, Light, Dark. Contrast must be measured; do not claim WCAG conformance without evidence.

## 5. Shape and radius
Small buttons 8 dp; fields 10 dp; standard cards 12 dp; large cards 16 dp; dialogs 20 dp; bottom sheets 20 dp top corners; avatars circular. Do not round every element excessively.

## 6. Application bar
56 dp height, 16 dp horizontal padding, 24 dp leading/trailing icons and minimum 48 × 48 dp touch targets. Hamburger, page title/brand and contextual action/account avatar where appropriate.

## 7. Navigation drawer
Width-to-height proportion 3:5, maximum 85% of available width; header 150–180 dp; rows 48–52 dp; icons 22–24 dp; 16 dp horizontal padding; 4 dp vertical item spacing. Profile header, grouped destinations, clear active state, thin separators and settings/account actions near bottom. The actual destination list must reflect implemented routes.

## 8. Buttons
Primary 48 dp high, min width 112 dp, 20 dp horizontal padding, 10 dp radius. Secondary 44 dp high, 16 dp padding, 10 dp radius and subtle border. Text button 40 dp high with 12 dp padding. Icon button minimum touch target 48 × 48 dp and 24 dp icon. Implement default, pressed, disabled, loading and focused states.

## 9. Input fields
Standard 52 dp, compact 44 dp, 12 sp label, 15 sp input, 14 dp horizontal padding, 10 dp radius and 1 dp border. Include only applicable real text/password/search/dropdown/number/multiline controls with helper, validation, focus and error states.

## 10. Cards and information panels
Use cards only for meaningful grouping. Standard: 16 dp padding, 12 dp radius, 1 dp border, 12 dp internal spacing. Compact: 12 dp padding and 10 dp radius. Large panel: 20 dp padding and 16 dp radius. Prefer flat sections and lists where clearer.

## 11. Lists
Minimum row height 56 dp, 16 dp horizontal padding, 22–24 dp leading icon, 14 sp title, 12 sp subtitle and 20–24 dp trailing action. Use 1 dp separators where useful; long lists scroll naturally.

## 12. Iconography
One minimalist line-icon family; standard 24 dp, small 18 dp, large 28 dp, approximately 1.75–2 dp stroke. Maintain optical alignment and monochromatic treatment.

## 13. Dialogs and bottom sheets
Dialogs: maximum 340 dp phone width, 24 dp margin/padding, 20 dp radius, 20 sp title and 14 sp body. Bottom sheets: 20 dp top radius, 20 dp horizontal padding, 32 × 4 dp drag indicator and 16 dp content spacing. Dialogs for important confirmations; sheets for contextual actions.

## 14. Bottom navigation
Only where appropriate: 64–72 dp high excluding system insets, 24 dp icons, 11 sp labels and at most five destinations. Do not force it onto layouts better served by the adaptive rail/drawer.

## 15. Avatars and status
Avatar sizes 32, 40, 48 and 72 dp. Status dot 8 dp; standard badge 24 dp high, 8 dp horizontal padding and 6 dp radius. Status text accompanies colour where clarity matters. Do not invent an account avatar/profile.

## 16. Data and statistics
Primary statistic 24–28 sp, label 12 sp and support 11–12 sp. Charts use minimal axes, subtle grid lines, clear labels and no unnecessary gradients. Prioritise readability and explicit units/provenance.

## 17. Scrolling and safe areas
Respect status/navigation bars, keyboard insets and safe drawing areas. Prevent clipping and overlap; keep important bottom actions reachable with the keyboard open.

## 18. Interaction and animation
Button feedback 100–150 ms; small state transition 150–200 ms; screen transition 200–250 ms; bottom sheet 200–300 ms. Use restrained fade/slide and respect reduced motion; no bounce/parallax decoration.

## 19. Responsive rules
Compact: 16 dp padding, accessible actions, natural scroll and no horizontal overflow. Standard: 20 dp. Large: 24 dp and readable content width. Tablet: max content width where appropriate, two-column layouts and side navigation where beneficial.

## 20. Final quality requirements
Consistent spacing, typography, radii, icons and component heights; balanced whitespace; clear hierarchy; accessible contrast; responsive layouts; light/dark appearance; realistic interactive states; pixel-consistent alignment.

## Product and engineering constraints
- The active visual system does not change MOLECULARIS product scope or architecture.
- Home/Work/Settings must use real app state and supported operations. The separate Explore destination is removed; registered services are surfaced in the Home carousel and service list.
- No runnable capability without a real registry entry, dispatcher, input/result contract and tests.
- Local biometric app lock must not be represented as cloud account authentication.
- Preserve all owner assets byte-for-byte. Font binaries, icon libraries and other dependencies require licence/glyph/platform review.
- Owner-authorized patient-data research testing is permitted only within the institutional approval scope declared under D-025; no patient data in GitHub/CI/logs. Diagnosis, treatment/dosing recommendations and Clinical Mode remain disabled.
- Screenshot concepts are not running-app evidence. Device and accessibility status remain NOT RUN until recorded.

## Track U
The two-step execution plan and exact evidence requirements are in docs/track-u/implementation-plan.md. This document defines the desired UI, not a completion claim.


## Public scientific database card — 2026-11-18

Home includes an in-app public reference search card for NCBI Gene, NCBI Nucleotide, NCBI Protein, UniProtKB and RCSB PDB entry IDs. Search/retrieval is explicit user action. Fetched FASTA records are analysed by the existing local sequence QC workflow; fetched RCSB mmCIF records are handed to the existing offline structure parser/viewer. Raw public records are encrypted in app-private storage and can be deleted from the Home saved-record list. The source metadata and analysis result index are currently app-private SQLite without encryption at rest. The card must retain the monochrome visual system and use semantic status colours only. Search result browsing/reopen, cancellation, provider retry, accessibility/device acceptance and broader provider search remain open.

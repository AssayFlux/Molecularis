package org.assayflux.designsystem

import androidx.compose.material3.Typography
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

/**
 * Owner V1 typography: refined sans-serif throughout. System font fallback is
 * deliberate until any bundled family passes licence, Indic glyph and offline review.
 */
private val BaseTypography = Typography()

val MolecularisTypography = BaseTypography.copy(
    displayLarge = BaseTypography.displayLarge.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 28.sp,
        fontWeight = FontWeight.SemiBold, letterSpacing = 0.sp,
    ),
    displayMedium = BaseTypography.displayMedium.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 28.sp,
        fontWeight = FontWeight.SemiBold,
    ),
    displaySmall = BaseTypography.displaySmall.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 24.sp,
        fontWeight = FontWeight.SemiBold,
    ),
    headlineLarge = BaseTypography.headlineLarge.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 24.sp,
        fontWeight = FontWeight.SemiBold,
    ),
    headlineMedium = BaseTypography.headlineMedium.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 24.sp,
        fontWeight = FontWeight.SemiBold,
    ),
    headlineSmall = BaseTypography.headlineSmall.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 20.sp,
        fontWeight = FontWeight.SemiBold,
    ),
    titleLarge = BaseTypography.titleLarge.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 20.sp,
        fontWeight = FontWeight.SemiBold,
    ),
    titleMedium = BaseTypography.titleMedium.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 16.sp,
        fontWeight = FontWeight.Medium,
    ),
    titleSmall = BaseTypography.titleSmall.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 14.sp,
        fontWeight = FontWeight.Medium,
    ),
    bodyLarge = BaseTypography.bodyLarge.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 16.sp,
        fontWeight = FontWeight.Normal,
    ),
    bodyMedium = BaseTypography.bodyMedium.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 14.sp,
        fontWeight = FontWeight.Normal,
    ),
    bodySmall = BaseTypography.bodySmall.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 13.sp,
        fontWeight = FontWeight.Normal,
    ),
    labelLarge = BaseTypography.labelLarge.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 14.sp,
        fontWeight = FontWeight.Medium,
    ),
    labelMedium = BaseTypography.labelMedium.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 12.sp,
        fontWeight = FontWeight.Normal,
    ),
    labelSmall = BaseTypography.labelSmall.copy(
        fontFamily = FontFamily.SansSerif, fontSize = 11.sp,
        fontWeight = FontWeight.Medium,
    ),
)

/** Scientific identifiers and numeric summaries use tabular monospace fallback. */
val MolecularisScientificTextStyle = BaseTypography.bodyMedium.copy(
    fontFamily = FontFamily.Monospace,
    fontFeatureSettings = "tnum",
    letterSpacing = 0.sp,
)

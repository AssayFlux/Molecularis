package org.assayflux.molecularis

/**
 * Navigation is selected from the current app window, never from a device-name heuristic.
 * Breakpoints follow the Android adaptive window guidance: 600dp, 1200dp and 480dp.
 */
internal enum class NavigationMode { BottomBar, Rail, Drawer }

internal fun classifyNavigationMode(widthDp: Float, heightDp: Float): NavigationMode {
    require(widthDp >= 0f && heightDp >= 0f) { "Window dimensions cannot be negative" }
    return when {
        heightDp < 480f -> NavigationMode.Rail
        widthDp >= 1200f -> NavigationMode.Drawer
        widthDp >= 600f -> NavigationMode.Rail
        else -> NavigationMode.BottomBar
    }
}

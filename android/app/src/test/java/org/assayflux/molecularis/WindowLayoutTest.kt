package org.assayflux.molecularis

import org.junit.Assert.assertEquals
import org.junit.Test

class WindowLayoutTest {
    @Test fun compactPortraitUsesBottomBar() {
        assertEquals(NavigationMode.BottomBar, classifyNavigationMode(411f, 891f))
    }

    @Test fun compactLandscapeUsesRail() {
        assertEquals(NavigationMode.Rail, classifyNavigationMode(480f, 400f))
    }

    @Test fun mediumUsesRail() {
        assertEquals(NavigationMode.Rail, classifyNavigationMode(600f, 800f))
        assertEquals(NavigationMode.Rail, classifyNavigationMode(839f, 800f))
    }

    @Test fun expandedAndLargeUseRailUntilPermanentDrawerBreakpoint() {
        assertEquals(NavigationMode.Rail, classifyNavigationMode(840f, 900f))
        assertEquals(NavigationMode.Rail, classifyNavigationMode(1199f, 900f))
        assertEquals(NavigationMode.Drawer, classifyNavigationMode(1200f, 900f))
        assertEquals(NavigationMode.Drawer, classifyNavigationMode(1600f, 1000f))
        assertEquals(NavigationMode.Rail, classifyNavigationMode(1600f, 400f))
    }

    @Test(expected = IllegalArgumentException::class)
    fun negativeWindowSizeIsRejected() {
        classifyNavigationMode(-1f, 500f)
    }
}

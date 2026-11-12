package org.molecularis.app

import android.content.Context
import android.content.pm.PackageManager
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ApplicationSecuritySmokeTest {
    private val context: Context
        get() = ApplicationProvider.getApplicationContext()

    @Test
    fun applicationIdentityAndPrivateStorageAreStable() {
        assertEquals("org.astronaut.agi", context.packageName)
        assertTrue(context.filesDir.isDirectory)
        assertTrue(context.filesDir.canonicalPath.startsWith(context.applicationInfo.dataDir))
    }

    @Test
    fun appDoesNotEnablePlatformBackup() {
        val appInfo = context.packageManager.getApplicationInfo(context.packageName, PackageManager.GET_META_DATA)
        assertFalse(appInfo.flags and android.content.pm.ApplicationInfo.FLAG_ALLOW_BACKUP != 0)
    }

    @Test
    fun onlyDeclaredCorePermissionsArePresent() {
        val packageInfo = context.packageManager.getPackageInfo(
            context.packageName,
            PackageManager.GET_PERMISSIONS
        )
        val permissions = packageInfo.requestedPermissions.orEmpty().toSet()
        assertTrue(permissions.contains(android.Manifest.permission.INTERNET))
        assertTrue(permissions.contains(android.Manifest.permission.RECORD_AUDIO))
        assertFalse(permissions.contains(android.Manifest.permission.READ_EXTERNAL_STORAGE))
        assertFalse(permissions.contains(android.Manifest.permission.WRITE_EXTERNAL_STORAGE))
    }
}

package org.molecularis.app

import android.app.Application
import org.molecularis.app.features.CrashDiagnostics

class MolecularisApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        CrashDiagnostics.install(this)
    }
}

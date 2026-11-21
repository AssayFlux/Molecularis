pluginManagement {
    repositories {
        google()
        // Maven Central is the canonical source; avoid a flaky third-party mirror
        // that can fail dependency resolution before Gradle reaches Central.
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "Molecularis"
include(":app", ":designsystem")

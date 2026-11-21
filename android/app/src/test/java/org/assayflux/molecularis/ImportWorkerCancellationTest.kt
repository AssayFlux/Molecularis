package org.assayflux.molecularis

import androidx.work.ListenableWorker
import androidx.work.testing.TestListenableWorkerBuilder
import androidx.work.workDataOf
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35])
class ImportWorkerCancellationTest {
    private val context = RuntimeEnvironment.getApplication()

    @After
    fun cleanDatabase() {
        context.deleteDatabase("kinetics-research.db")
    }

    private fun worker(id: String) =
        TestListenableWorkerBuilder<ImportWorker>(context)
            .setInputData(
                workDataOf(
                    ImportWorker.KEY_JOB_ID to id,
                    ImportWorker.KEY_URI to "content://research-input",
                ),
            )
            .build()

    @Test
    fun lateWorkerCannotRestartCancelledQueuedImport() {
        val store = ResearchStore(context)
        store.createJob("cancel-before-start", "sample.fa", "content://research-input")
        assertTrue(store.cancelActiveImport("cancel-before-start"))
        store.close()

        val result = worker("cancel-before-start").doWork()
        assertTrue(result is ListenableWorker.Result.Failure)

        val check = ResearchStore(context)
        try {
            assertTrue(check.isJobCancelled("cancel-before-start"))
        } finally {
            check.close()
        }
    }

    @Test
    fun duplicateWorkerCannotDowngradeCompletedImport() {
        val store = ResearchStore(context)
        store.createJob("already-complete", "sample.fa", "content://research-input")
        store.updateJob("already-complete", "succeeded", hash = "f".repeat(64), bytes = 10L)
        store.close()

        val result = worker("already-complete").doWork()
        assertTrue(result is ListenableWorker.Result.Failure)

        val check = ResearchStore(context)
        try {
            assertEquals("succeeded", check.recentJobs().single().state)
        } finally {
            check.close()
        }
    }
}

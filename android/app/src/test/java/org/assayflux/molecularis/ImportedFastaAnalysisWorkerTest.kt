package org.assayflux.molecularis

import androidx.work.ListenableWorker
import androidx.work.testing.TestListenableWorkerBuilder
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35])
class ImportedFastaAnalysisWorkerTest {
    private val context = RuntimeEnvironment.getApplication()

    private fun markCommittedForGuardTest(store: ResearchStore, id: String, bytes: Long) {
        // Exercise worker preflight guards without invoking Android Keystore or decryption.
        store.writableDatabase.execSQL(
            "UPDATE jobs SET state='succeeded', sha256=?, byte_count=?, storage_path=? WHERE id=?",
            arrayOf("a".repeat(64), bytes, "/guard-test/not-materialized.kdat", id),
        )
    }

    @Test
    fun missingJobIdFailsClosed() {
        val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context).build()

        assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun malformedJobIdFailsClosedBeforeStoreAccess() {
        val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
            .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "../escape"))
            .build()

        assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun unknownJobFailsWithoutStartingScientificRuntime() {
        val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
            .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "missing-job"))
            .build()

        assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun oversizedCommittedInputIsRejectedBeforePlaintextMaterialization() {
        val store = ResearchStore(context)
        try {
            store.createJob("oversized-1", "large.fa", "content://large")
            markCommittedForGuardTest(store, "oversized-1", 1_000_001L)
            val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
                .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "oversized-1"))
                .build()

            assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
            val saved = store.recentJobs().single { it.id == "oversized-1" }
            assertTrue(saved.state == "succeeded")
            assertTrue(saved.message.orEmpty().contains("1,000,000-byte analysis limit"))
        } finally {
            store.close()
            context.deleteDatabase("kinetics-research.db")
        }
    }

    @Test
    fun fastqIsRejectedUntilPhredOffsetIsExplicit() {
        val store = ResearchStore(context)
        try {
            store.createJob("fastq-1", "reads.fastq", "content://reads")
            markCommittedForGuardTest(store, "fastq-1", 128L)
            val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
                .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "fastq-1"))
                .build()

            assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
            val saved = store.recentJobs().single { it.id == "fastq-1" }
            assertTrue(saved.message.orEmpty().contains("FASTQ requires an explicit Phred offset"))
        } finally {
            store.close()
            context.deleteDatabase("kinetics-research.db")
        }
    }
}

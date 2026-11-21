package org.assayflux.molecularis

import androidx.work.ListenableWorker
import androidx.work.testing.TestListenableWorkerBuilder
import androidx.work.workDataOf
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35])
class ImportedFastqAnalysisWorkerTest {
    private val context = RuntimeEnvironment.getApplication()

    private fun worker(id: String, offset: Int) =
        TestListenableWorkerBuilder<ImportedFastqAnalysisWorker>(context)
            .setInputData(workDataOf(
                ImportedFastqAnalysisWorker.KEY_JOB_ID to id,
                ImportedFastqAnalysisWorker.KEY_PHRED_OFFSET to offset,
            )).build()

    @Test
    fun missingJobIdFailsClosed() {
        val missingIdWorker = TestListenableWorkerBuilder<ImportedFastqAnalysisWorker>(context).build()
        assertTrue(missingIdWorker.doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun malformedJobIdFailsClosedBeforeStoreAccess() {
        assertTrue(worker("../escape", 33).doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun unsupportedPhredOffsetFailsClosedBeforeStoreAccess() {
        assertTrue(worker("valid-job", 0).doWork() is ListenableWorker.Result.Failure)
        assertTrue(worker("valid-job", 64 + 1).doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun supportedOffsetStillRequiresExistingCommittedJob() {
        assertTrue(worker("missing-job", 33).doWork() is ListenableWorker.Result.Failure)
        assertTrue(worker("missing-job", 64).doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun incompleteJobRemainsQueuedWhenAnalysisPreflightFails() {
        val store = ResearchStore(context)
        try {
            store.createJob("queued-fastq", "reads.fastq", "content://reads")
            val result = worker("queued-fastq", 33).doWork()
            assertTrue(result is ListenableWorker.Result.Failure)
            assertTrue(store.recentJobs().single { it.id == "queued-fastq" }.state == "queued")
        } finally {
            store.close()
            context.deleteDatabase("kinetics-research.db")
        }
    }

    @Test
    fun nonFastqJobIsRejectedBeforePlaintextMaterialization() {
        val store = ResearchStore(context)
        try {
            store.createJob("fasta-job", "sample.fa", "content://sample")
            store.writableDatabase.execSQL(
                "UPDATE jobs SET state='succeeded', sha256=?, byte_count=?, storage_path=? WHERE id=?",
                arrayOf("a".repeat(64), 128L, "/guard-test/not-materialized.kdat", "fasta-job"),
            )
            val result = worker("fasta-job", 33).doWork()
            assertTrue(result is ListenableWorker.Result.Failure)
            assertTrue(store.recentJobs().single { it.id == "fasta-job" }.message.orEmpty()
                .contains("FASTQ files only"))
        } finally {
            store.close()
            context.deleteDatabase("kinetics-research.db")
        }
    }

    @Test
    fun oversizedCommittedFastqIsRejectedBeforePlaintextMaterialization() {
        val store = ResearchStore(context)
        try {
            store.createJob("large-fastq", "reads.fastq", "content://reads")
            store.writableDatabase.execSQL(
                "UPDATE jobs SET state='succeeded', sha256=?, byte_count=?, storage_path=? WHERE id=?",
                arrayOf("b".repeat(64), 1_000_001L, "/guard-test/not-materialized.kdat", "large-fastq"),
            )
            val result = worker("large-fastq", 33).doWork()
            assertTrue(result is ListenableWorker.Result.Failure)
            assertTrue(store.recentJobs().single { it.id == "large-fastq" }.message.orEmpty()
                .contains("1,000,000-byte analysis limit"))
        } finally {
            store.close()
            context.deleteDatabase("kinetics-research.db")
        }
    }
}

package org.assayflux.molecularis

import android.database.sqlite.SQLiteDatabase
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35])
class ResearchStoreMigrationTest {
    private val context = RuntimeEnvironment.getApplication()

    @After
    fun cleanDatabase() {
        context.deleteDatabase("kinetics-research.db")
    }

    @Test
    fun freshInstallCreatesVersionFourSchemaAndCascadeForeignKey() {
        val store = ResearchStore(context)
        val db = store.writableDatabase

        assertEquals(4, db.version)
        assertTrue(tableExists(db, "analysis_results"))
        assertTrue(columnExists(db, "analysis_results", "input_sha256"))
        assertTrue(columnExists(db, "analysis_results", "result_json"))
        assertEquals("CASCADE", foreignKeyDeleteAction(db, "analysis_results", "jobs"))
        store.close()
    }

    @Test
    fun versionThreeDatabaseMigratesToVersionFourWithoutLosingJobs() {
        val legacy = context.openOrCreateDatabase("kinetics-research.db", 0, null)
        legacy.execSQL(
            """CREATE TABLE jobs (
                id TEXT PRIMARY KEY NOT NULL, input_name TEXT NOT NULL, input_uri TEXT NOT NULL,
                state TEXT NOT NULL, sha256 TEXT, byte_count INTEGER, message TEXT,
                storage_path TEXT, exported_at INTEGER, created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        legacy.execSQL(
            """CREATE TABLE provenance (
                job_id TEXT PRIMARY KEY NOT NULL REFERENCES jobs(id), tool_id TEXT NOT NULL,
                tool_version TEXT NOT NULL, input_sha256 TEXT NOT NULL,
                parameters_json TEXT NOT NULL, created_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        legacy.execSQL("CREATE INDEX jobs_created_at_idx ON jobs(created_at DESC)")
        legacy.execSQL("CREATE INDEX provenance_created_at_idx ON provenance(created_at DESC)")
        legacy.execSQL(
            "INSERT INTO jobs(id,input_name,input_uri,state,created_at,updated_at) VALUES('legacy-1','x.fa','content://legacy','succeeded',1,1)",
        )
        legacy.version = 3
        legacy.close()

        val store = ResearchStore(context)
        val db = store.writableDatabase

        assertEquals(4, db.version)
        assertTrue(tableExists(db, "analysis_results"))
        db.rawQuery("SELECT input_name FROM jobs WHERE id='legacy-1'", null).use { cursor ->
            assertTrue(cursor.moveToFirst())
            assertEquals("x.fa", cursor.getString(0))
        }
        store.close()
    }

    @Test
    fun versionOneDatabaseMigratesThroughAllVersionsWithoutLosingJobs() {
        assertLegacyDatabaseMigrates(version = 1)
    }

    @Test
    fun versionTwoDatabaseMigratesThroughAllVersionsWithoutLosingJobs() {
        assertLegacyDatabaseMigrates(version = 2)
    }

    private fun assertLegacyDatabaseMigrates(version: Int) {
        val legacy = context.openOrCreateDatabase("kinetics-research.db", 0, null)
        val storagePathColumn = if (version >= 2) ", storage_path TEXT" else ""
        val exportedAtColumn = if (version >= 3) ", exported_at INTEGER" else ""
        legacy.execSQL(
            """CREATE TABLE jobs (
                id TEXT PRIMARY KEY NOT NULL, input_name TEXT NOT NULL, input_uri TEXT NOT NULL,
                state TEXT NOT NULL, sha256 TEXT, byte_count INTEGER, message TEXT
                $storagePathColumn$exportedAtColumn, created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        legacy.execSQL(
            """CREATE TABLE provenance (
                job_id TEXT PRIMARY KEY NOT NULL REFERENCES jobs(id), tool_id TEXT NOT NULL,
                tool_version TEXT NOT NULL, input_sha256 TEXT NOT NULL,
                parameters_json TEXT NOT NULL, created_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        legacy.execSQL("CREATE INDEX jobs_created_at_idx ON jobs(created_at DESC)")
        if (version >= 3) {
            legacy.execSQL("CREATE INDEX provenance_created_at_idx ON provenance(created_at DESC)")
        }
        legacy.execSQL(
            "INSERT INTO jobs(id,input_name,input_uri,state,created_at,updated_at) VALUES('legacy-$version','x.fa','content://legacy','succeeded',1,1)",
        )
        legacy.version = version
        legacy.close()

        val store = ResearchStore(context)
        val db = store.writableDatabase
        assertEquals(4, db.version)
        assertTrue(tableExists(db, "analysis_results"))
        assertTrue(columnExists(db, "jobs", "storage_path"))
        assertTrue(columnExists(db, "jobs", "exported_at"))
        db.rawQuery("SELECT input_name FROM jobs WHERE id='legacy-$version'", null).use { cursor ->
            assertTrue(cursor.moveToFirst())
            assertEquals("x.fa", cursor.getString(0))
        }
        store.close()
    }

    @Test
    fun analysisResultIsDigestBoundAndExportStopsWhenJobDigestChanges() {
        val store = ResearchStore(context)
        store.createJob("job-1", "sample.fa", "content://sample")
        val digest = "a".repeat(64)
        store.updateJob("job-1", "succeeded", hash = digest, bytes = 12)
        store.saveAnalysisResult(
            id = "job-1",
            toolId = "sequence.fasta.qc",
            toolVersion = "1",
            parametersJson = """{"max_bytes":1048576}""",
            resultJson = """{"record_count":1,"records":[{"length":12}]}""",
        )

        assertNotNull(store.analysisResultJson("job-1"))
        assertNotNull(store.analysisExportJson("job-1"))

        store.updateJob("job-1", "succeeded", hash = "b".repeat(64))
        assertNull(store.analysisExportJson("job-1"))
        store.close()
    }

    @Test
    fun analysisCannotBeSavedForIncompleteOrMalformedImportDigest() {
        val store = ResearchStore(context)
        store.createJob("job-2", "sample.fa", "content://sample")
        store.updateJob("job-2", "queued", hash = "a".repeat(64))
        val notSucceeded = runCatching {
            store.saveAnalysisResult("job-2", "tool", "1", "{}", """{"ok":true}""")
        }.exceptionOrNull()
        assertNotNull(notSucceeded)

        store.updateJob("job-2", "succeeded", hash = "not-a-sha256")
        val malformed = runCatching {
            store.saveAnalysisResult("job-2", "tool", "1", "{}", """{"ok":true}""")
        }.exceptionOrNull()
        assertNotNull(malformed)
        store.close()
    }

    @Test
    fun deletingJobRemovesItsAnalysisResult() {
        val store = ResearchStore(context)
        store.createJob("job-3", "sample.fa", "content://sample")
        store.updateJob("job-3", "succeeded", hash = "c".repeat(64), bytes = 1)
        store.saveAnalysisResult("job-3", "tool", "1", "{}", """{"ok":true}""")

        assertTrue(store.deleteStoredJob("job-3"))
        assertNull(store.analysisResultJson("job-3"))
        assertFalse(store.deleteStoredJob("job-3"))
        store.close()
    }

    @Test
    fun cancellationWinsAgainstLateImportStartAndCannotDowngradeCompletedJobs() {
        val store = ResearchStore(context)
        try {
            store.createJob("cancel-race", "sample.fa", "content://sample")
            assertTrue(store.startImport("cancel-race"))
            assertTrue(store.isJobCancelled("cancel-race").not())
            assertTrue(store.cancelActiveImport("cancel-race"))
            assertTrue(store.isJobCancelled("cancel-race"))
            assertFalse(store.startImport("cancel-race"))
            assertFalse(store.cancelActiveImport("cancel-race"))

            store.createJob("completed-import", "done.fa", "content://done")
            store.updateJob("completed-import", "succeeded", hash = "d".repeat(64), bytes = 10)
            assertFalse(store.cancelActiveImport("completed-import"))
            assertFalse(store.isJobCancelled("completed-import"))
        } finally {
            store.close()
        }
    }

    @Test
    fun cancelledImportCannotBeFinalizedByLateWorker() {
        val store = ResearchStore(context)
        val encryptedDir = java.io.File(context.noBackupFilesDir, "research-inputs")
        val encryptedFile = java.io.File(encryptedDir, "cancelled-finalize.kdat")
        try {
            store.createJob("cancelled-finalize", "sample.fa", "content://sample")
            assertTrue(store.startImport("cancelled-finalize"))
            assertTrue(store.cancelActiveImport("cancelled-finalize"))
            assertTrue(encryptedDir.isDirectory || encryptedDir.mkdirs())
            encryptedFile.writeBytes(ByteArray(LocalCrypto.HEADER_BYTES.toInt() + 1))
            val finalization = runCatching {
                store.completeImport(
                    "cancelled-finalize", "e".repeat(64), 1, encryptedFile.absolutePath,
                )
            }
            assertTrue(finalization.isFailure)
            assertTrue(store.isJobCancelled("cancelled-finalize"))
        } finally {
            encryptedFile.delete()
            store.close()
        }
    }

    @Test
    fun runningImportCanBeReclaimedAfterProcessRestart() {
        val store = ResearchStore(context)
        try {
            store.createJob("process-restart", "sample.fa", "content://sample")
            assertTrue(store.startImport("process-restart"))
            // WorkManager may recreate a Worker after process death while its durable
            // job row still says running; claiming it again is the resume path.
            assertTrue(store.startImport("process-restart"))
            assertFalse(store.cancelActiveImport("missing-job"))
        } finally {
            store.close()
        }
    }

    @Test
    fun resumeTransitionsOnlyFailedOrCancelledJobsBackToQueued() {
        val store = ResearchStore(context)
        try {
            store.createJob("resume-job", "sample.fa", "content://sample")
            assertFalse(store.queueImportForResume("resume-job"))
            store.updateJob("resume-job", "cancelled")
            assertTrue(store.queueImportForResume("resume-job"))
            assertFalse(store.queueImportForResume("resume-job"))
            assertTrue(store.startImport("resume-job"))
        } finally {
            store.close()
        }
    }

    private fun tableExists(db: SQLiteDatabase, name: String): Boolean =
        db.rawQuery(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
            arrayOf(name),
        ).use { it.moveToFirst() }

    private fun columnExists(db: SQLiteDatabase, table: String, column: String): Boolean =
        db.rawQuery("PRAGMA table_info($table)", null).use { cursor ->
            val nameIndex = cursor.getColumnIndexOrThrow("name")
            generateSequence { if (cursor.moveToNext()) cursor.getString(nameIndex) else null }
                .any { it == column }
        }

    private fun foreignKeyDeleteAction(db: SQLiteDatabase, table: String, parent: String): String? =
        db.rawQuery("PRAGMA foreign_key_list($table)", null).use { cursor ->
            val tableIndex = cursor.getColumnIndexOrThrow("table")
            val actionIndex = cursor.getColumnIndexOrThrow("on_delete")
            while (cursor.moveToNext()) {
                if (cursor.getString(tableIndex) == parent) return@use cursor.getString(actionIndex)
            }
            null
        }
}

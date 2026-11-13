package org.molecularis.app.data

import android.content.ContentValues
import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase as FrameworkSQLiteDatabase
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase
import net.zetetic.database.sqlcipher.SupportOpenHelperFactory

/**
 * Explicit schema migrations preserve all local records. The first encrypted open also
 * copies the legacy plaintext DB into a temporary SQLCipher DB and verifies row counts
 * before atomically promoting it. The plaintext file is deleted only after the encrypted
 * database has successfully opened and the migration marker has been committed.
 */
private val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            "CREATE TABLE IF NOT EXISTS local_models (" +
                "uri TEXT NOT NULL, displayName TEXT NOT NULL, mimeType TEXT, " +
                "sizeBytes INTEGER NOT NULL, importedAt INTEGER NOT NULL, " +
                "runtimeStatus TEXT NOT NULL, PRIMARY KEY(uri))"
        )
        db.execSQL(
            "CREATE TABLE IF NOT EXISTS workspace_projects (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, " +
                "description TEXT NOT NULL, createdAt INTEGER NOT NULL, updatedAt INTEGER NOT NULL)"
        )
        db.execSQL(
            "CREATE INDEX IF NOT EXISTS index_messages_conversationId ON messages(conversationId)"
        )
    }
}

private val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE local_models ADD COLUMN modelPath TEXT")
    }
}

private val MIGRATION_3_4 = object : Migration(3, 4) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE messages ADD COLUMN attachmentText TEXT")
    }
}

private val MIGRATION_4_5 = object : Migration(4, 5) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE conversations ADD COLUMN workspaceProjectId INTEGER")
    }
}

private val MIGRATION_5_6 = object : Migration(5, 6) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_chunks (id TEXT NOT NULL, source TEXT NOT NULL, chunkIndex INTEGER NOT NULL, pageNumber INTEGER, text TEXT NOT NULL, embeddingModelId TEXT NOT NULL, scopeId TEXT NOT NULL, embedding BLOB NOT NULL, createdAt INTEGER NOT NULL, PRIMARY KEY(id))")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_chunks_source ON knowledge_chunks(source)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_chunks_embeddingModelId ON knowledge_chunks(embeddingModelId)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_chunks_scopeId ON knowledge_chunks(scopeId)")
    }
}


private val MIGRATION_6_7 = object : Migration(6, 7) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE IF NOT EXISTS books (id TEXT NOT NULL, title TEXT NOT NULL, originalFileName TEXT NOT NULL, localPath TEXT NOT NULL, sourceUri TEXT NOT NULL, pageCount INTEGER NOT NULL, extractedChars INTEGER NOT NULL, importedAt INTEGER NOT NULL, PRIMARY KEY(id))")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_books_importedAt ON books(importedAt)")
        db.execSQL("CREATE TABLE IF NOT EXISTS book_passages (id TEXT NOT NULL, bookId TEXT NOT NULL, chunkIndex INTEGER NOT NULL, pageNumber INTEGER NOT NULL, text TEXT NOT NULL, PRIMARY KEY(id), FOREIGN KEY(bookId) REFERENCES books(id) ON UPDATE NO ACTION ON DELETE CASCADE)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_book_passages_bookId ON book_passages(bookId)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_book_passages_pageNumber ON book_passages(pageNumber)")
    }
}

private val MIGRATION_7_8 = object : Migration(7, 8) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE IF NOT EXISTS saved_lessons (id TEXT NOT NULL, title TEXT NOT NULL, audienceLevel TEXT NOT NULL, durationMinutes INTEGER NOT NULL, outline TEXT NOT NULL, createdAt INTEGER NOT NULL, updatedAt INTEGER NOT NULL, PRIMARY KEY(id))")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_saved_lessons_updatedAt ON saved_lessons(updatedAt)")
    }
}


private val MIGRATION_9_10 = object : Migration(9, 10) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE VIRTUAL TABLE IF NOT EXISTS book_passages_fts USING fts4(text, content='book_passages')")
        db.execSQL("INSERT INTO book_passages_fts(book_passages_fts) VALUES('rebuild')")
        db.execSQL("CREATE TRIGGER IF NOT EXISTS book_passages_fts_insert AFTER INSERT ON book_passages BEGIN INSERT INTO book_passages_fts(docid,text) VALUES(new.rowid,new.text); END")
        db.execSQL("CREATE TRIGGER IF NOT EXISTS book_passages_fts_delete AFTER DELETE ON book_passages BEGIN INSERT INTO book_passages_fts(book_passages_fts,docid,text) VALUES('delete',old.rowid,old.text); END")
        db.execSQL("CREATE TRIGGER IF NOT EXISTS book_passages_fts_update AFTER UPDATE OF text ON book_passages BEGIN INSERT INTO book_passages_fts(book_passages_fts,docid,text) VALUES('delete',old.rowid,old.text); INSERT INTO book_passages_fts(docid,text) VALUES(new.rowid,new.text); END")
    }
}

private val MIGRATION_8_9 = object : Migration(8, 9) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_books (id TEXT NOT NULL, bookId TEXT NOT NULL, detectedTitle TEXT NOT NULL, author TEXT NOT NULL, publisher TEXT NOT NULL, edition TEXT NOT NULL, subject TEXT NOT NULL, summary TEXT NOT NULL, chapterOutline TEXT NOT NULL, extractedPageCount INTEGER NOT NULL, extractedChars INTEGER NOT NULL, passageCount INTEGER NOT NULL, topicCount INTEGER NOT NULL, qualityScore INTEGER NOT NULL, reviewState TEXT NOT NULL, processedAt INTEGER NOT NULL, PRIMARY KEY(id))")
        db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS index_knowledge_books_bookId ON knowledge_books(bookId)")
        db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_topics (id TEXT NOT NULL, knowledgeBookId TEXT NOT NULL, name TEXT NOT NULL, startPage INTEGER NOT NULL, confidence REAL NOT NULL, evidence TEXT NOT NULL, approved INTEGER NOT NULL, PRIMARY KEY(id))")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_topics_knowledgeBookId ON knowledge_topics(knowledgeBookId)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_topics_name ON knowledge_topics(name)")
    }
}

private val MIGRATION_10_11 = object : Migration(10, 11) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_processing_checkpoints (bookId TEXT NOT NULL, stagingBookId TEXT NOT NULL, nextPage INTEGER NOT NULL, extractedChars INTEGER NOT NULL, passageCount INTEGER NOT NULL, updatedAt INTEGER NOT NULL, PRIMARY KEY(bookId))")
    }
}

private val MIGRATION_11_12 = object : Migration(11, 12) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE knowledge_topics ADD COLUMN parentTopicId TEXT")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_topics_parentTopicId ON knowledge_topics(parentTopicId)")
        db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_topic_aliases (id TEXT NOT NULL, topicId TEXT NOT NULL, alias TEXT NOT NULL, normalizedAlias TEXT NOT NULL, PRIMARY KEY(id), FOREIGN KEY(topicId) REFERENCES knowledge_topics(id) ON UPDATE NO ACTION ON DELETE CASCADE)")
        db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS index_knowledge_topic_aliases_topicId_normalizedAlias ON knowledge_topic_aliases(topicId, normalizedAlias)")
    }
}

private val MIGRATION_12_13 = object : Migration(12, 13) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE books ADD COLUMN fileSha256 TEXT")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_books_fileSha256 ON books(fileSha256)")
    }
}

private val FTS_CALLBACK = object : RoomDatabase.Callback() {
    override fun onCreate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TRIGGER IF NOT EXISTS book_passages_fts_insert AFTER INSERT ON book_passages BEGIN INSERT INTO book_passages_fts(docid,text) VALUES(new.rowid,new.text); END")
        db.execSQL("CREATE TRIGGER IF NOT EXISTS book_passages_fts_delete AFTER DELETE ON book_passages BEGIN INSERT INTO book_passages_fts(book_passages_fts,docid,text) VALUES('delete',old.rowid,old.text); END")
        db.execSQL("CREATE TRIGGER IF NOT EXISTS book_passages_fts_update AFTER UPDATE OF text ON book_passages BEGIN INSERT INTO book_passages_fts(book_passages_fts,docid,text) VALUES('delete',old.rowid,old.text); INSERT INTO book_passages_fts(docid,text) VALUES(new.rowid,new.text); END")
        db.execSQL("INSERT INTO book_passages_fts(book_passages_fts) VALUES('rebuild')")
    }
}
private val MIGRATION_14_15 = object : Migration(14, 15) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_topic_passage_links (topicId TEXT NOT NULL, passageId TEXT NOT NULL, pageNumber INTEGER NOT NULL, linkType TEXT NOT NULL, PRIMARY KEY(topicId,passageId), FOREIGN KEY(topicId) REFERENCES knowledge_topics(id) ON UPDATE NO ACTION ON DELETE CASCADE, FOREIGN KEY(passageId) REFERENCES book_passages(id) ON UPDATE NO ACTION ON DELETE CASCADE)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_topic_passage_links_topicId ON knowledge_topic_passage_links(topicId)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_topic_passage_links_passageId ON knowledge_topic_passage_links(passageId)")
    }
}

private val MIGRATION_13_14 = object : Migration(13, 14) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE knowledge_books ADD COLUMN pagesWithText INTEGER NOT NULL DEFAULT 0")
        db.execSQL("ALTER TABLE knowledge_books ADD COLUMN emptyPages INTEGER NOT NULL DEFAULT 0")
        db.execSQL("ALTER TABLE knowledge_books ADD COLUMN shortTextPages INTEGER NOT NULL DEFAULT 0")
        db.execSQL("ALTER TABLE knowledge_books ADD COLUMN duplicatePages INTEGER NOT NULL DEFAULT 0")
        db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_page_audits (stagingBookId TEXT NOT NULL, pageNumber INTEGER NOT NULL, charCount INTEGER NOT NULL, fingerprint TEXT NOT NULL, qualityFlag TEXT NOT NULL, PRIMARY KEY(stagingBookId,pageNumber))")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_page_audits_stagingBookId ON knowledge_page_audits(stagingBookId)")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_knowledge_page_audits_fingerprint ON knowledge_page_audits(fingerprint)")
    }
}
object DatabaseProvider {
    private const val LEGACY_NAME = "molecularis-local.db"
    private const val ENCRYPTED_NAME = "molecularis-secure.db"
    private const val TEMP_NAME = "molecularis-secure-migrating.db"
    private const val STATE_PREFS = "molecularis_secure_database"
    private const val MIGRATION_COMPLETE = "encrypted_migration_complete"

    @Volatile private var instance: AppDatabase? = null

    fun get(context: Context): AppDatabase = instance ?: synchronized(this) {
        instance ?: openEncrypted(context.applicationContext).also { instance = it }
    }

    private fun openEncrypted(context: Context): AppDatabase {
        // SQLCipher's native core must be loaded before constructing its Room factory.
        System.loadLibrary("sqlcipher")

        val legacyFile = context.getDatabasePath(LEGACY_NAME)
        val encryptedFile = context.getDatabasePath(ENCRYPTED_NAME)
        val prefs = context.getSharedPreferences(STATE_PREFS, Context.MODE_PRIVATE)
        val migrationDone = prefs.getBoolean(MIGRATION_COMPLETE, false)

        // If the process died before committing the marker, the old DB is still canonical.
        // Discard only the incomplete encrypted copy and repeat the verified copy.
        if (encryptedFile.exists() && legacyFile.exists() && !migrationDone) {
            check(context.deleteDatabase(ENCRYPTED_NAME)) {
                "Could not remove an incomplete encrypted database copy."
            }
        }

        val canCreateKey = !encryptedFile.exists() || (legacyFile.exists() && !migrationDone)
        val passphrase = DatabaseKeyManager.getPassphrase(context, canCreateKey)

        if (!encryptedFile.exists() && legacyFile.exists()) {
            migrateLegacyDatabase(context, passphrase)
        }

        val database = Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            ENCRYPTED_NAME
        )
            .openHelperFactory(SupportOpenHelperFactory(passphrase.copyOf()))
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4, MIGRATION_4_5, MIGRATION_5_6, MIGRATION_6_7, MIGRATION_7_8, MIGRATION_8_9, MIGRATION_9_10, MIGRATION_10_11, MIGRATION_11_12, MIGRATION_12_13, MIGRATION_13_14, MIGRATION_14_15)
            .addCallback(FTS_CALLBACK)
            .setJournalMode(RoomDatabase.JournalMode.TRUNCATE)
            .build()

        // Force key validation now, before discarding the recoverable plaintext source.
        database.openHelper.writableDatabase
        check(prefs.edit().putBoolean(MIGRATION_COMPLETE, true).commit()) {
            "Could not commit encrypted database migration state."
        }
        if (legacyFile.exists()) {
            check(context.deleteDatabase(LEGACY_NAME)) {
                "Encrypted database opened, but the old plaintext database could not be deleted."
            }
        }
        return database
    }

    private fun migrateLegacyDatabase(context: Context, passphrase: ByteArray) {
        context.deleteDatabase(TEMP_NAME)
        val legacy = Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            LEGACY_NAME
        )
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4, MIGRATION_4_5, MIGRATION_5_6, MIGRATION_6_7, MIGRATION_7_8, MIGRATION_8_9, MIGRATION_9_10, MIGRATION_10_11, MIGRATION_11_12, MIGRATION_12_13, MIGRATION_13_14)
            .addCallback(FTS_CALLBACK)
            .setJournalMode(RoomDatabase.JournalMode.TRUNCATE)
            .build()

        val encryptedTemp = Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            TEMP_NAME
        )
            .openHelperFactory(SupportOpenHelperFactory(passphrase.copyOf()))
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4, MIGRATION_4_5, MIGRATION_5_6, MIGRATION_6_7, MIGRATION_7_8, MIGRATION_8_9, MIGRATION_9_10, MIGRATION_10_11, MIGRATION_11_12, MIGRATION_12_13, MIGRATION_13_14)
            .addCallback(FTS_CALLBACK)
            .setJournalMode(RoomDatabase.JournalMode.TRUNCATE)
            .build()

        try {
            val source = legacy.openHelper.writableDatabase
            val target = encryptedTemp.openHelper.writableDatabase
            val tables = listOf("conversations", "messages", "local_models", "workspace_projects", "knowledge_chunks", "books", "book_passages", "knowledge_books", "knowledge_topics", "saved_lessons", "knowledge_processing_checkpoints", "knowledge_topic_aliases", "knowledge_page_audits", "knowledge_topic_passage_links")
            target.beginTransaction()
            try {
                tables.forEach { table -> copyTable(source, target, table) }
                target.setTransactionSuccessful()
            } finally {
                target.endTransaction()
            }
            tables.forEach { table ->
                val sourceCount = countRows(source, table)
                val targetCount = countRows(target, table)
                check(sourceCount == targetCount) {
                    "Encrypted migration verification failed for $table ($sourceCount != $targetCount)."
                }
            }
        } catch (error: Throwable) {
            encryptedTemp.close()
            legacy.close()
            context.deleteDatabase(TEMP_NAME)
            throw error
        }

        encryptedTemp.close()
        legacy.close()
        val tempFile = context.getDatabasePath(TEMP_NAME)
        val encryptedFile = context.getDatabasePath(ENCRYPTED_NAME)
        check(tempFile.isFile && tempFile.renameTo(encryptedFile)) {
            context.deleteDatabase(TEMP_NAME)
            "Could not promote the verified encrypted database file."
        }
    }

    private fun copyTable(source: SupportSQLiteDatabase, target: SupportSQLiteDatabase, table: String) {
        source.query("SELECT * FROM $table").use { cursor ->
            while (cursor.moveToNext()) {
                val values = ContentValues(cursor.columnCount)
                for (index in 0 until cursor.columnCount) {
                    val column = cursor.getColumnName(index)
                    when (cursor.getType(index)) {
                        Cursor.FIELD_TYPE_NULL -> values.putNull(column)
                        Cursor.FIELD_TYPE_INTEGER -> values.put(column, cursor.getLong(index))
                        Cursor.FIELD_TYPE_FLOAT -> values.put(column, cursor.getDouble(index))
                        Cursor.FIELD_TYPE_STRING -> values.put(column, cursor.getString(index))
                        Cursor.FIELD_TYPE_BLOB -> values.put(column, cursor.getBlob(index))
                    }
                }
                target.insert(table, FrameworkSQLiteDatabase.CONFLICT_REPLACE, values)
            }
        }
    }

    private fun countRows(database: SupportSQLiteDatabase, table: String): Long =
        database.query("SELECT COUNT(*) FROM $table").use { cursor ->
            if (cursor.moveToFirst()) cursor.getLong(0) else 0L
        }
}

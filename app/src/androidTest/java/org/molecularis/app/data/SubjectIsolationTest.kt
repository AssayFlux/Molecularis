package org.molecularis.app.data

import android.content.Context
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class SubjectIsolationTest {
    private lateinit var database: AppDatabase

    @Before
    fun createDatabase() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
            .allowMainThreadQueries()
            .build()
    }

    @After
    fun closeDatabase() {
        database.close()
    }

    @Test
    fun libraryKnowledgeChatLessonsAndSchedulesStayInsideActiveSubject() = runBlocking {
        val now = System.currentTimeMillis()
        database.subjectWorkspaceDao().add(
            SubjectWorkspaceEntity(id = "math", name = "Mathematics", createdAt = now, updatedAt = now)
        )
        database.subjectWorkspaceDao().add(
            SubjectWorkspaceEntity(id = "history", name = "History", createdAt = now, updatedAt = now)
        )
        database.professorProfileDao().add(
            ProfessorProfileEntity(id = "math-prof", subjectId = "math", name = "Mathematics tutor")
        )
        database.professorProfileDao().add(
            ProfessorProfileEntity(id = "history-prof", subjectId = "history", name = "History tutor")
        )

        val mathBook = BookEntity(
            id = "math-book", title = "Algebra", originalFileName = "algebra.pdf",
            localPath = "/tmp/algebra.pdf", sourceUri = "content://math",
            pageCount = 1, extractedChars = 100, subjectId = "math"
        )
        val historyBook = BookEntity(
            id = "history-book", title = "Archive", originalFileName = "archive.pdf",
            localPath = "/tmp/archive.pdf", sourceUri = "content://history",
            pageCount = 1, extractedChars = 100, subjectId = "history"
        )
        database.bookDao().addBook(mathBook)
        database.bookDao().addBook(historyBook)
        database.bookDao().addPassages(
            listOf(
                BookPassageEntity("math-passage", "math-book", 0, 1, "sharedterm appears in mathematics"),
                BookPassageEntity("history-passage", "history-book", 0, 1, "sharedterm appears in history")
            )
        )

        database.openHelper.writableDatabase.execSQL(
            "INSERT INTO book_passages_fts(book_passages_fts) VALUES('rebuild')"
        )

        database.knowledgePoolDao().saveBook(
            KnowledgeBookEntity(
                id = "math-kb", bookId = "math-book", detectedTitle = "Algebra", author = "",
                publisher = "", edition = "", subject = "Mathematics", summary = "",
                chapterOutline = "", extractedPageCount = 1, extractedChars = 100,
                passageCount = 1, topicCount = 0, qualityScore = 90, reviewState = "approved"
            )
        )
        database.knowledgePoolDao().saveBook(
            KnowledgeBookEntity(
                id = "history-kb", bookId = "history-book", detectedTitle = "Archive", author = "",
                publisher = "", edition = "", subject = "History", summary = "",
                chapterOutline = "", extractedPageCount = 1, extractedChars = 100,
                passageCount = 1, topicCount = 0, qualityScore = 90, reviewState = "approved"
            )
        )

        database.chatDao().addConversation(
            ConversationEntity(title = "Math chat", subjectId = "math", professorProfileId = "math-prof")
        )
        database.chatDao().addConversation(
            ConversationEntity(title = "History chat", subjectId = "history", professorProfileId = "history-prof")
        )
        database.lessonDao().saveLesson(
            SavedLessonEntity(
                id = "math-lesson", title = "Algebra", audienceLevel = "General",
                durationMinutes = 30, outline = "Math outline", subjectId = "math",
                professorProfileId = "math-prof"
            )
        )
        database.lessonDao().saveLesson(
            SavedLessonEntity(
                id = "history-lesson", title = "Archive", audienceLevel = "General",
                durationMinutes = 30, outline = "History outline", subjectId = "history",
                professorProfileId = "history-prof"
            )
        )
        database.scheduledLectureDao().save(
            ScheduledLectureEntity(
                id = "math-schedule", lessonId = "math-lesson", title = "Algebra",
                audienceLevel = "General", durationMinutes = 30, languageTag = "en",
                scheduledAt = now + 60_000, subjectId = "math"
            )
        )
        database.scheduledLectureDao().save(
            ScheduledLectureEntity(
                id = "history-schedule", lessonId = "history-lesson", title = "Archive",
                audienceLevel = "General", durationMinutes = 30, languageTag = "en",
                scheduledAt = now + 60_000, subjectId = "history"
            )
        )

        assertEquals(listOf("math-book"), database.bookDao().booksForSubject("math").first().map { it.id })
        assertEquals(listOf("math-passage"), database.bookDao().searchAllForSubject("math", "sharedterm").map { it.id })
        assertEquals(listOf("math-passage"), database.bookDao().searchFilteredIndexedForSubject("sharedterm", "math", null, null, null).map { it.id })
        assertEquals(listOf("math-prof"), database.professorProfileDao().profiles("math").first().map { it.id })
        assertEquals(listOf("math-kb"), database.knowledgePoolDao().booksForSubject("math").first().map { it.id })
        assertEquals(listOf("Math chat"), database.chatDao().conversationsForSubject("math").first().map { it.title })
        assertEquals(listOf("math-lesson"), database.lessonDao().lessonsForSubject("math").first().map { it.id })
        assertEquals(listOf("math-schedule"), database.scheduledLectureDao().lecturesForSubject("math").first().map { it.id })
        assertTrue(database.bookDao().searchAllForSubject("math", "history").isEmpty())
    }
}

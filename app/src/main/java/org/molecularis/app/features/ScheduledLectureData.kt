package org.molecularis.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Index
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "scheduled_lectures", indices = [Index("scheduledAt"), Index("status")])
data class ScheduledLectureEntity(
    @PrimaryKey val id: String,
    val lessonId: String,
    val title: String,
    val audienceLevel: String,
    val durationMinutes: Int,
    val languageTag: String,
    val scheduledAt: Long,
    val status: String = "scheduled",
    val workId: String? = null,
    val lastError: String? = null,
    val updatedAt: Long = System.currentTimeMillis()
)

@Dao
interface ScheduledLectureDao {
    @Query("SELECT * FROM scheduled_lectures ORDER BY scheduledAt DESC")
    fun lectures(): Flow<List<ScheduledLectureEntity>>

    @Query("SELECT * FROM scheduled_lectures WHERE id=:id LIMIT 1")
    suspend fun lecture(id: String): ScheduledLectureEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun save(lecture: ScheduledLectureEntity)

    @Query("UPDATE scheduled_lectures SET status=:status, lastError=:error, updatedAt=:updatedAt WHERE id=:id")
    suspend fun updateStatus(id: String, status: String, error: String?, updatedAt: Long = System.currentTimeMillis())

    @Query("DELETE FROM scheduled_lectures WHERE id=:id")
    suspend fun delete(id: String)
}

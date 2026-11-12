package org.molecularis.app.data
import androidx.room.*
import kotlinx.coroutines.flow.Flow
@Entity(tableName="conversations")
data class ConversationEntity(@PrimaryKey(autoGenerate=true) val id:Long=0,val title:String,val createdAt:Long=System.currentTimeMillis(),val archived:Boolean=false,val pinned:Boolean=false,val workspaceProjectId:Long?=null)
@Entity(tableName="messages",indices=[Index("conversationId")])
data class MessageEntity(@PrimaryKey(autoGenerate=true) val id:Long=0,val conversationId:Long,val body:String,val role:String,val createdAt:Long=System.currentTimeMillis(),val status:String="complete",val attachmentUri:String?=null,val attachmentName:String?=null,val attachmentText:String?=null)
@Entity(tableName="local_models")
data class LocalModelEntity(@PrimaryKey val uri:String,val displayName:String,val mimeType:String?,val sizeBytes:Long,val importedAt:Long=System.currentTimeMillis(),val runtimeStatus:String="not_connected",val modelPath:String?=null)
@Entity(tableName="workspace_projects")
data class WorkspaceProjectEntity(@PrimaryKey(autoGenerate=true) val id:Long=0,val name:String,val description:String="",val createdAt:Long=System.currentTimeMillis(),val updatedAt:Long=System.currentTimeMillis())

/** Encrypted Room row containing one source-labelled chunk and its local embedding vector. */
@Entity(tableName="knowledge_chunks",indices=[Index("source"),Index("embeddingModelId"),Index("scopeId")])
data class KnowledgeChunkEntity(
 @PrimaryKey val id:String,
 val source:String,
 val chunkIndex:Int,
 val pageNumber:Int?,
 val text:String,
 val embeddingModelId:String,
 val scopeId:String,
 val embedding:ByteArray,
 val createdAt:Long=System.currentTimeMillis()
)

@Dao interface ChatDao {
 @Query("SELECT * FROM conversations WHERE archived=0 ORDER BY pinned DESC,createdAt DESC") fun conversations():Flow<List<ConversationEntity>>
 @Query("SELECT * FROM messages WHERE conversationId=:id ORDER BY createdAt,id") fun messages(id:Long):Flow<List<MessageEntity>>
 @Insert suspend fun addConversation(item:ConversationEntity):Long
 @Insert suspend fun addMessage(item:MessageEntity):Long
 @Query("UPDATE messages SET attachmentText=:text WHERE id=:id") suspend fun updateAttachmentText(id:Long,text:String)
 @Query("SELECT * FROM messages WHERE conversationId=:id AND attachmentText IS NOT NULL ORDER BY createdAt DESC LIMIT 5") suspend fun attachmentMessages(id:Long):List<MessageEntity>
 @Query("SELECT * FROM conversations WHERE id=:id LIMIT 1") suspend fun conversation(id:Long):ConversationEntity?
 @Query("SELECT * FROM conversations WHERE workspaceProjectId=:projectId AND archived=0 ORDER BY createdAt DESC LIMIT 1") suspend fun latestProjectConversation(projectId:Long):ConversationEntity?
 @Query("UPDATE conversations SET title=:title WHERE id=:id") suspend fun rename(id:Long,title:String)
 @Query("DELETE FROM messages WHERE conversationId=:id") suspend fun deleteMessages(id:Long)
 @Query("DELETE FROM conversations WHERE id=:id") suspend fun deleteConversation(id:Long)
}
@Dao interface KnowledgeDao {
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun upsert(chunks:List<KnowledgeChunkEntity>)
 @Query("SELECT * FROM knowledge_chunks WHERE embeddingModelId=:modelId AND scopeId=:scopeId ORDER BY source,chunkIndex") suspend fun chunksForModel(modelId:String,scopeId:String):List<KnowledgeChunkEntity>
 @Query("DELETE FROM knowledge_chunks WHERE source=:source AND embeddingModelId=:modelId AND scopeId=:scopeId") suspend fun deleteSource(source:String,modelId:String,scopeId:String)
 @Query("DELETE FROM knowledge_chunks WHERE embeddingModelId=:modelId AND scopeId=:scopeId") suspend fun clearModel(modelId:String,scopeId:String)
 @Query("SELECT COUNT(*) FROM knowledge_chunks WHERE embeddingModelId=:modelId AND scopeId=:scopeId") suspend fun countForModel(modelId:String,scopeId:String):Int
}
@Dao interface ModelDao {
 @Query("SELECT * FROM local_models ORDER BY importedAt DESC") fun models():Flow<List<LocalModelEntity>>
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun add(item:LocalModelEntity)
 @Query("DELETE FROM local_models WHERE uri=:uri") suspend fun remove(uri:String)
}
@Dao interface WorkspaceDao {
 @Query("SELECT * FROM workspace_projects ORDER BY updatedAt DESC") fun projects():Flow<List<WorkspaceProjectEntity>>
 @Insert suspend fun add(project:WorkspaceProjectEntity):Long
 @Query("DELETE FROM workspace_projects WHERE id=:id") suspend fun delete(id:Long)
}

@Entity(tableName="books",indices=[Index("importedAt")])
data class BookEntity(
 @PrimaryKey val id:String,
 val title:String,
 val originalFileName:String,
 val localPath:String,
 val sourceUri:String,
 val pageCount:Int,
 val extractedChars:Int,
 val importedAt:Long=System.currentTimeMillis()
)
@Entity(tableName="book_passages",indices=[Index("bookId"),Index("pageNumber")],foreignKeys=[ForeignKey(entity=BookEntity::class,parentColumns=["id"],childColumns=["bookId"],onDelete=ForeignKey.CASCADE)])
data class BookPassageEntity(
 @PrimaryKey val id:String,
 val bookId:String,
 val chunkIndex:Int,
 val pageNumber:Int,
 val text:String
)
@Dao interface BookDao {
 @Query("SELECT * FROM books ORDER BY importedAt DESC") fun books():Flow<List<BookEntity>>
 @Insert suspend fun addBook(book:BookEntity)
 @Insert suspend fun addPassages(passages:List<BookPassageEntity>)
 @Query("SELECT * FROM book_passages WHERE bookId=:bookId ORDER BY pageNumber,chunkIndex") suspend fun passages(bookId:String):List<BookPassageEntity>
 @Query("SELECT * FROM book_passages WHERE bookId=:bookId AND text LIKE '%' || :query || '%' ORDER BY pageNumber LIMIT 100") suspend fun searchInBook(bookId:String,query:String):List<BookPassageEntity>
 @Query("SELECT * FROM book_passages WHERE text LIKE '%' || :query || '%' ORDER BY bookId,pageNumber LIMIT 100") suspend fun searchAll(query:String):List<BookPassageEntity>
 @Query("UPDATE books SET pageCount=:pageCount, extractedChars=:extractedChars WHERE id=:bookId") suspend fun updateBookStats(bookId:String,pageCount:Int,extractedChars:Int)
 @Query("DELETE FROM books WHERE id=:bookId") suspend fun deleteBook(bookId:String)
}

@Entity(tableName="knowledge_books",indices=[Index("bookId",unique=true)])
data class KnowledgeBookEntity(
 @PrimaryKey val id:String,val bookId:String,val detectedTitle:String,val author:String,
 val publisher:String,val edition:String,val subject:String,val summary:String,
 val chapterOutline:String,val extractedPageCount:Int,val extractedChars:Int,
 val passageCount:Int,val topicCount:Int,val qualityScore:Int,
 val reviewState:String="needs_review",val processedAt:Long=System.currentTimeMillis()
)
@Entity(tableName="knowledge_topics",indices=[Index("knowledgeBookId"),Index("name")])
data class KnowledgeTopicEntity(
 @PrimaryKey val id:String,val knowledgeBookId:String,val name:String,
 val startPage:Int,val confidence:Float,val evidence:String,val approved:Boolean=false
)
@Dao interface KnowledgePoolDao {
 @Query("SELECT * FROM knowledge_books ORDER BY processedAt DESC") fun books():Flow<List<KnowledgeBookEntity>>
 @Query("SELECT * FROM knowledge_books WHERE bookId=:bookId LIMIT 1") suspend fun forBook(bookId:String):KnowledgeBookEntity?
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveBook(book:KnowledgeBookEntity)
 @Query("SELECT * FROM knowledge_topics WHERE knowledgeBookId=:knowledgeBookId ORDER BY startPage") suspend fun topics(knowledgeBookId:String):List<KnowledgeTopicEntity>
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveTopics(topics:List<KnowledgeTopicEntity>)
 @Query("UPDATE knowledge_topics SET approved=:approved WHERE id=:id") suspend fun setTopicApproved(id:String,approved:Boolean)
 @Query("DELETE FROM knowledge_topics WHERE knowledgeBookId=:knowledgeBookId") suspend fun clearTopics(knowledgeBookId:String)
 @Query("DELETE FROM knowledge_books WHERE bookId=:bookId") suspend fun deleteForBook(bookId:String)
}

@Entity(tableName="saved_lessons",indices=[Index("updatedAt")])
data class SavedLessonEntity(
 @PrimaryKey val id:String,
 val title:String,
 val audienceLevel:String,
 val durationMinutes:Int,
 val outline:String,
 val createdAt:Long=System.currentTimeMillis(),
 val updatedAt:Long=System.currentTimeMillis()
)
@Dao interface LessonDao {
 @Query("SELECT * FROM saved_lessons ORDER BY updatedAt DESC") fun lessons():Flow<List<SavedLessonEntity>>
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveLesson(lesson:SavedLessonEntity)
 @Query("DELETE FROM saved_lessons WHERE id=:id") suspend fun deleteLesson(id:String)
}

@Database(entities=[ConversationEntity::class,MessageEntity::class,LocalModelEntity::class,WorkspaceProjectEntity::class,KnowledgeChunkEntity::class,BookEntity::class,BookPassageEntity::class,KnowledgeBookEntity::class,KnowledgeTopicEntity::class,SavedLessonEntity::class],version=9,exportSchema=false)
abstract class AppDatabase:RoomDatabase(){
 abstract fun chatDao():ChatDao
 abstract fun modelDao():ModelDao
 abstract fun workspaceDao():WorkspaceDao
 abstract fun knowledgeDao():KnowledgeDao
 abstract fun bookDao():BookDao
 abstract fun lessonDao():LessonDao
 abstract fun knowledgePoolDao():KnowledgePoolDao
}

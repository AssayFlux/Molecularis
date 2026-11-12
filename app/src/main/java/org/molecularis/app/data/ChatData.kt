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
@Database(entities=[ConversationEntity::class,MessageEntity::class,LocalModelEntity::class,WorkspaceProjectEntity::class,KnowledgeChunkEntity::class],version=6,exportSchema=false)
abstract class AppDatabase:RoomDatabase(){
 abstract fun chatDao():ChatDao
 abstract fun modelDao():ModelDao
 abstract fun workspaceDao():WorkspaceDao
 abstract fun knowledgeDao():KnowledgeDao
}

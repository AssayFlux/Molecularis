package org.molecularis.app.data
import androidx.room.*
import kotlinx.coroutines.flow.Flow
@Entity(tableName="subject_workspaces", indices=[Index("updatedAt")])
data class SubjectWorkspaceEntity(
 @PrimaryKey val id:String,
 val name:String,
 val description:String="",
 val disciplineCode:String?=null,
 val languageTag:String="en",
 val createdAt:Long=System.currentTimeMillis(),
 val updatedAt:Long=System.currentTimeMillis(),
 val isDefault:Boolean=false
)
@Entity(tableName="professor_profiles", indices=[Index("subjectId"),Index("updatedAt")])
data class ProfessorProfileEntity(
 @PrimaryKey val id:String,
 val subjectId:String,
 val name:String,
 val role:String="evidence-aware learning professor",
 val instructions:String="",
 val learnerLevel:String="general",
 val tone:String="clear and supportive",
 val objectives:String="",
 val sourcePolicy:String="Prefer reviewed workspace sources; distinguish evidence from general knowledge.",
 val safetyBoundaries:String="Do not provide individualized high-impact professional decisions.",
 val promptVersion:String="1",
 val createdAt:Long=System.currentTimeMillis(),
 val updatedAt:Long=System.currentTimeMillis(),
 val isDefault:Boolean=false
)
@Entity(tableName="conversations", indices=[Index("subjectId"),Index("professorProfileId")])
data class ConversationEntity(@PrimaryKey(autoGenerate=true) val id:Long=0,val title:String,val createdAt:Long=System.currentTimeMillis(),val archived:Boolean=false,val pinned:Boolean=false,val workspaceProjectId:Long?=null,@ColumnInfo(defaultValue="'legacy-default'") val subjectId:String="legacy-default",val professorProfileId:String?=null)
@Entity(tableName="messages",indices=[Index("conversationId")])
data class MessageEntity(@PrimaryKey(autoGenerate=true) val id:Long=0,val conversationId:Long,val body:String,val role:String,val createdAt:Long=System.currentTimeMillis(),val status:String="complete",val attachmentUri:String?=null,val attachmentName:String?=null,val attachmentText:String?=null,val professorProfileId:String?=null,val modelProvider:String?=null,val modelVersion:String?=null,val promptVersion:String?=null,val promptHash:String?=null,val sourceSetHash:String?=null,val retrievalConfig:String?=null)
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

@Dao interface SubjectWorkspaceDao {
 @Query("SELECT * FROM subject_workspaces ORDER BY isDefault DESC,updatedAt DESC") fun workspaces():Flow<List<SubjectWorkspaceEntity>>
 @Query("SELECT * FROM subject_workspaces WHERE id=:id LIMIT 1") suspend fun workspace(id:String):SubjectWorkspaceEntity?
 @Insert(onConflict=OnConflictStrategy.ABORT) suspend fun add(workspace:SubjectWorkspaceEntity)
 @Update suspend fun update(workspace:SubjectWorkspaceEntity)
 @Query("UPDATE subject_workspaces SET updatedAt=:updatedAt WHERE id=:id") suspend fun touch(id:String,updatedAt:Long=System.currentTimeMillis())
 @Query("SELECT * FROM subject_workspaces WHERE isDefault=1 LIMIT 1") suspend fun defaultWorkspace():SubjectWorkspaceEntity?
}
@Dao interface ProfessorProfileDao {
 @Query("SELECT * FROM professor_profiles WHERE subjectId=:subjectId ORDER BY isDefault DESC,updatedAt DESC") fun profiles(subjectId:String):Flow<List<ProfessorProfileEntity>>
 @Query("SELECT * FROM professor_profiles WHERE id=:id LIMIT 1") suspend fun profile(id:String):ProfessorProfileEntity?
 @Insert(onConflict=OnConflictStrategy.ABORT) suspend fun add(profile:ProfessorProfileEntity)
 @Update suspend fun update(profile:ProfessorProfileEntity)
 @Query("DELETE FROM professor_profiles WHERE id=:id") suspend fun delete(id:String)
 @Query("SELECT * FROM professor_profiles WHERE subjectId=:subjectId AND isDefault=1 LIMIT 1") suspend fun defaultProfile(subjectId:String):ProfessorProfileEntity?
}
@Dao interface ChatDao {
 @Query("SELECT * FROM conversations WHERE archived=0 ORDER BY pinned DESC,createdAt DESC") fun conversations():Flow<List<ConversationEntity>>
 @Query("SELECT * FROM conversations WHERE archived=0 AND subjectId=:subjectId ORDER BY pinned DESC,createdAt DESC") fun conversationsForSubject(subjectId:String):Flow<List<ConversationEntity>>
 @Query("SELECT * FROM messages WHERE conversationId=:id ORDER BY createdAt,id") fun messages(id:Long):Flow<List<MessageEntity>>
 @Insert suspend fun addConversation(item:ConversationEntity):Long
 @Insert suspend fun addMessage(item:MessageEntity):Long
 @Query("UPDATE messages SET attachmentText=:text WHERE id=:id") suspend fun updateAttachmentText(id:Long,text:String)
 @Query("SELECT * FROM messages WHERE conversationId=:id AND attachmentText IS NOT NULL ORDER BY createdAt DESC LIMIT 5") suspend fun attachmentMessages(id:Long):List<MessageEntity>
 @Query("SELECT * FROM conversations WHERE id=:id LIMIT 1") suspend fun conversation(id:Long):ConversationEntity?
 @Query("SELECT * FROM conversations WHERE workspaceProjectId=:projectId AND subjectId=:subjectId AND archived=0 ORDER BY createdAt DESC LIMIT 1") suspend fun latestProjectConversation(projectId:Long,subjectId:String):ConversationEntity?
 @Query("UPDATE conversations SET title=:title WHERE id=:id") suspend fun rename(id:Long,title:String)
 @Query("UPDATE conversations SET professorProfileId=:profileId WHERE id=:conversationId AND subjectId=:subjectId") suspend fun setProfessorProfile(conversationId:Long,subjectId:String,profileId:String?)
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

@Entity(tableName="books",indices=[Index("importedAt"),Index("fileSha256"),Index("subjectId")])
data class BookEntity(
 @PrimaryKey val id:String,
 val title:String,
 val originalFileName:String,
 val localPath:String,
 val sourceUri:String,
 val pageCount:Int,
 val extractedChars:Int,
 val importedAt:Long=System.currentTimeMillis(),
 val fileSha256:String?=null,
 @ColumnInfo(defaultValue="'legacy-default'") val subjectId:String="legacy-default"
)
@Entity(tableName="book_passages",indices=[Index("bookId"),Index("pageNumber")],foreignKeys=[ForeignKey(entity=BookEntity::class,parentColumns=["id"],childColumns=["bookId"],onDelete=ForeignKey.CASCADE)])
data class BookPassageEntity(
 @PrimaryKey val id:String,
 val bookId:String,
 val chunkIndex:Int,
 val pageNumber:Int,
 val text:String
)

@Fts4(contentEntity = BookPassageEntity::class)
@Entity(tableName = "book_passages_fts")
data class BookPassageFts(val text: String)

@Entity(tableName="knowledge_page_audits",primaryKeys=["stagingBookId","pageNumber"],indices=[Index("stagingBookId"),Index("fingerprint")])
data class KnowledgePageAuditEntity(val stagingBookId:String,val pageNumber:Int,val charCount:Int,val fingerprint:String,val qualityFlag:String)
@Entity(tableName="knowledge_processing_checkpoints")
data class KnowledgeProcessingCheckpointEntity(@PrimaryKey val bookId:String,val stagingBookId:String,val nextPage:Int,val extractedChars:Int,val passageCount:Int,val updatedAt:Long=System.currentTimeMillis())

@Dao interface BookDao {
 @Query("SELECT * FROM books WHERE id NOT GLOB '__stage__*' ORDER BY importedAt DESC") fun books():Flow<List<BookEntity>>
 @Query("SELECT * FROM books WHERE id NOT GLOB '__stage__*' AND subjectId=:subjectId ORDER BY importedAt DESC") fun booksForSubject(subjectId:String):Flow<List<BookEntity>>
 @Query("SELECT * FROM books WHERE id=:bookId AND subjectId=:subjectId LIMIT 1") suspend fun bookInSubject(bookId:String,subjectId:String):BookEntity?
 @Insert suspend fun addBook(book:BookEntity)
 @Query("SELECT * FROM books WHERE id=:bookId LIMIT 1") suspend fun book(bookId:String):BookEntity?
 @Query("SELECT * FROM books WHERE fileSha256=:sha256 LIMIT 1") suspend fun bookBySha256(sha256:String):BookEntity?
 @Query("SELECT * FROM books WHERE fileSha256=:sha256 AND subjectId=:subjectId LIMIT 1") suspend fun bookBySha256InSubject(sha256:String,subjectId:String):BookEntity?
 @Query("SELECT * FROM books WHERE title=:title COLLATE NOCASE ORDER BY importedAt DESC LIMIT 1") suspend fun bookByTitle(title:String):BookEntity?
 @Update suspend fun updateBook(book:BookEntity)
 @Transaction suspend fun deleteBookAndProcessingState(bookId:String) { clearProcessingCheckpointAndStage(bookId); deletePageAudits(bookId); deleteBook(bookId) }
 @Transaction suspend fun clearProcessingCheckpointAndStage(bookId:String) {
  val checkpoint = processingCheckpoint(bookId)
  if (checkpoint != null) {
   deletePageAudits(checkpoint.stagingBookId)
   deleteBook(checkpoint.stagingBookId)
   deleteProcessingCheckpoint(bookId)
  }
 }
 @Query("SELECT * FROM knowledge_processing_checkpoints WHERE bookId=:bookId LIMIT 1") suspend fun processingCheckpoint(bookId:String):KnowledgeProcessingCheckpointEntity?
 @Query("SELECT COUNT(*) FROM knowledge_page_audits WHERE stagingBookId=:stageId AND fingerprint=:fingerprint") suspend fun pageFingerprintCount(stageId:String,fingerprint:String):Int
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun savePageAudit(audit:KnowledgePageAuditEntity)
 @Query("SELECT * FROM knowledge_page_audits WHERE stagingBookId=:stageId ORDER BY pageNumber") suspend fun pageAudits(stageId:String):List<KnowledgePageAuditEntity>
 @Query("DELETE FROM knowledge_page_audits WHERE stagingBookId=:stageId") suspend fun deletePageAudits(stageId:String)
 @Query("UPDATE knowledge_page_audits SET stagingBookId=:bookId WHERE stagingBookId=:stageId") suspend fun movePageAudits(stageId:String,bookId:String)
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveProcessingCheckpoint(checkpoint:KnowledgeProcessingCheckpointEntity)
 @Query("DELETE FROM knowledge_processing_checkpoints WHERE bookId=:bookId") suspend fun deleteProcessingCheckpoint(bookId:String)
 @Insert suspend fun addPassages(passages:List<BookPassageEntity>)
 @Query("DELETE FROM book_passages WHERE bookId=:bookId") suspend fun deletePassages(bookId:String)
 @Query("SELECT * FROM book_passages WHERE bookId=:bookId ORDER BY pageNumber,chunkIndex") suspend fun passages(bookId:String):List<BookPassageEntity>
 @Query("SELECT * FROM book_passages WHERE bookId=:bookId AND pageNumber=:page ORDER BY chunkIndex") suspend fun passagesAtPage(bookId:String,page:Int):List<BookPassageEntity>
 @Query("SELECT book_passages.* FROM book_passages JOIN book_passages_fts ON book_passages_fts.rowid = book_passages.rowid WHERE book_passages.bookId=:bookId AND book_passages_fts MATCH :query ORDER BY book_passages.pageNumber LIMIT 100") suspend fun searchInBookIndexed(bookId:String,query:String):List<BookPassageEntity>
 @Query("SELECT book_passages.* FROM book_passages JOIN book_passages_fts ON book_passages_fts.rowid = book_passages.rowid WHERE book_passages.bookId IN (SELECT id FROM books WHERE id NOT GLOB '__stage__*') AND book_passages_fts MATCH :query ORDER BY book_passages.bookId,book_passages.pageNumber LIMIT 100") suspend fun searchAllIndexed(query:String):List<BookPassageEntity>
 @Query("SELECT book_passages.* FROM book_passages JOIN book_passages_fts ON book_passages_fts.rowid = book_passages.rowid WHERE book_passages_fts MATCH :query AND (:bookId IS NULL OR book_passages.bookId=:bookId) AND (:fromPage IS NULL OR book_passages.pageNumber>=:fromPage) AND (:toPage IS NULL OR book_passages.pageNumber<=:toPage) ORDER BY book_passages.bookId,book_passages.pageNumber LIMIT 100") suspend fun searchFilteredIndexed(query:String,bookId:String?,fromPage:Int?,toPage:Int?):List<BookPassageEntity>
 @Query("SELECT * FROM book_passages WHERE bookId=:bookId AND text LIKE '%' || :query || '%' ORDER BY pageNumber LIMIT 100") suspend fun searchInBook(bookId:String,query:String):List<BookPassageEntity>
 @Query("SELECT * FROM book_passages WHERE bookId IN (SELECT id FROM books WHERE id NOT GLOB '__stage__*') AND text LIKE '%' || :query || '%' ORDER BY bookId,pageNumber LIMIT 100") suspend fun searchAll(query:String):List<BookPassageEntity>
 @Query("SELECT p.* FROM book_passages p INNER JOIN books b ON b.id=p.bookId WHERE b.subjectId=:subjectId AND b.id NOT GLOB '__stage__*' AND p.text LIKE '%' || :query || '%' ORDER BY p.bookId,p.pageNumber LIMIT 100") suspend fun searchAllForSubject(subjectId:String,query:String):List<BookPassageEntity>
 @Query("UPDATE books SET pageCount=:pageCount, extractedChars=:extractedChars WHERE id=:bookId") suspend fun updateBookStats(bookId:String,pageCount:Int,extractedChars:Int)
 @Query("DELETE FROM books WHERE id=:bookId") suspend fun deleteBook(bookId:String)
 @Query("DELETE FROM knowledge_page_audits WHERE stagingBookId IN (SELECT id FROM books WHERE id GLOB '__stage__*' AND importedAt < :olderThan AND id NOT IN (SELECT stagingBookId FROM knowledge_processing_checkpoints))") suspend fun deleteStalePageAudits(olderThan:Long)
 @Query("DELETE FROM books WHERE id GLOB '__stage__*' AND importedAt < :olderThan AND id NOT IN (SELECT stagingBookId FROM knowledge_processing_checkpoints)") suspend fun deleteStaleStagingBooksQuery(olderThan:Long)
 @Transaction suspend fun cleanupStaleStagingBooks(olderThan:Long) { deleteStalePageAudits(olderThan); deleteStaleStagingBooksQuery(olderThan) }
 @Query("UPDATE book_passages SET bookId=:bookId WHERE bookId=:stagingBookId") suspend fun moveStagedPassages(stagingBookId:String,bookId:String)
 @Transaction suspend fun replacePassagesFromStage(bookId:String,stagingBookId:String) {
  deletePassages(bookId)
  moveStagedPassages(stagingBookId,bookId)
  deleteBook(stagingBookId)
 }
}

@Entity(tableName="knowledge_books",indices=[Index("bookId",unique=true)])
data class KnowledgeBookEntity(
 @PrimaryKey val id:String,val bookId:String,val detectedTitle:String,val author:String,
 val publisher:String,val edition:String,val subject:String,val summary:String,
 val chapterOutline:String,val extractedPageCount:Int,val extractedChars:Int,
 val passageCount:Int,val topicCount:Int,val qualityScore:Int,
 val reviewState:String="needs_review",val processedAt:Long=System.currentTimeMillis(),
 @ColumnInfo(defaultValue="0") val pagesWithText:Int=0,
 @ColumnInfo(defaultValue="0") val emptyPages:Int=0,
 @ColumnInfo(defaultValue="0") val shortTextPages:Int=0,
 @ColumnInfo(defaultValue="0") val duplicatePages:Int=0
)
@Entity(tableName="knowledge_topics",indices=[Index("knowledgeBookId"),Index("name"),Index("parentTopicId")])
data class KnowledgeTopicEntity(
 @PrimaryKey val id:String,val knowledgeBookId:String,val name:String,
 val startPage:Int,val confidence:Float,val evidence:String,val approved:Boolean=false,
 val parentTopicId:String?=null
)
@Entity(tableName="knowledge_topic_aliases",indices=[Index(value=["topicId","normalizedAlias"],unique=true)],foreignKeys=[ForeignKey(entity=KnowledgeTopicEntity::class,parentColumns=["id"],childColumns=["topicId"],onDelete=ForeignKey.CASCADE)])
data class KnowledgeTopicAliasEntity(
 @PrimaryKey val id:String,val topicId:String,val alias:String,val normalizedAlias:String
)
/** Explicit provenance links from reviewed topics to the exact OCR passages that support them. */
@Entity(tableName="knowledge_topic_passage_links",primaryKeys=["topicId","passageId"],indices=[Index("topicId"),Index("passageId")],foreignKeys=[
 ForeignKey(entity=KnowledgeTopicEntity::class,parentColumns=["id"],childColumns=["topicId"],onDelete=ForeignKey.CASCADE),
 ForeignKey(entity=BookPassageEntity::class,parentColumns=["id"],childColumns=["passageId"],onDelete=ForeignKey.CASCADE)
])
data class KnowledgeTopicPassageLinkEntity(val topicId:String,val passageId:String,val pageNumber:Int,val linkType:String="section_page_range")
@Dao interface KnowledgePoolDao {
 @Query("SELECT * FROM knowledge_books ORDER BY processedAt DESC") fun books():Flow<List<KnowledgeBookEntity>>
 @Query("SELECT kb.* FROM knowledge_books kb INNER JOIN books b ON b.id=kb.bookId WHERE b.subjectId=:subjectId ORDER BY kb.processedAt DESC") fun booksForSubject(subjectId:String):Flow<List<KnowledgeBookEntity>>
 @Query("SELECT * FROM knowledge_books WHERE bookId=:bookId LIMIT 1") suspend fun forBook(bookId:String):KnowledgeBookEntity?
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveBook(book:KnowledgeBookEntity)
 @Query("UPDATE knowledge_books SET detectedTitle=:title,author=:author,publisher=:publisher,edition=:edition,subject=:subject,reviewState='needs_review' WHERE id=:id") suspend fun updateMetadata(id:String,title:String,author:String,publisher:String,edition:String,subject:String)
 @Query("SELECT * FROM knowledge_topics WHERE knowledgeBookId=:knowledgeBookId ORDER BY COALESCE(parentTopicId,''),startPage,name COLLATE NOCASE") suspend fun topics(knowledgeBookId:String):List<KnowledgeTopicEntity>
 @Insert(onConflict=OnConflictStrategy.IGNORE) suspend fun addTopicPassageLinks(links:List<KnowledgeTopicPassageLinkEntity>)
 @Query("SELECT book_passages.* FROM book_passages INNER JOIN knowledge_topic_passage_links ON knowledge_topic_passage_links.passageId=book_passages.id WHERE knowledge_topic_passage_links.topicId=:topicId ORDER BY book_passages.pageNumber,book_passages.chunkIndex") suspend fun passagesForTopic(topicId:String):List<BookPassageEntity>
 @Query("INSERT OR IGNORE INTO knowledge_topic_passage_links(topicId,passageId,pageNumber,linkType) SELECT :topicId,id,pageNumber,'manual_page' FROM book_passages WHERE bookId=:bookId AND pageNumber=:page") suspend fun linkTopicToPage(topicId:String,bookId:String,page:Int)
 @Query("INSERT OR IGNORE INTO knowledge_topic_passage_links(topicId,passageId,pageNumber,linkType) SELECT :targetId,passageId,pageNumber,linkType FROM knowledge_topic_passage_links WHERE topicId=:sourceId") suspend fun copyPassageLinks(sourceId:String,targetId:String)
 @Query("SELECT * FROM knowledge_topic_aliases WHERE topicId=:topicId ORDER BY alias COLLATE NOCASE") suspend fun aliases(topicId:String):List<KnowledgeTopicAliasEntity>
 @Insert(onConflict=OnConflictStrategy.IGNORE) suspend fun addAlias(alias:KnowledgeTopicAliasEntity):Long
 @Query("DELETE FROM knowledge_topic_aliases WHERE id=:aliasId") suspend fun deleteAlias(aliasId:String)
 @Query("UPDATE knowledge_topics SET parentTopicId=:parentId,approved=0 WHERE id=:topicId") suspend fun updateTopicParent(topicId:String,parentId:String?)
 @Transaction suspend fun setTopicParent(topicId:String,parentId:String?) {
  val topic = topicById(topicId) ?: error("Topic not found")
  if (parentId != null) {
   var cursor = topicById(parentId) ?: error("Parent topic not found")
   require(cursor.knowledgeBookId == topic.knowledgeBookId) { "Parent must belong to the same source book." }
   val visited = mutableSetOf<String>()
   while (true) {
    require(cursor.id != topicId) { "A topic cannot be its own ancestor." }
    require(visited.add(cursor.id)) { "Existing topic hierarchy contains a cycle." }
    val next = cursor.parentTopicId ?: break
    cursor = topicById(next) ?: break
   }
  }
  updateTopicParent(topicId,parentId)
 }
 @Query("UPDATE knowledge_topics SET parentTopicId=:targetId WHERE parentTopicId=:sourceId") suspend fun reparentChildren(sourceId:String,targetId:String?)
 @Query("INSERT OR IGNORE INTO knowledge_topic_aliases(id,topicId,alias,normalizedAlias) SELECT lower(hex(randomblob(16))),:targetId,alias,normalizedAlias FROM knowledge_topic_aliases WHERE topicId=:sourceId") suspend fun copyAliasesToTopic(sourceId:String,targetId:String)
 @Query("DELETE FROM knowledge_topic_aliases WHERE topicId=:sourceId") suspend fun deleteAliasesForTopic(sourceId:String)
 @Query("UPDATE knowledge_topics SET startPage=MIN(startPage,(SELECT startPage FROM knowledge_topics WHERE id=:sourceId)),confidence=MAX(confidence,(SELECT confidence FROM knowledge_topics WHERE id=:sourceId)),evidence=evidence || '; Merged: ' || (SELECT evidence FROM knowledge_topics WHERE id=:sourceId),approved=CASE WHEN approved=1 AND (SELECT approved FROM knowledge_topics WHERE id=:sourceId)=1 THEN 1 ELSE 0 END WHERE id=:targetId") suspend fun reconcileMergedApproval(sourceId:String,targetId:String)
 @Query("DELETE FROM knowledge_topics WHERE id=:sourceId") suspend fun deleteTopicById(sourceId:String)
 @Transaction suspend fun mergeTopic(sourceId:String,targetId:String) {
  require(sourceId != targetId)
  val source = topicById(sourceId) ?: error("Source topic not found")
  val target = topicById(targetId) ?: error("Target topic not found")
  require(source.knowledgeBookId == target.knowledgeBookId) { "Topics from different books cannot be merged." }
  var ancestor:KnowledgeTopicEntity? = target
  val visited = mutableSetOf<String>()
  while (ancestor != null && visited.add(ancestor.id)) {
   require(ancestor.id != sourceId) { "Cannot merge a topic into one of its descendants." }
   ancestor = ancestor.parentTopicId?.let { topicById(it) }
  }
  reparentChildren(sourceId,targetId)
  copyAliasesToTopic(sourceId,targetId)
  copyPassageLinks(sourceId,targetId)
  reconcileMergedApproval(sourceId,targetId)
  deleteAliasesForTopic(sourceId)
  deleteTopicById(sourceId)
 }
 @Query("SELECT * FROM knowledge_topics WHERE id=:id LIMIT 1") suspend fun topicById(id:String):KnowledgeTopicEntity?
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveTopics(topics:List<KnowledgeTopicEntity>)
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun addTopic(topic:KnowledgeTopicEntity)
 @Query("UPDATE knowledge_topics SET name=:name,startPage=:startPage,approved=0 WHERE id=:id") suspend fun updateTopicDetails(id:String,name:String,startPage:Int)
 @Query("UPDATE knowledge_topics SET approved=:approved WHERE id=:id") suspend fun setTopicApproved(id:String,approved:Boolean)
 @Query("DELETE FROM knowledge_topics WHERE knowledgeBookId=:knowledgeBookId") suspend fun clearTopics(knowledgeBookId:String)
 @Query("UPDATE knowledge_books SET reviewState=:state WHERE id=:id") suspend fun setReviewState(id:String,state:String)
 @Query("DELETE FROM knowledge_topics WHERE knowledgeBookId IN (SELECT id FROM knowledge_books WHERE bookId=:bookId)") suspend fun deleteTopicsForBook(bookId:String)
 @Query("DELETE FROM knowledge_books WHERE bookId=:bookId") suspend fun deleteBookMetadataForBook(bookId:String)
 @Transaction suspend fun deleteForBook(bookId:String) { deleteTopicsForBook(bookId); deleteBookMetadataForBook(bookId) }
}

@Entity(tableName="saved_lessons",indices=[Index("updatedAt"),Index("subjectId")])
data class SavedLessonEntity(
 @PrimaryKey val id:String,
 val title:String,
 val audienceLevel:String,
 val durationMinutes:Int,
 val outline:String,
 val createdAt:Long=System.currentTimeMillis(),
 val updatedAt:Long=System.currentTimeMillis(),
 @ColumnInfo(defaultValue="'legacy-default'") val subjectId:String="legacy-default",
 val professorProfileId:String?=null,
 @ColumnInfo(defaultValue="'1'") val promptVersion:String="1"
)
@Dao interface LessonDao {
 @Query("SELECT * FROM saved_lessons ORDER BY updatedAt DESC") fun lessons():Flow<List<SavedLessonEntity>>
 @Query("SELECT * FROM saved_lessons WHERE subjectId=:subjectId ORDER BY updatedAt DESC") fun lessonsForSubject(subjectId:String):Flow<List<SavedLessonEntity>>
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveLesson(lesson:SavedLessonEntity)
 @Query("SELECT * FROM saved_lessons WHERE id=:id LIMIT 1") suspend fun lesson(id:String):SavedLessonEntity?
 @Query("DELETE FROM saved_lessons WHERE id=:id") suspend fun deleteLesson(id:String)
}

@Entity(tableName="saved_diagrams",indices=[Index("updatedAt")])
data class SavedDiagramEntity(@PrimaryKey val id:String,val title:String,val template:String,val diagramJson:String,val updatedAt:Long=System.currentTimeMillis())
@Dao interface DiagramDao {
 @Query("SELECT * FROM saved_diagrams ORDER BY updatedAt DESC") fun diagrams():Flow<List<SavedDiagramEntity>>
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun saveDiagram(diagram:SavedDiagramEntity)
 @Query("DELETE FROM saved_diagrams WHERE id=:id") suspend fun deleteDiagram(id:String)
}

@Database(entities=[SubjectWorkspaceEntity::class,ProfessorProfileEntity::class,ConversationEntity::class,MessageEntity::class,LocalModelEntity::class,WorkspaceProjectEntity::class,KnowledgeChunkEntity::class,BookEntity::class,BookPassageEntity::class,KnowledgeBookEntity::class,KnowledgeTopicEntity::class,SavedLessonEntity::class,BookPassageFts::class,KnowledgeProcessingCheckpointEntity::class,KnowledgeTopicAliasEntity::class,KnowledgePageAuditEntity::class,KnowledgeTopicPassageLinkEntity::class,SavedDiagramEntity::class,ScheduledLectureEntity::class],version=18,exportSchema=false)
abstract class AppDatabase:RoomDatabase(){
 abstract fun subjectWorkspaceDao():SubjectWorkspaceDao
 abstract fun professorProfileDao():ProfessorProfileDao
 abstract fun chatDao():ChatDao
 abstract fun modelDao():ModelDao
 abstract fun workspaceDao():WorkspaceDao
 abstract fun knowledgeDao():KnowledgeDao
 abstract fun bookDao():BookDao
 abstract fun lessonDao():LessonDao
 abstract fun diagramDao():DiagramDao
 abstract fun scheduledLectureDao():ScheduledLectureDao
 abstract fun knowledgePoolDao():KnowledgePoolDao
}

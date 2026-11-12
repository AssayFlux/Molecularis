package org.molecularis.app.ui

import android.Manifest
import android.content.Context
import android.content.ComponentCallbacks2
import android.content.res.Configuration
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.StatFs
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.layout.imePadding
import androidx.documentfile.provider.DocumentFile
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Job
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.molecularis.app.ai.LiteRtRuntime
import org.molecularis.app.ai.ConversationPromptBuilder
import org.molecularis.app.ai.PromptTurn
import org.molecularis.app.ai.Capability
import org.molecularis.app.ai.CollaborationEngine
import org.molecularis.app.ai.CollaborationResult
import org.molecularis.app.ai.InferenceRequest
import org.molecularis.app.ai.LiteRtModelProvider
import org.molecularis.app.ai.ModelCatalog
import org.molecularis.app.ai.ModelDescriptor
import org.molecularis.app.data.*
import org.molecularis.app.features.OfflineDocumentReader
import org.molecularis.app.features.OfflineImageAnalyzer
import org.molecularis.app.features.VisionImagePreprocessor
import org.molecularis.app.features.LocalRagIndex
import org.molecularis.app.features.OnnxWordPieceEmbedder
import org.molecularis.app.features.PersistentHybridRag
import org.molecularis.app.features.OfflineVoiceController
import org.molecularis.app.features.VerifiedModelDownloader
import org.molecularis.app.features.OfflineDatasetInspector
import org.molecularis.app.features.DatasetReport
import org.molecularis.app.features.TrainingApiClient
import org.molecularis.app.features.TrainingJobStatus
import org.molecularis.app.features.OpenAiCompatibleClient
import org.molecularis.app.features.RemoteChatMessage
import org.molecularis.app.features.EncryptedSecretStore
import java.io.ByteArrayOutputStream
import java.io.File
import java.util.UUID

private val Muted=Color(0xFF65736D)
private enum class Section(val label:String){TEACHING("Teach"),CHATS("Chats"),LIBRARY("Library"),AI_HUB("AI Hub"),MODELS("Models"),TRAINING("Training"),WORKSPACE("Workspace"),ONLINE_AI("Online AI"),SETTINGS("Settings")}

@OptIn(ExperimentalMaterial3Api::class)
@Composable fun MessengerApp(){
 val context=LocalContext.current
 val db= remember{DatabaseProvider.get(context)}
 val runtime= remember{LiteRtRuntime(context)}
 val scope= rememberCoroutineScope()
 var section by remember{mutableStateOf(Section.CHATS)}
 var moreNavigationExpanded by remember{mutableStateOf(false)}
 var selectedConversation by remember{mutableStateOf<Long?>(null)}
 var draft by remember{mutableStateOf("")}
 var pendingAttachment by remember{mutableStateOf<Pair<Uri,String>?>(null)}
 val activeModelPrefs=remember(context){context.getSharedPreferences("molecularis_active_model",Context.MODE_PRIVATE)}
 var activeModelPath by remember{mutableStateOf(activeModelPrefs.getString("path",null))}
 var activeModelName by remember{mutableStateOf<String?>(null)}
 var restoringActiveModel by remember{mutableStateOf(false)}
 var runtimeMessage by remember{mutableStateOf("Import a .litertlm model to start offline AI chat.")}
 DisposableEffect(context,runtime){
  val memoryCallbacks=object:ComponentCallbacks2{
   override fun onConfigurationChanged(newConfig:Configuration) = Unit
   override fun onLowMemory(){onTrimMemory(ComponentCallbacks2.TRIM_MEMORY_RUNNING_CRITICAL)}
   override fun onTrimMemory(level:Int){
    if(level>=ComponentCallbacks2.TRIM_MEMORY_RUNNING_LOW&&activeModelPath!=null){
     scope.launch{
      runCatching{runtime.unload()}
      activeModelPrefs.edit().remove("path").apply()
      activeModelPath=null
      activeModelName=null
      runtimeMessage="Model unloaded to protect the app during memory pressure. Reload it from Models when memory is available."
     }
    }
   }
  }
  context.registerComponentCallbacks(memoryCallbacks)
  onDispose{context.unregisterComponentCallbacks(memoryCallbacks)}
 }

 val personalizationPrefs=remember(context){context.getSharedPreferences("molecularis_personalization",Context.MODE_PRIVATE)}
 var responseStyle by remember{mutableStateOf(personalizationPrefs.getString("response_style","balanced")?:"balanced")}
 var darkAppearance by remember{mutableStateOf(personalizationPrefs.getBoolean("dark_appearance",false))}
 var accentName by remember{mutableStateOf(personalizationPrefs.getString("accent_name","Sage")?:"Sage")}
 val enginePrefs=remember(context){context.getSharedPreferences("molecularis_engine",Context.MODE_PRIVATE)}
 var engineOptimization by remember{mutableStateOf(enginePrefs.getString("optimization","balanced")?:"balanced")}
 val onlinePrefs=remember(context){context.getSharedPreferences("molecularis_online_ai",Context.MODE_PRIVATE)}
 val secretStore=remember(context){EncryptedSecretStore(context)}
 var onlineBaseUrl by remember{mutableStateOf(onlinePrefs.getString("base_url","")?:"")}
 var onlineModelId by remember{mutableStateOf(onlinePrefs.getString("model_id","")?:"")}
 var onlineEnabled by remember{mutableStateOf(onlinePrefs.getBoolean("enabled",false))}
 var onlineHasKey by remember{mutableStateOf(runCatching{!secretStore.get("online_api_key").isNullOrBlank()}.getOrDefault(false))}
 var onlineStatus by remember{mutableStateOf("Online AI is disabled. Configure a provider and explicitly enable it to use remote inference.")}
 var voiceListening by remember{mutableStateOf(false)}
 val speechPrefs=remember(context){context.getSharedPreferences("molecularis_offline_speech",Context.MODE_PRIVATE)}
 var speechLanguageTag by remember{mutableStateOf(speechPrefs.getString("language_tag",java.util.Locale.getDefault().toLanguageTag())?:java.util.Locale.getDefault().toLanguageTag())}
 var ttsVoiceName by remember{mutableStateOf(speechPrefs.getString("tts_voice_name",null))}
 var offlineTtsVoices by remember{mutableStateOf(emptyList<org.molecularis.app.features.OfflineTtsVoice>())}
 var recognitionLanguages by remember{mutableStateOf(org.molecularis.app.features.OfflineRecognitionLanguages(emptyList(),emptyList(),emptyList()))}
 var speechStatus by remember{mutableStateOf("Offline speech is device-managed. Check installed language packs before use.")}
 val voiceController=remember(context){OfflineVoiceController(context,onResult={spoken->draft=if(draft.isBlank())spoken else "$draft $spoken"},onError={runtimeMessage=it;speechStatus=it},onListeningChanged={voiceListening=it},initialLanguageTag=speechLanguageTag,initialTtsVoiceName=ttsVoiceName,onVoiceCatalogChanged={voices->offlineTtsVoices=voices;if(ttsVoiceName==null)ttsVoiceName=voices.firstOrNull()?.name})}
 var loadingModel by remember{mutableStateOf(false)}
 var sending by remember{mutableStateOf(false)}
 var showNewProject by remember{mutableStateOf(false)}
 var showTeachingStudio by remember{mutableStateOf(false)}
 var projectName by remember{mutableStateOf("")}
 var projectDescription by remember{mutableStateOf("")}
 var collaborationPrompt by remember{mutableStateOf("")}
 var collaborationStatus by remember{mutableStateOf("Import two distinct compatible .litertlm models to enable collaboration.")}
 var collaborating by remember{mutableStateOf(false)}
 var downloadingModel by remember{mutableStateOf(false)}
 var modelDownloadJob by remember{mutableStateOf<Job?>(null)}
 var downloadProgress by remember{mutableFloatStateOf(0f)}
 var downloadStatus by remember{mutableStateOf("")}
 var datasetContent by remember{mutableStateOf("")}
 var datasetName by remember{mutableStateOf("")}
 var datasetReport by remember{mutableStateOf<DatasetReport?>(null)}
 var datasetStatus by remember{mutableStateOf("")}
 var datasetBusy by remember{mutableStateOf(false)}
 var trainingJob by remember{mutableStateOf<TrainingJobStatus?>(null)}
 var trainingStatus by remember{mutableStateOf("")}
 var trainingBusy by remember{mutableStateOf(false)}
 val embeddingPrefs=remember(context){context.getSharedPreferences("molecularis_local_embeddings",Context.MODE_PRIVATE)}
 var embeddingModelPath by remember{mutableStateOf(embeddingPrefs.getString("model_path",null))}
 var embeddingVocabPath by remember{mutableStateOf(embeddingPrefs.getString("vocab_path",null))}
 var embeddingStatus by remember{mutableStateOf("Optional: import a MiniLM-compatible ONNX model and its vocab.txt to enable semantic retrieval.")}
 val visionPrefs=remember(context){context.getSharedPreferences("molecularis_vision_models",Context.MODE_PRIVATE)}
 var visionModelPath by remember{mutableStateOf(visionPrefs.getString("vision_model_path",null))}
 var activeModelVision by remember{mutableStateOf(false)}
 val conversations by db.chatDao().conversations().collectAsState(initial=emptyList())
 val models by db.modelDao().models().collectAsState(initial=emptyList())
 val projects by db.workspaceDao().projects().collectAsState(initial=emptyList())
 val conversationId=selectedConversation?:conversations.firstOrNull()?.id
 val allMessages by db.chatDao().messages(conversationId?:-1L).collectAsState(initial=emptyList())
 val messages=allMessages.filter{it.conversationId==conversationId}
 LaunchedEffect(models,activeModelPath){
  if(!restoringActiveModel && activeModelPath!=null && activeModelName==null){
   val savedModel=models.firstOrNull{it.modelPath==activeModelPath}
   if(savedModel!=null && File(savedModel.modelPath!!).isFile){
    restoringActiveModel=true
    try{
     val vision=savedModel.modelPath==visionModelPath
     runtime.load(savedModel.modelPath!!,enableVision=vision)
     activeModelName=savedModel.displayName
     activeModelVision=vision
     runtimeMessage="Restored "+savedModel.displayName+". Ready for offline chat."
    }catch(error:Throwable){
     activeModelPath=null
     activeModelPrefs.edit().remove("path").apply()
     runtimeMessage="Saved model could not be restored: "+(error.message?:error.javaClass.simpleName)
    }finally{restoringActiveModel=false}
   }else if(models.isNotEmpty()){
    activeModelPath=null
    activeModelPrefs.edit().remove("path").apply()
   }
  }
 }
 DisposableEffect(runtime){onDispose{runtime.close()}}
 DisposableEffect(voiceController){onDispose{voiceController.close()}}
 LaunchedEffect(conversations,selectedConversation){
  if(selectedConversation!=null && conversations.none{it.id==selectedConversation}) selectedConversation=null
  if(selectedConversation==null && conversations.isEmpty()) selectedConversation=db.chatDao().addConversation(ConversationEntity(title="New conversation"))
 }
 val microphonePermission=rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()){granted->if(granted)voiceController.startListening()else runtimeMessage="Microphone permission was denied."}
 val attachmentPicker=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()){uri->
  if(uri!=null){
   runCatching{context.contentResolver.takePersistableUriPermission(uri,Intent.FLAG_GRANT_READ_URI_PERMISSION)}
   pendingAttachment=uri to (DocumentFile.fromSingleUri(context,uri)?.name?:"Attachment")
  }
 }
 val datasetPicker=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()){uri->
  if(uri!=null) scope.launch{
   datasetBusy=true
   try{
    val name=DocumentFile.fromSingleUri(context,uri)?.name?:"dataset.jsonl"
    val content=readDatasetBounded(context,uri)
    datasetContent=content
    datasetName=name
    datasetReport=OfflineDatasetInspector.inspect(content)
    datasetStatus="Validated "+name+" locally. No dataset was uploaded."
   }catch(error:Throwable){datasetReport=null;datasetStatus="Dataset import failed: "+(error.message?:error.javaClass.simpleName)}
   finally{datasetBusy=false}
  }
 }
 val datasetExport=rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/json")){uri->
  if(uri!=null) scope.launch{
   datasetBusy=true
   try{
    val report=datasetReport?:error("Import and validate a dataset first.")
    val invalid=report.invalidLines.toSet()
    val clean=datasetContent.lineSequence().mapIndexedNotNull{index,line->if(line.isNotBlank()&&index+1 !in invalid)line else null}.joinToString("\n")
    withContext(Dispatchers.IO){context.contentResolver.openOutputStream(uri)?.use{it.write(clean.toByteArray(Charsets.UTF_8))}?:error("Cannot create dataset output file.")}
    datasetStatus="Exported "+report.validRecords+" valid JSONL records."
   }catch(error:Throwable){datasetStatus="Dataset export failed: "+(error.message?:error.javaClass.simpleName)}
   finally{datasetBusy=false}
  }
 }
 val embeddingModelPicker=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()){uri->
  if(uri!=null) scope.launch{
   try{
    val name=DocumentFile.fromSingleUri(context,uri)?.name?: "sentence-embedder.onnx"
    require(name.endsWith(".onnx",true)){"Choose an ONNX embedding model (.onnx)."}
    val dir=File(context.filesDir,"embeddings").apply{mkdirs()}
    val target=File(dir,UUID.randomUUID().toString()+"-"+name.replace(Regex("[^A-Za-z0-9._-]"),"_"))
    withContext(Dispatchers.IO){context.contentResolver.openInputStream(uri)?.use{input->target.outputStream().use{output->input.copyTo(output)}}?:error("Cannot read ONNX model")}
    embeddingPrefs.edit().putString("model_path",target.absolutePath).apply()
    embeddingModelPath=target.absolutePath
    val vocab=embeddingVocabPath?.let(::File)
    if(vocab?.isFile==true){
     embeddingStatus="Validating local embedding model…"
     withContext(Dispatchers.IO){OnnxWordPieceEmbedder(target,vocab,target.name+":"+target.length()+":"+vocab.name+":"+vocab.length()).use{it.embed("Molecularis local semantic retrieval test")}}
     embeddingStatus="Semantic retrieval ready · "+name
    }else embeddingStatus="ONNX model imported. Now import the matching vocab.txt file."
   }catch(error:Throwable){embeddingStatus="Embedding model import failed: "+(error.message?:error.javaClass.simpleName)}
  }
 }
 val embeddingVocabPicker=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()){uri->
  if(uri!=null) scope.launch{
   try{
    val name=DocumentFile.fromSingleUri(context,uri)?.name?: "vocab.txt"
    require(name.equals("vocab.txt",true)||name.endsWith(".txt",true)){"Choose the matching WordPiece vocab.txt file."}
    val dir=File(context.filesDir,"embeddings").apply{mkdirs()}
    val target=File(dir,UUID.randomUUID().toString()+"-vocab.txt")
    withContext(Dispatchers.IO){context.contentResolver.openInputStream(uri)?.use{input->target.outputStream().use{output->input.copyTo(output)}}?:error("Cannot read vocabulary")}
    embeddingPrefs.edit().putString("vocab_path",target.absolutePath).apply()
    embeddingVocabPath=target.absolutePath
    val model=embeddingModelPath?.let(::File)
    if(model?.isFile==true){
     embeddingStatus="Validating local embedding model…"
     withContext(Dispatchers.IO){OnnxWordPieceEmbedder(model,target,model.name+":"+model.length()+":"+target.name+":"+target.length()).use{it.embed("Molecularis local semantic retrieval test")}}
     embeddingStatus="Semantic retrieval ready · "+model.name
    }else embeddingStatus="Vocabulary imported. Now import a compatible ONNX embedding model."
   }catch(error:Throwable){embeddingStatus="Vocabulary import failed: "+(error.message?:error.javaClass.simpleName)}
  }
 }
 val modelPicker=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()){uri->
  if(uri!=null) scope.launch{
   try{
    val doc=DocumentFile.fromSingleUri(context,uri)
    val name=doc?.name?: "local-model.litertlm"
    val supportedExtensions=listOf(".litertlm",".gguf",".ggml",".onnx",".tflite",".task",".safetensors",".bin",".pt",".pth",".ckpt",".pb",".mlmodel",".mlpackage",".zip",".tar",".tar.gz",".model")
    require(supportedExtensions.any{name.endsWith(it,true)}){"Choose a supported AI artifact: "+supportedExtensions.joinToString()}
    val sourceSize=doc?.length()?:-1L
    require(sourceSize in 1..15_000_000_000L){"Artifact must have a known size between 1 byte and 15 GB."}
    val available=StatFs(context.filesDir.absolutePath).availableBytes
    require(available>=sourceSize+512L*1024L*1024L){"Not enough free storage. Keep at least 512 MiB free after importing the artifact."}
    val modelDir=File(context.filesDir,"models").apply{mkdirs()}
    val safeName=name.replace(Regex("[^A-Za-z0-9._-]"),"_")
    val target=File(modelDir,UUID.randomUUID().toString()+"-"+safeName)
    try{
     withContext(Dispatchers.IO){
      context.contentResolver.openInputStream(uri)?.use{input->target.outputStream().buffered().use{output->
       val buffer=ByteArray(64*1024);var copied=0L
       while(true){val count=input.read(buffer);if(count<0)break;copied+=count;require(copied<=15_000_000_000L){"Artifact exceeds the 15 GB import limit."};output.write(buffer,0,count)}
      }}?:error("Cannot read selected file")
     }
     require(target.length()==sourceSize){"Imported artifact size does not match the source document."}
     db.modelDao().add(LocalModelEntity(uri.toString(),name,context.contentResolver.getType(uri),target.length(),modelPath=target.absolutePath))
     if(name.endsWith(".onnx",true)){
      embeddingPrefs.edit().putString("model_path",target.absolutePath).apply()
      embeddingModelPath=target.absolutePath
      embeddingStatus="ONNX artifact imported. Import its matching WordPiece vocab.txt to enable MiniLM semantic retrieval."
      runtimeMessage="Imported $name. This ONNX model is configured for the embeddings pathway, not chat."
     }else if(name.endsWith(".litertlm",true)){
      runtimeMessage="Imported $name. Tap Load model to activate it."
     }else{
      runtimeMessage="Imported $name. Artifact is stored and checksum-verified only when downloaded with SHA-256; its runtime is not bundled yet, so inference is disabled."
     }
    }catch(error:Throwable){target.delete();throw error}
   }catch(error:Throwable){runtimeMessage="Import failed: "+(error.message?:error.javaClass.simpleName)}
  }
 }
 val selectedAccent=when(accentName){
  "Sage"->Color(0xFF78988A)
  "Sky"->Color(0xFF83AFCB)
  "Lavender"->Color(0xFFA69BCB)
  "Rose"->Color(0xFFC58F9C)
  "Peach"->Color(0xFFD5A184)
  "Butter"->Color(0xFFC8B36F)
  "Seafoam"->Color(0xFF83B8A8)
  "Mint"->Color(0xFF16866A)
  "Blue"->Color(0xFF4968D8)
  "Violet"->Color(0xFF7955C8)
  "Amber"->Color(0xFFB7791F)
  "Graphite"->Color(0xFF4B5563)
  else->runCatching{Color(android.graphics.Color.parseColor(accentName))}.getOrDefault(Color(0xFF78988A))
 }
 val selectedOnAccent=Color(0xFF202A27)
 MaterialTheme(shapes=Shapes(small=RoundedCornerShape(14.dp),medium=RoundedCornerShape(20.dp),large=RoundedCornerShape(26.dp)),colorScheme=if(darkAppearance)
  darkColorScheme(primary=selectedAccent,onPrimary=selectedOnAccent,primaryContainer=selectedAccent.copy(alpha=0.28f),onPrimaryContainer=Color(0xFFE9EDF3),background=Color(0xFF101318),surface=Color(0xFF1A1F27),onSurface=Color(0xFFE9EDF3),secondary=selectedAccent)
 else
  lightColorScheme(primary=selectedAccent,onPrimary=selectedOnAccent,primaryContainer=selectedAccent.copy(alpha=0.14f),onPrimaryContainer=Color(0xFF20242B),background=Color(0xFFF6F7F9),surface=Color.White,onSurface=Color(0xFF20242B),secondary=selectedAccent)){
  Scaffold(containerColor=MaterialTheme.colorScheme.background,topBar={TopAppBar(title={Column{
   Text("MOLECULARIS",style=MaterialTheme.typography.labelMedium,color=MaterialTheme.colorScheme.primary,fontWeight=FontWeight.Bold)
   Text(section.label,style=MaterialTheme.typography.titleLarge,fontWeight=FontWeight.SemiBold)
  }},actions={if(section==Section.CHATS) IconButton(onClick={scope.launch{selectedConversation=db.chatDao().addConversation(ConversationEntity(title="New conversation"))}}){Icon(Icons.Default.Add,"New chat")}},colors=TopAppBarDefaults.topAppBarColors(containerColor=MaterialTheme.colorScheme.background))},
   bottomBar={if(WindowInsets.ime.getBottom(LocalDensity.current)==0) NavigationBar(containerColor=MaterialTheme.colorScheme.surface, tonalElevation=6.dp){
    val primarySections=listOf(Section.CHATS,Section.MODELS,Section.WORKSPACE,Section.LIBRARY)
    primarySections.forEach{item->
     val icon=when(item){Section.CHATS->Icons.Default.ChatBubbleOutline;Section.MODELS->Icons.Default.Memory;Section.WORKSPACE->Icons.Default.FolderOpen;Section.LIBRARY->Icons.Default.MenuBook;else->Icons.Default.MoreHoriz}
     NavigationBarItem(selected=section==item,onClick={section=item;moreNavigationExpanded=false},icon={Icon(icon,item.label)},label={Text(item.label,maxLines=1)})
    }
    NavigationBarItem(
     selected=section==Section.AI_HUB||section==Section.TRAINING||section==Section.ONLINE_AI||section==Section.SETTINGS,
     onClick={moreNavigationExpanded=true},
     icon={
      Box{
       Icon(Icons.Default.MoreHoriz,"More sections")
       DropdownMenu(expanded=moreNavigationExpanded,onDismissRequest={moreNavigationExpanded=false}){
        listOf(Section.AI_HUB,Section.TRAINING,Section.ONLINE_AI,Section.SETTINGS).forEach{item->
         val icon=when(item){Section.LIBRARY->Icons.Default.MenuBook;Section.AI_HUB->Icons.Default.Hub;Section.TRAINING->Icons.Default.Tune;Section.ONLINE_AI->Icons.Default.Cloud;else->Icons.Default.Settings}
         DropdownMenuItem(text={Text(item.label)},leadingIcon={Icon(icon,null)},onClick={section=item;moreNavigationExpanded=false})
        }
       }
      }
     },
     label={Text("More")}
    )
   }}
  ){padding->Box(Modifier.fillMaxSize().padding(padding).imePadding()){
   Image(painter=painterResource(id=org.molecularis.app.R.drawable.molecularis_background),contentDescription=null,contentScale=ContentScale.Crop,modifier=Modifier.fillMaxSize().alpha(if(darkAppearance)0.035f else 0.055f))
   Column(Modifier.fillMaxSize()){
   when(section){
    Section.TEACHING->TeachingStudioScreen(db, voiceAvailable = offlineTtsVoices.isNotEmpty(), localModelAvailable = activeModelPath != null && activeModelName != null, onSpeak = { voiceController.speak(it) }, onGenerateWithLocalModel = { prompt -> runtime.generate(prompt) })
    Section.LIBRARY->BookLibraryScreen(db)
    Section.CHATS->ChatScreen(conversations,conversationId,messages,draft,{draft=it},pendingAttachment?.second,activeModelName,runtimeMessage,loadingModel,sending,voiceListening,
     
     {if(voiceListening)voiceController.stopListening()else if(ContextCompat.checkSelfPermission(context,Manifest.permission.RECORD_AUDIO)==PackageManager.PERMISSION_GRANTED)voiceController.startListening()else microphonePermission.launch(Manifest.permission.RECORD_AUDIO)},
     {text->voiceController.speak(text)} ,
     {attachmentPicker.launch(arrayOf("*/*"))},{pendingAttachment=null},{selectedConversation=it},{id->scope.launch{
      db.chatDao().deleteMessages(id)
      db.chatDao().deleteConversation(id)
      if(selectedConversation==id)selectedConversation=null
     }},onlineEnabled,{
      val text=draft.trim();val target=conversationId;val attachment=pendingAttachment
      if((text.isNotEmpty()||attachment!=null)&&target!=null&&!sending){
       sending=true
       scope.launch{
        try{
         require(!onlineEnabled||attachment==null){"Online AI mode sends text only. Remove the attachment or switch back to offline mode."}
         val userMessageId=db.chatDao().addMessage(MessageEntity(conversationId=target,body=text,role="user",attachmentUri=attachment?.first?.toString(),attachmentName=attachment?.second))
         val extractedAttachment = attachment?.let { selected ->
          val mime=context.contentResolver.getType(selected.first)
          val reader = OfflineDocumentReader(context)
          val extractedText=try {
           reader.read(selected.first,mime,displayName=selected.second)
          } finally { reader.close() }
          val imageFile=selected.second.lowercase().let{name->listOf(".png",".jpg",".jpeg",".webp",".bmp",".gif",".heic",".heif").any(name::endsWith)}
          val isImage=mime?.startsWith("image/")==true||imageFile
          val imageLabels=if(isImage){
           val analyzer=OfflineImageAnalyzer(context)
           try{analyzer.analyze(selected.first)}finally{analyzer.close()}
          }else ""
          val combined=listOf(extractedText,imageLabels).filter{it.isNotBlank()}.joinToString("\n\n").take(100_000)
          if(isImage)combined.ifBlank{"Image attachment: "+selected.second+". Visual pixels can be analyzed when a compatible vision model is enabled."}
          else combined.also{require(it.isNotBlank()){"No readable text was found in this attachment."}}
         }
         if(extractedAttachment!=null) db.chatDao().updateAttachmentText(userMessageId,extractedAttachment)
         if(messages.isEmpty()&&(text.isNotEmpty()||attachment!=null)) db.chatDao().rename(target,(text.ifBlank{attachment?.second.orEmpty()}).take(42))
         if(activeModelPath==null&&!onlineEnabled){
          db.chatDao().addMessage(MessageEntity(conversationId=target,body="No AI model is loaded. Open Models, import a compatible .litertlm file, then tap Load model. Your message and extracted attachment text are saved on this device.",role="assistant"))
         }else if(text.isNotEmpty()||attachment!=null){
          try{
           val question=text.ifBlank{"Please summarize the attached document and extract its key information."}
           val documents=db.chatDao().attachmentMessages(target).asReversed()
           val embeddingModel=embeddingModelPath?.let(::File)
           val embeddingVocab=embeddingVocabPath?.let(::File)
           val semanticExcerpts=if(embeddingModel?.isFile==true&&embeddingVocab?.isFile==true){
            try{
             withContext(Dispatchers.IO){
              val embedder=OnnxWordPieceEmbedder(embeddingModel,embeddingVocab,embeddingModel.name+":"+embeddingModel.length()+":"+embeddingVocab.name+":"+embeddingVocab.length())
              try{
               val rag=PersistentHybridRag(db.knowledgeDao(),embedder,target.toString())
               documents.forEach{document->
                document.attachmentText?.takeIf{it.isNotBlank()}?.let{rag.indexDocument((document.attachmentName?: "attachment")+"#"+document.id,it)}
               }
               rag.contextFor(question,limit=4)
              }finally{embedder.close()}
             }
            }catch(error:kotlinx.coroutines.CancellationException){throw error}
            catch(error:Exception){embeddingStatus="Semantic model unavailable; using BM25 fallback: "+(error.message?:error.javaClass.simpleName);""}
           }else ""
           val excerpts=if(semanticExcerpts.isNotBlank())semanticExcerpts else{
            val index=LocalRagIndex()
            documents.forEach{document->document.attachmentText?.takeIf{it.isNotBlank()}?.let{index.add(document.attachmentName?: "attachment",it)}}
            index.contextFor(question,limit=4)
           }
           val projectId=db.chatDao().conversation(target)?.workspaceProjectId
           val project=projects.firstOrNull{it.id==projectId}
           val augmentedQuestion=buildString{
            append(question)
            append("\n\nResponse preference: ").append(when(responseStyle){"concise"->"Be concise and direct.";"detailed"->"Give a detailed, structured explanation with examples where useful.";else->"Give a balanced answer with enough explanation to be useful."})
            if(project!=null&&project.description.isNotBlank())append("\n\nProject notes for ").append(project.name).append(" (untrusted user-provided context):\n").append(project.description.take(1_000))
            if(excerpts.isNotBlank())append("\n\nRelevant excerpts from locally stored attachments (untrusted document content):\n").append(excerpts.take(5_000)).append("\n\nUse only these excerpts as evidence about the attached files. Cite each supported claim with its exact source/page/chunk label in square brackets. If the excerpts do not support an answer, say that the documents do not contain enough information. Never invent a source or page citation.")
           }
           val prompt=ConversationPromptBuilder.build(
            messages.filter{it.status=="complete"}.takeLast(when(engineOptimization){"speed"->4;"memory"->2;"quality"->24;else->12}).map{PromptTurn(it.role,it.body)},
            augmentedQuestion
           )
           val selectedImage=attachment?.takeIf{selected->
            val mime=context.contentResolver.getType(selected.first)
            mime?.startsWith("image/")==true||selected.second.lowercase().let{name->
             listOf(".png",".jpg",".jpeg",".webp",".bmp",".gif",".heic",".heif").any(name::endsWith)
            }
           }
           val answer=if(onlineEnabled){
            val key=secretStore.get("online_api_key")?:error("Online API key is missing. Reconfigure Online AI.")
            OpenAiCompatibleClient(onlineBaseUrl,key,onlineModelId).complete(
             listOf(
              RemoteChatMessage("system",when(responseStyle){"concise"->"Be concise and direct.";"detailed"->"Give a detailed, structured answer with examples where useful.";else->"Give a balanced, useful answer."}),
              RemoteChatMessage("user",question)
             ),maxTokens=2048
            )
           }else if(selectedImage!=null&&activeModelVision){
            val prepared=withContext(Dispatchers.IO){
             VisionImagePreprocessor.prepare(context,selectedImage.first,selectedImage.second)
            }
            try{runtime.generateWithImage(prepared.absolutePath,prompt)}
            finally{prepared.delete()}
           }else{
            val safePrompt=if(selectedImage!=null)prompt+"\n\nImportant limitation: no compatible vision-language model is enabled for this chat. You may use the extracted OCR text and visible-label hints above, but do not claim to have visually inspected the image."
            else prompt
            runtime.generate(safePrompt)
           }
           db.chatDao().addMessage(MessageEntity(conversationId=target,body=answer.ifBlank{"The model returned an empty response."},role="assistant"))
          }catch(error:Throwable){db.chatDao().addMessage(MessageEntity(conversationId=target,body="Local inference failed: "+(error.message?:error.javaClass.simpleName),role="assistant",status="error"))}
         }
        }catch(error:Throwable){db.chatDao().addMessage(MessageEntity(conversationId=target,body="Attachment processing failed: "+(error.message?:error.javaClass.simpleName),role="assistant",status="error"))}finally{draft="";pendingAttachment=null;sending=false}
       }
      }
     }, onTeach={showTeachingStudio=true}, onLibrary={section=Section.LIBRARY}, onModels={section=Section.MODELS}, onAiHub={section=Section.AI_HUB})
    Section.AI_HUB->CollaborationScreen(models,collaborationPrompt,{collaborationPrompt=it},collaborationStatus,collaborating){
     val prompt=collaborationPrompt.trim()
     if(prompt.isNotBlank()&&!collaborating){
      collaborating=true
      scope.launch{
       val previousPath=activeModelPath
       val previousName=activeModelName
       try{
        if(previousPath!=null){runtime.unload();activeModelPath=null;activeModelName=null}
        val target=conversationId?:db.chatDao().addConversation(ConversationEntity(title="Model collaboration"))
        val provider=LiteRtModelProvider(context)
        val catalog=ModelCatalog()
        models.filter{it.modelPath!=null&&File(it.modelPath).isFile}.distinctBy{it.modelPath}.forEach{model->
         catalog.register(ModelDescriptor(model.uri,model.displayName,provider.providerId,setOf(Capability.CHAT),true,localPath=model.modelPath))
        }
        val result=CollaborationEngine(listOf(provider),catalog).execute(
         InferenceRequest(prompt,target),
         setOf(Capability.CHAT),
         provider
        ){progress->collaborationStatus=progress}
        when(result){
         is CollaborationResult.Success->{
          val report=buildString{
           append("TWO-MODEL REVIEW\n\n")
           result.participants.forEachIndexed{index,answer->
            append("Independent model ").append(index+1).append(": ").append(answer.modelId).append(" (").append(answer.elapsedMs).append(" ms)\n")
            append(answer.text).append("\n\n")
           }
           append("COORDINATOR SYNTHESIS\n").append(result.finalAnswer)
          }
          db.chatDao().addMessage(MessageEntity(conversationId=target,body=report,role="assistant"))
          selectedConversation=target
          section=Section.CHATS
          collaborationStatus="Review completed. The report was saved to this conversation."
         }
         is CollaborationResult.Unavailable->collaborationStatus=result.reason
        }
       }catch(error:Throwable){
        collaborationStatus="Collaboration failed: "+(error.message?:error.javaClass.simpleName)
       }finally{
        if(previousPath!=null&&File(previousPath).isFile){
         try{runtime.load(previousPath);activeModelPath=previousPath;activeModelName=previousName}
         catch(error:Throwable){activeModelPath=null;activeModelName=null;runtimeMessage="Could not restore active model: "+(error.message?:error.javaClass.simpleName)}
        }
        collaborating=false
       }
      }
     }
    }
    Section.MODELS->ModelsScreen(
     models,activeModelPath,activeModelName,runtimeMessage,loadingModel,downloadingModel,downloadProgress,downloadStatus,
     embeddingModelPath?.let(::File)?.isFile==true&&embeddingVocabPath?.let(::File)?.isFile==true,embeddingStatus,
     {embeddingModelPicker.launch(arrayOf("application/octet-stream","*/*"))},
     {embeddingVocabPicker.launch(arrayOf("text/plain","*/*"))},
     {modelPicker.launch(arrayOf("*/*"))},
     {url,checksum,name->
      if(!downloadingModel){
       downloadingModel=true;downloadProgress=0f;downloadStatus="Connecting to HTTPS model host…"
       modelDownloadJob=scope.launch{
        try{
         val result=VerifiedModelDownloader(context).download(url,checksum,name){downloaded,total->
          downloadProgress=if(total!=null&&total>0)(downloaded.toFloat()/total).coerceIn(0f,1f)else 0f
          downloadStatus=if(total!=null)"Downloaded "+formatBytes(downloaded)+" / "+formatBytes(total)else "Downloaded "+formatBytes(downloaded)
         }
         db.modelDao().add(LocalModelEntity("sha256:"+result.sha256,name,"application/octet-stream",result.bytes,modelPath=result.file.absolutePath))
         downloadStatus="Verified SHA-256 "+result.sha256.take(16)+"…"
         if(name.endsWith(".onnx",true)){
          embeddingPrefs.edit().putString("model_path",result.file.absolutePath).apply()
          embeddingModelPath=result.file.absolutePath
          embeddingStatus="ONNX artifact downloaded and verified. Import its matching vocab.txt to enable MiniLM semantic retrieval."
          runtimeMessage="Downloaded and verified "+name+". Configured as an ONNX embedding artifact, not a chat model."
         }else runtimeMessage="Downloaded and verified "+name+". Tap Load model only if its compatible runtime is bundled."
        }catch(cancelled:CancellationException){throw cancelled}
        catch(error:Exception){downloadStatus="Download failed: "+(error.message?:error.javaClass.simpleName)}
        finally{downloadingModel=false;modelDownloadJob=null}
       }
      }
     },
     {modelDownloadJob?.cancel();downloadStatus="Download cancelled. Partial bytes remain private and can be resumed."},
     {model->

     if(model.modelPath!=null){loadingModel=true;scope.launch{
      try{val visionEnabled=model.modelPath==visionModelPath;runtime.load(model.modelPath,enableVision=visionEnabled);activeModelPath=model.modelPath;activeModelPrefs.edit().putString("path",model.modelPath).apply();activeModelName=model.displayName;activeModelVision=visionEnabled;runtimeMessage=if(visionEnabled)"Loaded "+model.displayName+" with local image input enabled." else "Loaded "+model.displayName+". Text chat is ready offline."}
      catch(error:Throwable){activeModelPath=null;activeModelPrefs.edit().remove("path").apply();activeModelName=null;activeModelVision=false;runtimeMessage="Could not load model: "+(error.message?:error.javaClass.simpleName)}
      finally{loadingModel=false}
     }}
    },{model->scope.launch{if(activeModelPath==model.modelPath){runtime.unload();activeModelPath=null;activeModelPrefs.edit().remove("path").apply();activeModelName=null;activeModelVision=false};if(visionModelPath==model.modelPath){visionPrefs.edit().remove("vision_model_path").apply();visionModelPath=null};model.modelPath?.let{File(it).delete()};db.modelDao().remove(model.uri)}},visionModelPath,{path->
      val next=if(visionModelPath==path)null else path
      visionPrefs.edit().putString("vision_model_path",next).apply()
      visionModelPath=next
      if(activeModelPath==path){scope.launch{runtime.unload();activeModelPath=null;activeModelPrefs.edit().remove("path").apply();activeModelName=null;activeModelVision=false;runtimeMessage="Vision setting changed. Reload this model to apply it."}}
     }, { entry, file ->
      scope.launch {
       db.modelDao().add(LocalModelEntity("catalog:"+entry.id+":"+entry.version,entry.name,"application/octet-stream",file.length(),modelPath=file.absolutePath))
       if(entry.format=="onnx" && entry.capabilities.contains(org.molecularis.app.features.ModelCapability.EMBEDDING)){
        embeddingPrefs.edit().putString("model_path",file.absolutePath).apply()
        embeddingModelPath=file.absolutePath
        val vocab=embeddingVocabPath?.let(::File)
        if(vocab?.isFile==true){
         embeddingStatus="Validating catalog ONNX embedding model…"
         try{
          withContext(Dispatchers.IO){OnnxWordPieceEmbedder(file,vocab,entry.id+":"+file.length()+":"+vocab.length()).use{it.embed("Molecularis catalog embedding validation")}}
          embeddingStatus="Semantic retrieval ready · "+entry.name
         }catch(error:Throwable){embeddingStatus="Catalog ONNX model needs a compatible vocab or tensor layout: "+(error.message?:error.javaClass.simpleName)}
        }else embeddingStatus="ONNX embedding model installed. Import its matching vocab.txt to enable semantic retrieval."
       }
      }
     })
    Section.TRAINING->TrainingLabScreen(
     datasetName,datasetReport,datasetStatus,datasetBusy,trainingJob,trainingStatus,trainingBusy,
     {datasetPicker.launch(arrayOf("*/*"))},
     {datasetExport.launch("molecularis-cleaned-dataset.jsonl")},
     {serverUrl,apiKey,baseModel,method,epochs->
      if(!trainingBusy){
       trainingBusy=true;trainingStatus="Preparing secure upload…";trainingJob=null
       scope.launch{
        try{
         val report=datasetReport?:error("Import a valid JSONL dataset first.")
         val invalid=report.invalidLines.toSet()
         val clean=datasetContent.lineSequence().mapIndexedNotNull{index,line->if(line.isNotBlank()&&index+1 !in invalid)line else null}.joinToString("\n")
         val client=TrainingApiClient(serverUrl,apiKey)
         val datasetId=client.uploadDataset(datasetName.ifBlank{"molecularis-dataset.jsonl"},clean)
         trainingStatus="Dataset uploaded to your configured workstation. Creating job…"
         var job=client.startJob(datasetId,baseModel,method,epochs)
         trainingJob=job;trainingStatus=job.message
         while(job.state=="queued"||job.state=="running"){
          delay(3_000)
          job=client.getJob(job.id)
          trainingJob=job
          trainingStatus=job.message
         }
         trainingStatus=job.message
        }catch(error:Throwable){trainingStatus="Training request failed: "+(error.message?:error.javaClass.simpleName)}
        finally{trainingBusy=false}
       }
      }
     },
     {serverUrl,apiKey,jobId->
      scope.launch{
       try{
        val job=TrainingApiClient(serverUrl,apiKey).cancelJob(jobId)
        trainingJob=job;trainingStatus=job.message
       }catch(error:Throwable){trainingStatus="Cancellation failed: "+(error.message?:error.javaClass.simpleName)}
      }
     }
    )
    Section.WORKSPACE->WorkspaceScreen(projects,{showNewProject=true},{project->
     scope.launch{
      val existing=db.chatDao().latestProjectConversation(project.id)
      val id=existing?.id?:db.chatDao().addConversation(ConversationEntity(title=project.name,workspaceProjectId=project.id))
      selectedConversation=id
      section=Section.CHATS
     }
    },{id->scope.launch{db.workspaceDao().delete(id)}})
    Section.ONLINE_AI->OnlineAiScreen(
     onlineBaseUrl,onlineModelId,onlineHasKey,onlineEnabled,onlineStatus,
     {url,model,key->
      try{
       require(url.startsWith("https://",true)){"Use an HTTPS provider URL."}
       require(model.isNotBlank()){"Enter the provider's exact model ID."}
       if(key.isNotBlank())require(key.length>=8){"Enter a valid API key."}
       val effectiveKey=key.takeIf{it.isNotBlank()}?:secretStore.get("online_api_key").orEmpty()
       require(effectiveKey.length>=8){"Enter an API key before saving the provider."}
       OpenAiCompatibleClient(url,effectiveKey,model)
       onlinePrefs.edit().putString("base_url",url.trim()).putString("model_id",model.trim()).apply()
       if(key.isNotBlank())secretStore.put("online_api_key",key.trim())
       onlineBaseUrl=url.trim();onlineModelId=model.trim();onlineHasKey=true
       onlineStatus="Provider configuration saved securely. Test the connection before enabling online mode."
      }catch(error:Throwable){onlineStatus="Could not save provider: "+(error.message?:error.javaClass.simpleName)}
     },
     {enabled->
      onlineEnabled=enabled
      onlinePrefs.edit().putBoolean("enabled",enabled).apply()
      onlineStatus=if(enabled)"ONLINE MODE ENABLED. Only the current text prompt is sent; local history and attachments are not uploaded." else "Online mode disabled. Chat will use the local model."
     },
     {
      secretStore.remove("online_api_key");onlineHasKey=false;onlineEnabled=false
      onlinePrefs.edit().putBoolean("enabled",false).apply()
      onlineStatus="API key removed and online mode disabled."
     },
     {
      scope.launch{
       onlineStatus="Testing provider connection…"
       try{
        val key=secretStore.get("online_api_key")?:error("Save an API key first.")
        val answer=OpenAiCompatibleClient(onlineBaseUrl,key,onlineModelId).complete(listOf(RemoteChatMessage("user","Reply with OK.")),maxTokens=16)
        onlineStatus="Connection successful. Provider replied: "+answer.take(120)
       }catch(error:Throwable){onlineStatus="Provider test failed: "+(error.message?:error.javaClass.simpleName)}
      }
     }
    )
    Section.SETTINGS->SettingsScreen(
     speechLanguageTag,ttsVoiceName,offlineTtsVoices,recognitionLanguages,speechStatus,responseStyle,darkAppearance,accentName,engineOptimization,
     {style->responseStyle=style;personalizationPrefs.edit().putString("response_style",style).apply()},
     {name->accentName=name;personalizationPrefs.edit().putString("accent_name",name).apply()},
     {enabled->darkAppearance=enabled;personalizationPrefs.edit().putBoolean("dark_appearance",enabled).apply()},
     {mode->engineOptimization=mode;enginePrefs.edit().putString("optimization",mode).apply()},
     {tag->try{
      val normalized=OfflineVoiceController.normalizeLanguageTag(tag)
      speechLanguageTag=normalized
      speechPrefs.edit().putString("language_tag",normalized).apply()
      voiceController.setLanguageTag(normalized)
      ttsVoiceName=voiceController.selectedTtsVoiceName()
      speechPrefs.edit().putString("tts_voice_name",ttsVoiceName).apply()
      speechStatus="Language set to $normalized. Check on-device language support."
     }catch(error:Throwable){speechStatus=error.message?: "Invalid language tag"}},
     {speechStatus="Checking installed and downloadable on-device language packs…";voiceController.checkRecognitionSupport{support->recognitionLanguages=support;speechStatus="Language support refreshed for $speechLanguageTag."}},
     {voiceController.downloadRecognitionLanguage{speechStatus=it}},
     {name->voiceController.setTtsVoice(name);ttsVoiceName=name;speechPrefs.edit().putString("tts_voice_name",name).apply();speechStatus="Offline voice selected."},
     {voiceController.speak("Molecularis offline speech is ready.")}
    )
   }
  }}}
 }
 if(showTeachingStudio) Dialog(onDismissRequest={showTeachingStudio=false},properties=DialogProperties(usePlatformDefaultWidth=false)) {
  Surface(Modifier.fillMaxWidth().fillMaxHeight(0.96f),shape=RoundedCornerShape(24.dp),color=MaterialTheme.colorScheme.background) {
   Column(Modifier.fillMaxSize()) {
    Row(Modifier.fillMaxWidth().padding(horizontal=12.dp,vertical=6.dp),verticalAlignment=Alignment.CenterVertically) {
     Text("Teach a lesson",modifier=Modifier.weight(1f),style=MaterialTheme.typography.titleLarge,fontWeight=FontWeight.SemiBold)
     IconButton(onClick={showTeachingStudio=false}) { Icon(Icons.Default.Close,"Close teaching studio") }
    }
    HorizontalDivider()
    TeachingStudioScreen(db,voiceAvailable=offlineTtsVoices.isNotEmpty(),localModelAvailable=activeModelPath!=null&&activeModelName!=null,onSpeak={voiceController.speak(it)},onGenerateWithLocalModel={prompt->runtime.generate(prompt)})
   }
  }
 }
 if(showNewProject) AlertDialog(onDismissRequest={showNewProject=false},title={Text("Create project")},text={Column(verticalArrangement=Arrangement.spacedBy(8.dp)){
  OutlinedTextField(projectName,{projectName=it},label={Text("Project name")},singleLine=true)
  OutlinedTextField(projectDescription,{projectDescription=it},label={Text("Description")},minLines=2)
 }},confirmButton={TextButton(onClick={
  if(projectName.isNotBlank()) scope.launch{db.workspaceDao().add(WorkspaceProjectEntity(name=projectName.trim(),description=projectDescription.trim()));projectName="";projectDescription="";showNewProject=false}
 }){Text("Create")}},dismissButton={TextButton(onClick={showNewProject=false}){Text("Cancel")}})
}


@Composable private fun OnlineAiScreen(
 baseUrl:String,
 modelId:String,
 hasKey:Boolean,
 enabled:Boolean,
 status:String,
 onSave:(String,String,String)->Unit,
 onToggle:(Boolean)->Unit,
 onClearKey:()->Unit,
 onTest:()->Unit
){
 var urlDraft by remember(baseUrl){mutableStateOf(baseUrl)}
 var modelDraft by remember(modelId){mutableStateOf(modelId)}
 var keyDraft by remember{mutableStateOf("")}
 Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),verticalArrangement=Arrangement.spacedBy(10.dp)){
  Text("Online AI providers",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold)
  Text("Connect an OpenAI-compatible endpoint. This supports providers that expose the Chat Completions API, including provider-hosted free tiers where available.",color=Muted)
  Card{Column(Modifier.padding(14.dp),verticalArrangement=Arrangement.spacedBy(8.dp)){
   Text("Privacy boundary",fontWeight=FontWeight.SemiBold)
   Text("When Online mode is enabled, Molecularis sends only the current text prompt and selected model ID. It does NOT send previous chat messages, project notes, local documents, images or attachments. Requests go to the endpoint you configure. Provider pricing, free quotas and data retention are controlled by that provider.",style=MaterialTheme.typography.bodySmall,color=Muted)
  }}
  OutlinedTextField(urlDraft,{urlDraft=it},modifier=Modifier.fillMaxWidth(),label={Text("Provider base URL (HTTPS)")},placeholder={Text("https://api.example.com")},singleLine=true)
  OutlinedTextField(modelDraft,{modelDraft=it},modifier=Modifier.fillMaxWidth(),label={Text("Exact model ID")},placeholder={Text("provider/model-name")},singleLine=true)
  OutlinedTextField(keyDraft,{keyDraft=it},modifier=Modifier.fillMaxWidth(),label={Text(if(hasKey)"Replace API key (leave blank to keep saved key)" else "API key")},visualTransformation=PasswordVisualTransformation(),singleLine=true)
  Button(onClick={onSave(urlDraft.trim(),modelDraft.trim(),keyDraft);keyDraft=""},modifier=Modifier.fillMaxWidth(),enabled=urlDraft.startsWith("https://",true)&&modelDraft.isNotBlank()&&(keyDraft.length>=8||hasKey)){
   Icon(Icons.Default.Save,null);Spacer(Modifier.width(8.dp));Text("Save provider and encrypted API key")
  }
  Text(if(hasKey)"An API key is saved encrypted using Android Keystore." else "No API key saved.",style=MaterialTheme.typography.bodySmall,color=Muted)
  OutlinedButton(onClick=onTest,modifier=Modifier.fillMaxWidth(),enabled=hasKey&&baseUrl.startsWith("https://")&&modelId.isNotBlank()){Icon(Icons.Default.WifiTethering,null);Spacer(Modifier.width(8.dp));Text("Test provider connection")}
  Row(verticalAlignment=Alignment.CenterVertically){
   Column(Modifier.weight(1f)){
    Text("Use online inference",fontWeight=FontWeight.SemiBold)
    Text(if(enabled)"STATUS · ON — remote inference is active" else "STATUS · OFF — all chat stays on-device",style=MaterialTheme.typography.bodySmall,color=if(enabled)MaterialTheme.colorScheme.primary else Muted)
   }
   Switch(checked=enabled,onCheckedChange=onToggle,enabled=hasKey&&baseUrl.startsWith("https://")&&modelId.isNotBlank()||enabled)
  }
  if(hasKey)TextButton(onClick=onClearKey){Text("Remove saved API key and disable online mode")}
  Text(status,color=if(status.contains("failed",true)||status.contains("could not",true))Color(0xFFB45335) else MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
 }
}

@Composable private fun ChatScreen(conversations:List<ConversationEntity>,selectedId:Long?,messages:List<MessageEntity>,draft:String,onDraftChange:(String)->Unit,attachmentName:String?,activeModelName:String?,runtimeMessage:String,loading:Boolean,sending:Boolean,voiceListening:Boolean,onVoice:()->Unit,onSpeak:(String)->Unit,onAttach:()->Unit,onClearAttachment:()->Unit,onSelect:(Long)->Unit,onDelete:(Long)->Unit,onlineEnabled:Boolean,onSend:()->Unit,onTeach:()->Unit,onLibrary:()->Unit,onModels:()->Unit,onAiHub:()->Unit){
 var pendingDelete by remember{mutableStateOf<Long?>(null)}
 var historyExpanded by remember{mutableStateOf(false)}
 var actionsExpanded by remember{mutableStateOf(false)}
 val messageListState=rememberLazyListState()
 LaunchedEffect(selectedId,messages.size){if(messages.isNotEmpty())messageListState.animateScrollToItem(messages.lastIndex)}
 Column(Modifier.fillMaxSize().padding(horizontal=16.dp)){
  if(conversations.isNotEmpty()) Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically){
   Box(Modifier.weight(1f)){
    OutlinedButton(onClick={historyExpanded=true},modifier=Modifier.fillMaxWidth()){
     Icon(Icons.Default.Forum,null);Spacer(Modifier.width(8.dp))
     Text(conversations.firstOrNull{it.id==selectedId}?.title?: "Choose conversation",maxLines=1,overflow=TextOverflow.Ellipsis,modifier=Modifier.weight(1f))
     Icon(Icons.Default.ExpandMore,null)
    }
    DropdownMenu(expanded=historyExpanded,onDismissRequest={historyExpanded=false}){
     conversations.forEach{chat->DropdownMenuItem(
      text={Text(chat.title,maxLines=1,overflow=TextOverflow.Ellipsis)},
      leadingIcon={Icon(if(chat.id==selectedId)Icons.Default.CheckCircle else Icons.Default.ChatBubbleOutline,null)},
      trailingIcon={IconButton(onClick={pendingDelete=chat.id;historyExpanded=false}){Icon(Icons.Default.DeleteOutline,"Delete conversation")}},
      onClick={onSelect(chat.id);historyExpanded=false}
     )}
    }
   }
  }
  if(pendingDelete!=null) AlertDialog(onDismissRequest={pendingDelete=null},title={Text("Delete conversation?")},text={Text("This permanently deletes this chat and its messages from this device.")},confirmButton={TextButton(onClick={pendingDelete?.let(onDelete);pendingDelete=null}){Text("Delete")}},dismissButton={TextButton(onClick={pendingDelete=null}){Text("Cancel")}})
  if(messages.isEmpty()) Column(Modifier.weight(1f).fillMaxWidth(),horizontalAlignment=Alignment.CenterHorizontally,verticalArrangement=Arrangement.Center){
   Box(Modifier.size(68.dp).background(Color(0xFFDCEBE3),CircleShape),contentAlignment=Alignment.Center){Icon(Icons.Default.AutoAwesome,null,tint=MaterialTheme.colorScheme.primary,modifier=Modifier.size(32.dp))}
   Spacer(Modifier.height(18.dp));Text("A quieter kind of AI.",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold)
   Text("Private conversations. On-device intelligence.",color=Muted)
   Text(runtimeMessage,style=MaterialTheme.typography.bodySmall,color=Muted)
  }else LazyColumn(state=messageListState,modifier=Modifier.weight(1f).fillMaxWidth(),contentPadding=PaddingValues(vertical=12.dp),verticalArrangement=Arrangement.spacedBy(10.dp)){
   items(messages,key={it.id}){message->val mine=message.role=="user"
    Row(Modifier.fillMaxWidth(),horizontalArrangement=if(mine)Arrangement.End else Arrangement.Start){
     Surface(color=if(mine)MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,shape=RoundedCornerShape(if(mine)22.dp else 16.dp),modifier=Modifier.widthIn(max=340.dp)){
      Column(Modifier.padding(14.dp)){
       if(message.body.isNotBlank()) Text(message.body,color=MaterialTheme.colorScheme.onSurface)
       if(!mine&&message.body.isNotBlank()) Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.End){IconButton(onClick={onSpeak(message.body)}){Icon(Icons.Default.VolumeUp,"Read response aloud",tint=MaterialTheme.colorScheme.primary)}}
       if(message.attachmentName!=null){Row(verticalAlignment=Alignment.CenterVertically){Icon(Icons.Default.AttachFile,null,tint=MaterialTheme.colorScheme.primary,modifier=Modifier.size(16.dp));Text(message.attachmentName,color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.labelMedium)}}
       Text(if(mine)"You" else "Molecularis",style=MaterialTheme.typography.labelSmall,color=MaterialTheme.colorScheme.primary)
      }
     }
    }
   }
  }
  if(attachmentName!=null) Row(verticalAlignment=Alignment.CenterVertically,modifier=Modifier.fillMaxWidth().padding(bottom=6.dp)){
   Icon(Icons.Default.AttachFile,null,tint=MaterialTheme.colorScheme.primary);Text(attachmentName,Modifier.weight(1f),maxLines=1,overflow=TextOverflow.Ellipsis)
   IconButton(onClick=onClearAttachment){Icon(Icons.Default.Close,"Remove attachment")}
  }
  Surface(color=MaterialTheme.colorScheme.surface,shape=RoundedCornerShape(26.dp),shadowElevation=3.dp){
   Row(Modifier.padding(start=6.dp,end=8.dp,top=4.dp,bottom=4.dp),verticalAlignment=Alignment.CenterVertically){
    IconButton(onClick={actionsExpanded=true}){Icon(Icons.Default.AttachFile,"Teaching tools and attachments",tint=MaterialTheme.colorScheme.primary)}
    IconButton(onClick=onVoice,enabled=!sending){Icon(if(voiceListening)Icons.Default.MicOff else Icons.Default.Mic,if(voiceListening)"Listening" else "Speak message",tint=if(voiceListening)MaterialTheme.colorScheme.primary else Muted)}
    TextField(draft,onDraftChange,Modifier.weight(1f),placeholder={Text("Message privately…")},maxLines=5,enabled=!sending,colors=TextFieldDefaults.colors(focusedContainerColor=Color.Transparent,unfocusedContainerColor=Color.Transparent,focusedIndicatorColor=Color.Transparent,unfocusedIndicatorColor=Color.Transparent))
    IconButton(onClick=onSend,enabled=!sending&&(draft.isNotBlank()||attachmentName!=null)){if(sending)CircularProgressIndicator(Modifier.size(20.dp),strokeWidth=2.dp)else Icon(Icons.Default.Send,"Send",tint=MaterialTheme.colorScheme.primary)}
   }
  }
  Text((if(onlineEnabled)"Online · remote provider" else "On-device · "+(activeModelName?: "No model loaded")),style=MaterialTheme.typography.labelSmall,color=MaterialTheme.colorScheme.primary,modifier=Modifier.padding(top=6.dp,bottom=8.dp))
 }
 if(actionsExpanded) ModalBottomSheet(onDismissRequest={actionsExpanded=false}) {
  Column(Modifier.fillMaxWidth().navigationBarsPadding().padding(horizontal=20.dp,vertical=12.dp),verticalArrangement=Arrangement.spacedBy(10.dp)) {
   Text("Molecularis tools",style=MaterialTheme.typography.titleLarge,fontWeight=FontWeight.SemiBold)
   Text("Keep chatting here. Open a focused tool only when you need it.",style=MaterialTheme.typography.bodySmall,color=Muted)
   Button(onClick={actionsExpanded=false;onTeach()},modifier=Modifier.fillMaxWidth()) { Icon(Icons.Default.School,null);Spacer(Modifier.width(10.dp));Text("Teach a lesson") }
   OutlinedButton(onClick={actionsExpanded=false;onAttach()},modifier=Modifier.fillMaxWidth()) { Icon(Icons.Default.AttachFile,null);Spacer(Modifier.width(10.dp));Text("Attach a document or image") }
   OutlinedButton(onClick={actionsExpanded=false;onLibrary()},modifier=Modifier.fillMaxWidth()) { Icon(Icons.Default.MenuBook,null);Spacer(Modifier.width(10.dp));Text("Textbook library") }
   Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(10.dp)) {
    OutlinedButton(onClick={actionsExpanded=false;onModels()},modifier=Modifier.weight(1f)) { Icon(Icons.Default.Memory,null);Spacer(Modifier.width(6.dp));Text("Models") }
    OutlinedButton(onClick={actionsExpanded=false;onAiHub()},modifier=Modifier.weight(1f)) { Icon(Icons.Default.Hub,null);Spacer(Modifier.width(6.dp));Text("AI tools") }
   }
  }
 }
}

@Composable private fun ModelsScreen(models:List<LocalModelEntity>,activePath:String?,activeName:String?,status:String,loading:Boolean,downloading:Boolean,downloadProgress:Float,downloadStatus:String,embeddingReady:Boolean,embeddingStatus:String,onImportEmbeddingModel:()->Unit,onImportEmbeddingVocab:()->Unit,onImport:()->Unit,onDownload:(String,String,String)->Unit,onCancelDownload:()->Unit,onLoad:(LocalModelEntity)->Unit,onRemove:(LocalModelEntity)->Unit,visionModelPath:String?,onEnableVision:(String)->Unit,onCatalogInstalled:(org.molecularis.app.features.ModelCatalogEntry,File)->Unit){
 var showCatalog by remember { mutableStateOf(false) }
 Column(Modifier.fillMaxSize().padding(16.dp)){
  Card(colors=CardDefaults.cardColors(containerColor=MaterialTheme.colorScheme.primaryContainer.copy(alpha=0.42f)),modifier=Modifier.fillMaxWidth()){Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(5.dp)){Text("MODEL LIBRARY",style=MaterialTheme.typography.labelMedium,color=MaterialTheme.colorScheme.primary,fontWeight=FontWeight.Bold);Text("Manage your local models",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold);Text("Import, verify, activate and organize AI files. Files stay in app-private storage.",color=MaterialTheme.colorScheme.onSurfaceVariant)}}
  Card{Column(Modifier.padding(12.dp),verticalArrangement=Arrangement.spacedBy(4.dp)){
   Text("Runtime availability",fontWeight=FontWeight.SemiBold)
   Text("Ready: LiteRT-LM chat/vision and ONNX MiniLM embeddings (with matching vocab.txt). GGUF/llama.cpp, diffusion image generation and dedicated Whisper/Sherpa engines are not bundled yet; their downloads are stored but cannot be loaded until the runtime is added.",style=MaterialTheme.typography.bodySmall,color=Muted)
  }}
  OutlinedButton(onClick={showCatalog=true},modifier=Modifier.fillMaxWidth()){Icon(Icons.Default.Verified,null);Spacer(Modifier.width(8.dp));Text("Browse verified model catalog")}
  if(showCatalog) AlertDialog(onDismissRequest={showCatalog=false},title={Text("Verified model catalog")},text={Column(Modifier.heightIn(max=560.dp).verticalScroll(rememberScrollState())){CatalogLibraryPanel(onCatalogInstalled)}},confirmButton={TextButton(onClick={showCatalog=false}){Text("Close")}})
  Spacer(Modifier.height(14.dp));Button(onClick=onImport,modifier=Modifier.fillMaxWidth(),enabled=!downloading){Icon(Icons.Default.FileOpen,null);Spacer(Modifier.width(8.dp));Text("Import AI model artifact")}
  Spacer(Modifier.height(18.dp))
  Text("Semantic document search",style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
  Text("Optional local embedding model. Use a MiniLM-compatible ONNX export with input_ids and attention_mask (int64), plus its matching WordPiece vocab.txt. Files stay on this device.",color=Muted,style=MaterialTheme.typography.bodySmall)
  OutlinedButton(onClick=onImportEmbeddingModel,modifier=Modifier.fillMaxWidth(),enabled=!downloading){Icon(Icons.Default.FileOpen,null);Spacer(Modifier.width(8.dp));Text("Import embedding model (.onnx)")}
  OutlinedButton(onClick=onImportEmbeddingVocab,modifier=Modifier.fillMaxWidth(),enabled=!downloading){Icon(Icons.Default.Description,null);Spacer(Modifier.width(8.dp));Text("Import matching vocab.txt")}
  Text(if(embeddingReady)"SEMANTIC RETRIEVAL CONFIGURED" else "BM25 fallback active",color=if(embeddingReady)MaterialTheme.colorScheme.primary else Muted,style=MaterialTheme.typography.labelSmall,fontWeight=FontWeight.Bold)
  Text(embeddingStatus,color=Muted,style=MaterialTheme.typography.bodySmall)

  var downloadUrl by remember{mutableStateOf("")}
  var downloadSha by remember{mutableStateOf("")}
  var downloadName by remember{mutableStateOf("model.litertlm")}
  Spacer(Modifier.height(16.dp))
  Text("Download and verify",style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
  Text("Import or download LiteRT-LM, GGUF, ONNX, TFLite, Task, Safetensors, PyTorch, TensorFlow, Core ML and archive artifacts. SHA-256 is mandatory for downloads. Stored formats only run when their matching runtime is installed.",color=Muted,style=MaterialTheme.typography.bodySmall)
  OutlinedTextField(downloadUrl,{downloadUrl=it},modifier=Modifier.fillMaxWidth(),label={Text("HTTPS download URL")},singleLine=true,enabled=!downloading)
  OutlinedTextField(downloadSha,{downloadSha=it},modifier=Modifier.fillMaxWidth(),label={Text("SHA-256 checksum (64 hex characters)")},singleLine=true,enabled=!downloading)
  OutlinedTextField(downloadName,{downloadName=it},modifier=Modifier.fillMaxWidth(),label={Text("Filename with supported extension")},singleLine=true,enabled=!downloading)
  Button(onClick={onDownload(downloadUrl.trim(),downloadSha.trim(),downloadName.trim())},modifier=Modifier.fillMaxWidth(),enabled=!downloading&&downloadUrl.startsWith("https://")&&downloadSha.matches(Regex("[A-Fa-f0-9]{64}"))&&downloadName.matches(Regex("(?i).+\\.(litertlm|gguf|ggml|onnx|tflite|task|safetensors|bin|pt|pth|ckpt|pb|mlmodel|mlpackage|zip|tar(?:\\.gz)?|model)"))){if(downloading)CircularProgressIndicator(Modifier.size(18.dp),strokeWidth=2.dp)else Icon(Icons.Default.Download,null);Spacer(Modifier.width(8.dp));Text(if(downloading)"Downloading…" else "Download and verify")}
  if(downloading&&downloadProgress>0f)LinearProgressIndicator(progress={downloadProgress},modifier=Modifier.fillMaxWidth())
  if(downloading)OutlinedButton(onClick=onCancelDownload,modifier=Modifier.fillMaxWidth()){
   Icon(Icons.Default.Close,null);Spacer(Modifier.width(8.dp));Text("Cancel download")
  }
  if(downloadStatus.isNotBlank())Text(downloadStatus,color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
  Spacer(Modifier.height(10.dp));Text(status,color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
  if(loading)LinearProgressIndicator(Modifier.fillMaxWidth())
  Spacer(Modifier.height(10.dp))
  if(models.isEmpty())EmptyState("No model imported","Choose a compatible LiteRT-LM .litertlm file. A small model is best for phones.")
  LazyColumn(Modifier.weight(1f),verticalArrangement=Arrangement.spacedBy(8.dp)){items(models,key={it.uri}){model->
   val canLoad=model.modelPath?.endsWith(".litertlm",true)==true
   val isOnnx=model.modelPath?.endsWith(".onnx",true)==true
   Card{Column(Modifier.fillMaxWidth().padding(14.dp)){
   Text(model.displayName,fontWeight=FontWeight.SemiBold,maxLines=2,overflow=TextOverflow.Ellipsis)
   Text(formatBytes(model.sizeBytes),color=Muted,style=MaterialTheme.typography.labelSmall)
   if(isOnnx)Text("ONNX artifact. Embedding models need their matching vocab.txt and are used by semantic retrieval, not the chat engine.",color=Muted,style=MaterialTheme.typography.bodySmall)
   else if(!canLoad)Text("Artifact imported. Its declared runtime is not bundled in this build, so loading is disabled rather than sent to an incompatible engine.",color=Muted,style=MaterialTheme.typography.bodySmall)
   Text("Vision input is available only for compatible multimodal .litertlm models. Enable this only when the model publisher confirms image support.",color=Muted,style=MaterialTheme.typography.bodySmall)
   Row(verticalAlignment=Alignment.CenterVertically){
    if(activePath==model.modelPath)Text("ACTIVE · "+activeName,color=MaterialTheme.colorScheme.primary,modifier=Modifier.weight(1f),style=MaterialTheme.typography.labelSmall) else Spacer(Modifier.weight(1f))
    FilterChip(selected=model.modelPath==visionModelPath,onClick={model.modelPath?.let(onEnableVision)?:Unit},enabled=model.modelPath!=null,label={Text(if(model.modelPath==visionModelPath)"Vision · ON" else "Vision · OFF")},leadingIcon={Icon(if(model.modelPath==visionModelPath)Icons.Default.Visibility else Icons.Default.VisibilityOff,null)})
    TextButton(onClick={onRemove(model)}){Text("Remove")}
    Button(onClick={onLoad(model)},enabled=!loading&&canLoad){Text(if(activePath==model.modelPath)"Reload" else if(canLoad)"Load model" else if(isOnnx)"Embedding artifact" else "Runtime unavailable")}
   }
  }} }}
 }
}
@Composable private fun CollaborationScreen(
 models:List<LocalModelEntity>,
 prompt:String,
 onPrompt:(String)->Unit,
 status:String,
 running:Boolean,
 onRun:()->Unit
){
 val available=models.filter{it.modelPath!=null}.distinctBy{it.modelPath}
 Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),verticalArrangement=Arrangement.spacedBy(12.dp)){
  Card(colors=CardDefaults.cardColors(containerColor=MaterialTheme.colorScheme.primaryContainer.copy(alpha=0.48f)),modifier=Modifier.fillMaxWidth()) { Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(6.dp)) {
   Text("AI HUB",style=MaterialTheme.typography.labelMedium,color=MaterialTheme.colorScheme.primary,fontWeight=FontWeight.Bold)
   Text("Your private AI toolkit",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold)
   Text("Local capabilities, model tools and workflows in one place.",color=MaterialTheme.colorScheme.onSurfaceVariant)
   Text("Available local models · "+available.size,style=MaterialTheme.typography.labelLarge,color=MaterialTheme.colorScheme.primary)
  } }
  Text("TOOLS & WORKFLOWS",style=MaterialTheme.typography.labelMedium,color=Muted,fontWeight=FontWeight.Bold)
  Row(horizontalArrangement=Arrangement.spacedBy(8.dp)) { HubCapabilityCard("Document AI","PDF · DOCX · TXT","Local extraction",Icons.Default.Description,Modifier.weight(1f)); HubCapabilityCard("Image understanding","OCR · labels · vision","Vision model optional",Icons.Default.Image,Modifier.weight(1f)) }
  Row(horizontalArrangement=Arrangement.spacedBy(8.dp)) { HubCapabilityCard("Voice","Speech input · TTS","Device language packs",Icons.Default.RecordVoiceOver,Modifier.weight(1f)); HubCapabilityCard("Knowledge search","BM25 · ONNX vectors","Local retrieval",Icons.Default.Search,Modifier.weight(1f)) }
  Text("MODEL COLLABORATION",style=MaterialTheme.typography.labelMedium,color=Muted,fontWeight=FontWeight.Bold)
  Text("Run two different local models one at a time, then compare their answers. Sequential execution helps reduce peak RAM use.",color=Muted,style=MaterialTheme.typography.bodySmall)
  available.forEach{model->Text("• "+model.displayName,style=MaterialTheme.typography.bodySmall,color=Muted)}
  OutlinedTextField(prompt,onPrompt,modifier=Modifier.fillMaxWidth(),label={Text("Task for both models")},minLines=3,maxLines=6,enabled=!running)
  Button(onClick=onRun,modifier=Modifier.fillMaxWidth(),enabled=!running&&prompt.isNotBlank()&&available.size>=2){
   if(running)CircularProgressIndicator(Modifier.size(18.dp),strokeWidth=2.dp) else Icon(Icons.Default.Hub,null)
   Spacer(Modifier.width(8.dp));Text(if(running)"Reviewing…" else "Run two-model review")
  }
  Text(status,color=if(running)MaterialTheme.colorScheme.primary else Muted,style=MaterialTheme.typography.bodySmall)
  if(available.size<2)EmptyState("Two models required","Import at least two distinct .litertlm model files in Models. No model output is simulated.")
 }
}

@Composable private fun WorkspaceScreen(projects:List<WorkspaceProjectEntity>,onAdd:()->Unit,onOpen:(WorkspaceProjectEntity)->Unit,onDelete:(Long)->Unit){
 var studioOpen by remember { mutableStateOf(false) }
 if(studioOpen){
  Column(Modifier.fillMaxSize()){
   TextButton(onClick={studioOpen=false},modifier=Modifier.padding(start=12.dp)){Icon(Icons.Default.ArrowBack,null);Text("Back to projects")}
   DeveloperStudioScreen(Modifier.weight(1f))
  }
  return
 }
 Column(Modifier.fillMaxSize().padding(16.dp)){
  Card(colors=CardDefaults.cardColors(containerColor=MaterialTheme.colorScheme.primaryContainer.copy(alpha=0.42f)),modifier=Modifier.fillMaxWidth()){Row(Modifier.fillMaxWidth().padding(16.dp),verticalAlignment=Alignment.CenterVertically){Column(Modifier.weight(1f)){Text("WORKSPACE",style=MaterialTheme.typography.labelMedium,color=MaterialTheme.colorScheme.primary,fontWeight=FontWeight.Bold);Text("Your local workbench",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold);Text("Projects, notes and a scoped code editor.",color=MaterialTheme.colorScheme.onSurfaceVariant)};Column(verticalArrangement=Arrangement.spacedBy(6.dp)){FilledTonalButton(onClick=onAdd){Icon(Icons.Default.Add,null);Text("New")};OutlinedButton(onClick={studioOpen=true}){Icon(Icons.Default.Code,null);Text("Studio")}}}}
  Spacer(Modifier.height(14.dp));if(projects.isEmpty())EmptyState("A space for your work","Create a project to keep its name and description on this device.")
  LazyColumn(Modifier.weight(1f),verticalArrangement=Arrangement.spacedBy(8.dp)){items(projects,key={it.id}){project->Card{Row(Modifier.fillMaxWidth().padding(14.dp),verticalAlignment=Alignment.CenterVertically){
   Icon(Icons.Default.Folder,null,tint=MaterialTheme.colorScheme.primary,modifier=Modifier.size(28.dp));Spacer(Modifier.width(12.dp))
   Column(Modifier.weight(1f)){Text(project.name,fontWeight=FontWeight.SemiBold);if(project.description.isNotBlank())Text(project.description,color=Muted,maxLines=2)}
   TextButton(onClick={onOpen(project)}){Text("Open assistant")}
   IconButton(onClick={onDelete(project.id)}){Icon(Icons.Default.DeleteOutline,"Delete project")}
  }} }}
 }
}
@Composable private fun TrainingLabScreen(
 datasetName:String,
 report:DatasetReport?,
 status:String,
 busy:Boolean,
 job:TrainingJobStatus?,
 jobStatus:String,
 trainingBusy:Boolean,
 onImport:()->Unit,
 onExport:()->Unit,
 onStartTraining:(String,String,String,String,Int)->Unit,
 onCancelTraining:(String,String,String)->Unit
){
 Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),verticalArrangement=Arrangement.spacedBy(12.dp)){
  Text("Training data lab",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold)
  Text("Import JSONL examples, validate their structure and export a cleaned dataset. Files are processed on this device.",color=Muted)
  Button(onClick=onImport,modifier=Modifier.fillMaxWidth(),enabled=!busy){Icon(Icons.Default.FileOpen,null);Spacer(Modifier.width(8.dp));Text("Import JSONL dataset")}
  if(busy)LinearProgressIndicator(Modifier.fillMaxWidth())
  if(report!=null){
   Text(datasetName,style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
   Card(Modifier.fillMaxWidth()){
    Column(Modifier.padding(14.dp),verticalArrangement=Arrangement.spacedBy(6.dp)){
     Text("Valid records: "+report.validRecords,style=MaterialTheme.typography.titleMedium,color=MaterialTheme.colorScheme.primary)
     Text("Training split: "+report.trainRecords)
     Text("Validation split: "+report.validationRecords)
     Text("Invalid lines: "+report.invalidLines.size,color=if(report.invalidLines.isEmpty())MaterialTheme.colorScheme.primary else Color(0xFF9A4D27))
     if(report.invalidLines.isNotEmpty())Text("Invalid line numbers: "+report.invalidLines.take(20).joinToString(", "),color=Muted,style=MaterialTheme.typography.bodySmall)
    }
   }
   Button(onClick=onExport,modifier=Modifier.fillMaxWidth(),enabled=!busy&&report.validRecords>0){Icon(Icons.Default.FileDownload,null);Spacer(Modifier.width(8.dp));Text("Export cleaned JSONL")}
  }else EmptyState("No dataset loaded","Choose a JSONL file containing text, prompt, or messages fields.")
  if(status.isNotBlank())Text(status,color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
  Divider()
  Text("Optional workstation training",style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
  Text("Training uploads the cleaned dataset to the HTTPS server you configure below. The API key is held only in this screen's memory and is not saved.",color=Muted,style=MaterialTheme.typography.bodySmall)
  var serverUrl by remember{mutableStateOf("")}
  var apiKey by remember{mutableStateOf("")}
  var baseModelPath by remember{mutableStateOf("")}
  var method by remember{mutableStateOf("lora")}
  var epochs by remember{mutableStateOf("1")}
  OutlinedTextField(serverUrl,{serverUrl=it},modifier=Modifier.fillMaxWidth(),label={Text("Training server HTTPS URL")},singleLine=true,enabled=!trainingBusy)
  OutlinedTextField(apiKey,{apiKey=it},modifier=Modifier.fillMaxWidth(),label={Text("Training API key")},singleLine=true,visualTransformation=PasswordVisualTransformation(),enabled=!trainingBusy)
  OutlinedTextField(baseModelPath,{baseModelPath=it},modifier=Modifier.fillMaxWidth(),label={Text("Server-local base model directory")},singleLine=true,enabled=!trainingBusy)
  Row(horizontalArrangement=Arrangement.spacedBy(8.dp),verticalAlignment=Alignment.CenterVertically){
   FilterChip(selected=method=="lora",onClick={method="lora"},label={Text("LoRA")},enabled=!trainingBusy)
   FilterChip(selected=method=="qlora",onClick={method="qlora"},label={Text("QLoRA")},enabled=!trainingBusy)
   OutlinedTextField(epochs,{epochs=it.filter(Char::isDigit)},modifier=Modifier.width(90.dp),label={Text("Epochs")},singleLine=true,enabled=!trainingBusy)
  }
  Button(onClick={onStartTraining(serverUrl.trim(),apiKey,baseModelPath.trim(),method,epochs.toIntOrNull()?:1)},modifier=Modifier.fillMaxWidth(),enabled=!trainingBusy&&report?.validRecords?.let{it>0}==true&&serverUrl.startsWith("https://")&&apiKey.length>=16&&baseModelPath.isNotBlank()&&(epochs.toIntOrNull()?:0) in 1..10){
   if(trainingBusy)CircularProgressIndicator(Modifier.size(18.dp),strokeWidth=2.dp)else Icon(Icons.Default.PlayArrow,null)
   Spacer(Modifier.width(8.dp));Text(if(trainingBusy)"Training job running…" else "Upload dataset and start training")
  }
  if(trainingBusy)LinearProgressIndicator(Modifier.fillMaxWidth())
  if(job!=null){
   Text("Job "+job.id+" · "+job.state.uppercase(),fontWeight=FontWeight.SemiBold)
   LinearProgressIndicator(progress=job.progress/100f,modifier=Modifier.fillMaxWidth())
   Text(job.message+" ("+job.progress.toInt()+"%)",color=Muted,style=MaterialTheme.typography.bodySmall)
   if(job.state=="queued"||job.state=="running")TextButton(onClick={onCancelTraining(serverUrl.trim(),apiKey,job.id)}){Text("Cancel training")}
   if(job.artifactUrl!=null)Text("Adapter artifact endpoint: "+serverUrl.trimEnd('/')+job.artifactUrl,color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
  }
  if(jobStatus.isNotBlank())Text(jobStatus,color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
  Text("The GPU worker runs on your workstation, not on Android. It returns a PEFT adapter and manifest; conversion to a directly loadable .litertlm model is a separate step.",color=Muted,style=MaterialTheme.typography.bodySmall)
 }
}

private const val MAX_DATASET_BYTES = 20 * 1024 * 1024
private suspend fun readDatasetBounded(context:Context,uri:Uri):String = withContext(Dispatchers.IO){
 val input=context.contentResolver.openInputStream(uri)?:error("Cannot open dataset file")
 input.use{stream->
  val output=ByteArrayOutputStream()
  val buffer=ByteArray(8192)
  var total=0
  while(true){
   val count=stream.read(buffer)
   if(count<0)break
   total+=count
   require(total<=MAX_DATASET_BYTES){"Dataset exceeds the 20 MiB import limit."}
   output.write(buffer,0,count)
  }
  String(output.toByteArray(),Charsets.UTF_8)
 }
}

@Composable private fun SettingsScreen(
 languageTag:String,
 selectedVoiceName:String?,
 voices:List<org.molecularis.app.features.OfflineTtsVoice>,
 recognition:org.molecularis.app.features.OfflineRecognitionLanguages,
 speechStatus:String,
 responseStyle:String,
 darkAppearance:Boolean,
 accentName:String,
 engineOptimization:String,
 onResponseStyleChange:(String)->Unit,
 onAccentChange:(String)->Unit,
 onDarkAppearanceChange:(Boolean)->Unit,
 onEngineOptimizationChange:(String)->Unit,
 onLanguageChange:(String)->Unit,
 onCheckLanguages:()->Unit,
 onDownloadLanguage:()->Unit,
 onVoiceSelect:(String)->Unit,
 onTestVoice:()->Unit
){
 var languageDraft by remember(languageTag){mutableStateOf(languageTag)}
 var voiceMenu by remember{mutableStateOf(false)}
 var languageMenu by remember{mutableStateOf(false)}
 val languageOptions=(listOf(languageTag,java.util.Locale.getDefault().toLanguageTag(),"en-US","hi-IN","bn-IN")+recognition.installed+recognition.downloadable+recognition.pending).distinct()
 val duplicateVoiceLabels=voices.groupingBy{it.label}.eachCount()
 Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp)){
  Card(colors=CardDefaults.cardColors(containerColor=MaterialTheme.colorScheme.primaryContainer.copy(alpha=0.42f)),modifier=Modifier.fillMaxWidth()){Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(5.dp)){Text("CUSTOMIZE",style=MaterialTheme.typography.labelMedium,color=MaterialTheme.colorScheme.primary,fontWeight=FontWeight.Bold);Text("Make Molecularis yours",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold);Text("Appearance, response style, engine behaviour and offline voice preferences. Saved on this device.",color=MaterialTheme.colorScheme.onSurfaceVariant)}}
  Text("Response style",style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
  Row(horizontalArrangement=Arrangement.spacedBy(6.dp)){
   FilterChip(selected=responseStyle=="concise",onClick={onResponseStyleChange("concise")},label={Text("Concise")})
   FilterChip(selected=responseStyle=="balanced",onClick={onResponseStyleChange("balanced")},label={Text("Balanced")})
   FilterChip(selected=responseStyle=="detailed",onClick={onResponseStyleChange("detailed")},label={Text("Detailed")})
  }
  Row(verticalAlignment=Alignment.CenterVertically){
   Column(Modifier.weight(1f)){Text("Dark appearance",fontWeight=FontWeight.Medium);Text(if(darkAppearance)"Enabled · low-glare dark workspace" else "Disabled · light workspace",style=MaterialTheme.typography.bodySmall,color=Muted)}
   Switch(checked=darkAppearance,onCheckedChange=onDarkAppearanceChange)
  }
  Text("Colour palette",style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
  Text("Soft classic accents. Select a swatch to apply it across cards, buttons and active states.",style=MaterialTheme.typography.bodySmall,color=Muted)
  val palette=listOf("Sage" to 0xFF78988A,"Sky" to 0xFF83AFCB,"Lavender" to 0xFFA69BCB,"Rose" to 0xFFC58F9C,"Peach" to 0xFFD5A184,"Butter" to 0xFFC8B36F,"Seafoam" to 0xFF83B8A8,"Mint" to 0xFF16866A,"Blue" to 0xFF4968D8,"Violet" to 0xFF7955C8,"Amber" to 0xFFB7791F,"Graphite" to 0xFF4B5563)
  palette.chunked(4).forEach{row->Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(8.dp)){row.forEach{(name,hex)->val selected=accentName==name;Surface(onClick={onAccentChange(name)},shape=RoundedCornerShape(14.dp),color=Color(hex).copy(alpha=if(selected)0.28f else 0.12f),border=if(selected)androidx.compose.foundation.BorderStroke(2.dp,Color(hex)) else null,modifier=Modifier.weight(1f)){Column(Modifier.padding(vertical=10.dp),horizontalAlignment=Alignment.CenterHorizontally){Box(Modifier.size(22.dp).background(Color(hex),CircleShape));Spacer(Modifier.height(5.dp));Text(name,style=MaterialTheme.typography.labelSmall,maxLines=1)}}}}}
  var customHex by remember{mutableStateOf(if(accentName.startsWith("#"))accentName else "#D8B4FE")}
  Row(verticalAlignment=Alignment.CenterVertically,horizontalArrangement=Arrangement.spacedBy(8.dp)){OutlinedTextField(customHex,{customHex=it.uppercase()},modifier=Modifier.weight(1f),label={Text("Custom HEX colour")},singleLine=true,placeholder={Text("#D8B4FE")});Button(onClick={onAccentChange(customHex)},enabled=customHex.matches(Regex("#[A-F0-9]{6}"))){Text("Apply")}}
  Divider()
  Text("Engine optimization",style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
  Text("Choose how much recent chat context is sent to the local model. Smaller context can reduce prompt processing time and memory pressure.",style=MaterialTheme.typography.bodySmall,color=Muted)
  Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(6.dp)){listOf("memory" to "Memory saver","speed" to "Faster","balanced" to "Balanced","quality" to "More context").forEach{(value,label)->FilterChip(selected=engineOptimization==value,onClick={onEngineOptimizationChange(value)},label={Text(label)},modifier=Modifier.weight(1f))}}
  Text(when(engineOptimization){"memory"->"Uses the last 2 completed turns."; "speed"->"Uses the last 4 completed turns."; "quality"->"Uses the last 24 completed turns.";else->"Uses the last 12 completed turns."},style=MaterialTheme.typography.labelSmall,color=MaterialTheme.colorScheme.primary)
  Divider()
  Text("Privacy & device",style=MaterialTheme.typography.headlineSmall,fontWeight=FontWeight.SemiBold)
  InfoCard("Offline-first","Chat records and model files are stored on this device. Model generation runs locally.")
  InfoCard("No silent uploads","This app does not upload chats or connect to an account or server.")
  InfoCard("Model requirement","Obtain a compatible .litertlm model separately, then import it in Models. Chat generation works offline after model installation.")
  Spacer(Modifier.height(12.dp))
  Text("Offline voice",style=MaterialTheme.typography.titleLarge,fontWeight=FontWeight.SemiBold)
  Text("Voice names are shown as readable languages and quality levels instead of Android's technical voice IDs. Tap a voice to select and preview it.",color=Muted,style=MaterialTheme.typography.bodySmall)
  Text("Speech recognition uses Android's on-device recognizer only. Text-to-speech is restricted to installed voices that do not require a network connection.",color=Muted,style=MaterialTheme.typography.bodySmall)
  Box{
   OutlinedButton(onClick={languageMenu=true},modifier=Modifier.fillMaxWidth()){
    Column(Modifier.weight(1f),horizontalAlignment=Alignment.Start){Text("Speech language",style=MaterialTheme.typography.labelSmall,color=Muted);Text(friendlyLanguageName(languageDraft),maxLines=1,overflow=TextOverflow.Ellipsis)}
    Icon(Icons.Default.ExpandMore,null)
   }
   DropdownMenu(expanded=languageMenu,onDismissRequest={languageMenu=false}){
    languageOptions.forEach{tag->DropdownMenuItem(text={Text(friendlyLanguageName(tag))},leadingIcon={if(tag.equals(languageDraft,true))Icon(Icons.Default.Check,null)},onClick={languageDraft=tag;languageMenu=false})}
   }
  }
  Button(onClick={onLanguageChange(languageDraft)},modifier=Modifier.fillMaxWidth()){Text("Use this speech language")}
  Row(horizontalArrangement=Arrangement.spacedBy(8.dp)){
   OutlinedButton(onClick=onCheckLanguages,modifier=Modifier.weight(1f)){Text("Check packs")}
   Button(onClick=onDownloadLanguage,modifier=Modifier.weight(1f),enabled=recognition.downloadable.isNotEmpty()){Text("Download pack")}
  }
  if(recognition.installed.isNotEmpty())Text("Installed for offline speech: "+recognition.installed.joinToString{friendlyLanguageName(it)},color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
  if(recognition.downloadable.isNotEmpty())Text("Available to download: "+recognition.downloadable.joinToString{friendlyLanguageName(it)},color=Muted,style=MaterialTheme.typography.bodySmall)
  if(recognition.pending.isNotEmpty())Text("Download pending: "+recognition.pending.joinToString{friendlyLanguageName(it)},color=Muted,style=MaterialTheme.typography.bodySmall)
  Text("Offline TTS voice",style=MaterialTheme.typography.titleMedium,fontWeight=FontWeight.SemiBold)
  Box{
   OutlinedButton(onClick={voiceMenu=true},modifier=Modifier.fillMaxWidth(),enabled=voices.isNotEmpty()){
    Text(voices.firstOrNull{it.name==selectedVoiceName}?.label?:if(voices.isEmpty())"No offline TTS voices installed" else voices.first().label)
   }
   DropdownMenu(expanded=voiceMenu,onDismissRequest={voiceMenu=false}){
    voices.forEachIndexed{index,voice->DropdownMenuItem(
     text={Column{val duplicateCount=duplicateVoiceLabels[voice.label]?:0;val display=voice.label+(if(duplicateCount>1)" · Voice "+voices.take(index+1).count{it.label==voice.label} else "");Text(display);Text("Installed on this device · offline · tap to preview",style=MaterialTheme.typography.labelSmall,color=Muted)}},
     leadingIcon={Icon(Icons.Default.RecordVoiceOver,null)},
     onClick={voiceMenu=false;onVoiceSelect(voice.name);onTestVoice()}
    )}
   }
  }
  OutlinedButton(onClick=onTestVoice,modifier=Modifier.fillMaxWidth(),enabled=voices.isNotEmpty()){Icon(Icons.Default.VolumeUp,null);Spacer(Modifier.width(8.dp));Text("Test offline voice")}
  Text(speechStatus,color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.bodySmall)
  InfoCard("Language pack downloads","On Android 13 and newer, Molecularis can ask the system speech provider to download supported on-device recognition languages. The system provider controls the actual download and availability. Android 12 can use an already-installed on-device recognizer but cannot expose the same pack-management API.")
 }
}
@Composable private fun InfoCard(title:String,body:String){Card(Modifier.fillMaxWidth().padding(bottom=10.dp)){Column(Modifier.padding(16.dp)){Text(title,fontWeight=FontWeight.SemiBold);Spacer(Modifier.height(4.dp));Text(body,color=Muted,style=MaterialTheme.typography.bodyMedium)}}}
@Composable private fun EmptyState(title:String,body:String){Column(Modifier.fillMaxWidth().padding(vertical=24.dp),horizontalAlignment=Alignment.CenterHorizontally){Text(title,fontWeight=FontWeight.SemiBold);Text(body,color=Muted,style=MaterialTheme.typography.bodySmall)}}
private fun friendlyLanguageName(tag:String):String {
 val locale=java.util.Locale.forLanguageTag(tag)
 val display=locale.getDisplayName(java.util.Locale.getDefault())
 return if(display.isBlank())tag else "$display ($tag)"
}
private fun formatBytes(bytes:Long):String=when{bytes>=1073741824->"%.1f GB".format(bytes/1073741824.0);bytes>=1048576->"%.1f MB".format(bytes/1048576.0);bytes>=1024->"%.1f KB".format(bytes/1024.0);else->"$bytes B"}

@Composable private fun HubCapabilityCard(title:String,subtitle:String,status:String,icon: androidx.compose.ui.graphics.vector.ImageVector,modifier:Modifier=Modifier){
 Card(modifier=modifier,colors=CardDefaults.cardColors(containerColor=MaterialTheme.colorScheme.surfaceVariant.copy(alpha=0.62f))){Column(Modifier.fillMaxWidth().padding(12.dp),verticalArrangement=Arrangement.spacedBy(5.dp)){Icon(icon,null,tint=MaterialTheme.colorScheme.primary,modifier=Modifier.size(22.dp));Text(title,fontWeight=FontWeight.SemiBold,style=MaterialTheme.typography.titleSmall);Text(subtitle,style=MaterialTheme.typography.bodySmall,color=Muted);Text(status,style=MaterialTheme.typography.labelSmall,color=MaterialTheme.colorScheme.primary)}}
}

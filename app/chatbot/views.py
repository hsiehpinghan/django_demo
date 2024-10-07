import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_openai import ChatOpenAI
#from langchain_openai import OpenAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .forms import CreateThread, CreateMessage, CreateFile
from .models import Thread, Message, File
from .serializers import ThreadSerializer, MessageSerializer
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
from .tools import CountCharactersTool

llm = ChatOpenAI(model=os.environ['LLM_MODEL'],
                 api_key=os.environ['LLM_API_KEY'],
                 base_url=os.environ['LLM_API_BASE'])
llm.bind_tools([CountCharactersTool()])
embeddings = HuggingFaceEndpointEmbeddings(model=os.environ['EMBEDDING_API_BASE'])
reranker = HuggingFaceCrossEncoder(model_name=os.environ['RERANK_MODEL'],
                                   model_kwargs={'cache_dir': 'hf_cache'})

index_path = 'faiss_index'

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
@login_required(login_url='/login/')
def get_threads(request):
    threads = Thread.objects.filter(user=request.user).order_by('created_at')
    serializer = ThreadSerializer(threads, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@login_required(login_url='/login/')
def add_thread(request):
    form = CreateThread(request.POST)
    if form.is_valid() is False:
        return Response({'error': form.errors}, status=400)
    thread = form.save(commit=False)
    thread.user = request.user
    thread.save()
    return Response({'id': thread.id, 'name': thread.name}, status=200)

@api_view(['POST'])
@login_required(login_url='/login/')
def add_message(request):
    form = CreateMessage(request.POST)
    if form.is_valid() is False:
        return Response({'error': form.errors}, status=400)
    message = form.save(commit=False)
    message.type = 'user'
    message.thread = Thread.objects.get(id=request.POST.get('thread_id'))
    message.save()
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_type='similarity',
                                         search_kwargs={'k': 10})
    compressor = CrossEncoderReranker(model=reranker, top_n=1)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=compression_retriever)
    result = qa.run(message.content)
    Message(content=result, type='ai', thread=message.thread).save()
    return Response({'content': result}, status=200)

@api_view(['POST'])
@login_required(login_url='/login/')
def get_messages(request):
    thread = Thread.objects.get(id=request.POST.get('thread_id'))
    messages = Message.objects.filter(thread=thread).order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@login_required(login_url='/login/')
def upload_file(request):
    form = CreateFile(request.POST, request.FILES)
    if form.is_valid() is False:
        return Response({'error': form.errors}, status=400)
    file = form.save(commit=False)
    file.user = request.user
    file.save()
    _save_to_vector_db(file.file.path)
    return Response({'success': True}, status=200)
            
def _save_to_vector_db(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
    chunks = text_splitter.split_text(content)
    documents = []
    for chunk in chunks:
        documents.append(Document(page_content=chunk))
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(index_path)

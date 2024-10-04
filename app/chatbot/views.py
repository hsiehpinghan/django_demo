import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_openai import ChatOpenAI
from .forms import CreateThread, CreateMessage, CreateFile
from .models import Thread, Message, File
from .serializers import ThreadSerializer

client = ChatOpenAI(model=os.environ['LLM_MODEL'],
                    api_key=os.environ['LLM_API_KEY'],
                    base_url=os.environ['LLM_API_BASE'])

# Create your views here.
#@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def get_threads(request):
    threads = Thread.objects.filter(user=request.user).order_by('created_at')
    serializer = ThreadSerializer(threads, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_thread(request):
    form = CreateThread(request.POST)
    if form.is_valid():
        thread = form.save(commit=False)
        thread.user = request.user
        thread.save()
    return Response({'id': thread.id, 'name': thread.name}, status=200)

@api_view(['POST'])
def add_message(request):
    form = CreateMessage(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.type = 'user'
        message.thread = Thread.objects.get(id=request.POST.get('thread_id'))
        message.save()
    response = client.invoke(message.content)
    return Response({'content': response.content}, status=200)

@api_view(['POST'])
def upload_file(request):
    form = CreateFile(request.POST, request.FILES)
    if form.is_valid() is False:
        return Response({'error': form.errors}, status=400)
    file = form.save(commit=False)
    file.user = request.user
    file.save()

    with open(file.file.path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(content, '!!!!!!!!!!!^^^!')


    
    return Response({'success': True}, status=200)
            



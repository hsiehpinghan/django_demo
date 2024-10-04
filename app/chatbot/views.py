from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import CreateThread, CreateMessage
from .models import Thread, Message
from .serializers import ThreadSerializer

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
    if request.method == 'POST':
        form = CreateThread(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
    return Response({'id': thread.id, 'name': thread.name}, status=200)

@api_view(['POST'])
def add_message(request):
    if request.method == 'POST':
        form = CreateMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'human'
            message.content = request.POST.get('message')
            message.thread = Thread.objects.get(id=request.POST.get('thread_id'))
            message.save()
    return Response({'content': 'hi hi'}, status=200)


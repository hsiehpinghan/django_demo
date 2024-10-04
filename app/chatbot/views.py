from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import CreateThread

# Create your views here.
#@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def add_thread(request):
    if request.method == 'POST':
        form = CreateThread(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user

            print(thread.name, '!!!!!!!!!!!!!!')
            thread.save()
    return Response({'thread_id': thread.id}, status=200)

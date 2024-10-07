from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import os
import re
import json

url = 'https://api.dify.ai/v1/chat-messages'
headers = {
    'Authorization': f'Bearer {os.getenv("DIFY_API_KEY")}',
    'Content-Type': 'application/json'
}

# Create your views here.
@csrf_protect
@login_required(login_url='/login/')
def index(request):
    return render(request, 'workflow.html')

@csrf_protect
@login_required(login_url='/login/')
def get_html(request):
    content = request.POST.get('content')
    print(content, '!!!!!!!!!!!!!!!!!!!!!!!')
    data = {
        "inputs": {},
        "query": content,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "abc-123"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        # 使用正則表達式提取 <html> 和 </html> 之間的內容
        answer = json.loads(response.text)['answer']
        html_content = re.search(r'```html(.*?)```', answer, re.DOTALL)
        if html_content:
            extracted_html = html_content.group(1)
            return JsonResponse({'html': extracted_html})
        else:
            return JsonResponse({'error': '無法提取 HTML 內容'}, status=500)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
# init poetry
cd /home/hsiehpinghan/git/django_demo/
poetry init
    Package name [django-demo]:  
    Version [0.1.0]:  
    Description []:  
    Author [hsiehpinghan <thank.hsiehpinghan@gmail.com>, n to skip]:  
    License []:  
    Compatible Python versions [^3.9]:  ^3.10
    Would you like to define your main dependencies interactively? (yes/no) [no] 
    Would you like to define your development dependencies interactively? (yes/no) [no]
    Do you confirm generation? (yes/no) [yes] 
poetry config --list
poetry config virtualenvs.in-project true
poetry env use 3.10
poetry add django==5.0.1
poetry add djangorestframework==3.14.0
poetry add langchain-huggingface==0.0.3
poetry add langchain-openai==0.1.10
poetry add langchain==0.2.7
poetry add langchain-community==0.2.1
poetry add python-dotenv==1.0.1
poetry add faiss-cpu==1.7.4
poetry add tika==2.6.0
poetry add python-docx==1.1.0
poetry add xgboost==2.0.3
poetry add pdfplumber==0.10.4
poetry add pypdf==4.3.0
poetry add markdown==3.6
poetry add cachetools==5.3.3
poetry add ruamel.yaml==0.18.6
poetry add StrEnum==0.4.15
poetry add onnxruntime-gpu==1.17.1
poetry add datrie==0.8.2
poetry add hanziconv==0.3.2
poetry add nltk==3.8.1
poetry add six==1.16.0
poetry add opencv-python-headless==4.9.0.80
poetry add shapely==2.0.3
poetry add pyclipper==1.3.0.post5
poetry add elasticsearch-dsl==8.12.0
poetry add roman-numbers==1.0.2
poetry add word2number==1.1
poetry add cn2an==0.5.22
poetry add pandas==2.2.1
poetry add pycryptodomex==3.20.0

cd /home/hsiehpinghan/git/django_demo/app
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py startapp chatbot
poetry run python manage.py startapp workflow
poetry run python manage.py runserver

# docker
## tgi
docker run -itd \
    --name tgi \
    -e HF_TOKEN=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 \
    -p 10080:80 \
    -v /home/hsiehpinghan/Desktop/data:/data \
    ghcr.io/huggingface/text-generation-inference:2.2.0 \
    --model-id Qwen/Qwen2-0.5B-Instruct
curl http://127.0.0.1:10080/generate_stream \
    -X POST \
    -d '{"inputs":"What is Deep Learning?", "parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
## tei_embedding
docker run -itd \
    --name tei_embedding \
    -p 10081:80 \
    -v /home/hsiehpinghan/Desktop/data:/data \
    ghcr.io/huggingface/text-embeddings-inference:cpu-1.0 \
    --model-id intfloat/multilingual-e5-large-instruct \
    --revision baa7be480a7de1539afce709c8f13f833a510e0a
curl 127.0.0.1:10081/embed \
    -X POST \
    -d '{"inputs":"What is Deep Learning?"}' \
    -H 'Content-Type: application/json'

# export
cd /home/hsiehpinghan/git/django_demo/
poetry export -f requirements.txt -o requirements.txt --without-hashes
docker build -t django_demo:0.9.0 .
docker run -itd \
    --name app \
    -p 80:8000 \
    --link tgi:tgi \
    --link tei_embedding:tei_embedding \
    -e LLM_MODEL=Qwen/Qwen2-0.5B-Instruct \
    -e LLM_API_KEY=Placeholder \
    -e LLM_API_BASE=http://tgi:80/v1 \
    -e EMBEDDING_API_BASE=http://tei_embedding:80 \
    -e RERANK_MODEL=BAAI/bge-reranker-base \
    django_demo:0.9.0
docker tag django_demo:0.9.0 hsiehpinghan/django_demo:0.9.0
docker login
docker push hsiehpinghan/django_demo:0.9.0

# gcp
https://docs.docker.com/engine/install/ubuntu/
git clone https://github.com/hsiehpinghan/django_demo.git
cd django_demo
sudo docker compose up -d

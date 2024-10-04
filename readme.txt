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
cd /home/hsiehpinghan/git/django_demo/app
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py startapp chatbot
poetry run python manage.py runserver

# export
cd /home/hsiehpinghan/git/django_demo/
poetry export -f requirements.txt -o requirements.txt --without-hashes
docker build -t django_demo:0.1.0 .

docker login
docker push myapp:1.0

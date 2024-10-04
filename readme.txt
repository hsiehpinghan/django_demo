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
cd /home/hsiehpinghan/git/django_demo/app
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py startapp chatbot
poetry run python manage.py runserver






poetry run python manage.py startapp commons
poetry run python manage.py startapp assistants
poetry run python manage.py startapp runs
poetry run python manage.py startapp threads
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py makemigrations
poetry run python manage.py makemigrations commons --name initial_migration
poetry run python manage.py migrate
poetry run python manage.py runserver
poetry run python manage.py test commons
poetry run python manage.py test assistants
poetry run python manage.py test runs



# init django
cd C:\Users\thank\git\django_demo
poetry run django-admin startproject app
mkdir C:\Users\thank\git\django_demo\app\app\templates
cd C:\Users\thank\git\django_demo\app
poetry run python manage.py runserver

# init tailwind
cd C:\Users\thank\git\django_demo
fnm env --use-on-cd | Out-String | Invoke-Expression
npm init -y
npm view tailwindcss versions
npm install -D tailwindcss@3.4.11
npx tailwindcss init
npm install -D @tailwindcss/forms
npm install -D @tailwindcss/typography
npm install -D prettier prettier-plugin-tailwindcss
mkdir C:\Users\thank\git\django_demo\gpts\static
mkdir C:\Users\thank\git\django_demo\gpts\static\src
npx tailwindcss -i C:\Users\thank\git\django_demo\gpts\static\src\styles.css -o C:\Users\thank\git\django_demo\gpts\static\dist\styles.css --watch

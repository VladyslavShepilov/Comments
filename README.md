## Comments
Application for managing comments board. Consists of 3 applications: 
* comments, which is the main app with console commands, celery settings, settings and utils for jwt authentication.
* dashboard, which is responsible for managing comments. Consists of models, views, celery tasks for additional validation with scheduled requests to OpenAI,
and additional validation.
* User application with implemented jwt functionality, custom user views and forms.

### Credentials

    python manage.py createsuperuser

### For docker
    docker exec -it <container name/id> sh
    python manage.py createsuperuser


##  Installing / Getting Started
Set your .env variables using .env_sample, or simply copy-paste values. Retrieve your personal OpenAI token to make additional validation work. 

### Using Shell Console
    git clone ...
    cd comments
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

### Using Docker
    cp .env_sample .env
    python manage.py makemigrations
    docker-compose build
    docker-compose up
Installs requirements and runs the Django server.

### Features
* JWT authentication
* Celery - RabbitMQ tasks
* OpenAI requests
* Admin panel with task's logs.
* Custom user update page with not required password changing.
* Comments with captcha, images and files.

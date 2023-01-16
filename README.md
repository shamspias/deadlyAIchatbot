## WhatsAPP AI Chatbot for DeadlyAI
Rename example-docker-compose.yml to docker-compose.yml


Flask, Celery, Flower and Redis services with Docker
docker-compose.yml file split into the following services
- redis
- website
- celery
- flower

### Build With
- Whatsapp Business API
- OpenAI GPT-3
- OpenAI DAL-E-2

### Technology 

* Python
* Flask
* PostgresSQL


### Install & deploy

- Rename example.env to .env and set the API key for OpenAI
- Create a virtual environment and active it
  - Windows
  - ```python -m venv venv```
  - ```venv/Scripts/activate```
  - Linux/Mac 
  - ```python3 -m venv venv```
  - ```venv/bin/activate```
- Install the requirements ```pip install -r requirements.txt```
- Run it ```python app.py```
- If everything is ok then host it with Nginx and Guniron.

### Host Flask Application
- Host to Ubuntu VPS [Tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
- Host to Heroku [Tutorial](https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/)



## Setup gunicorn

- Make gunicorn service file```sudo nano /etc/systemd/system/deadlyai.service```
- Write service into gunicorn service file
  ```
  [Unit]
  Description=Gunicorn instance to serve whatsapp chatbot script
  After=network.target
  
  [Service]
  User=ubuntu
  Group=www-data
  WorkingDirectory=/home/ubuntu/deadlyAIchatbot
  Environment="PATH=/home/ubuntu/deadlyAIchatbot/venv/bin"
  ExecStart=/home/ubuntu/deadlyAIchatbot/venv/bin/gunicorn --workers 3 --bind unix:deadlyai.sock -m 007 wsgi:app
  
  [Install]
  WantedBy=multi-user.target
  ```
- Start and enable the service 
  ``` sudo systemctl start deadlyai && sudo systemctl enable deadlyai ```

## Setup Nginx

- Create nginx config `sudo nano /etc/nginx/sites-available/deadlyai` and add the code
  ``` 
  server {
      listen 80;
      server_name chatbot.deadlyai.com www.chatbot.deadlyai.com;
  
      location / {
          include proxy_params;
          proxy_pass http://unix:/home/ubuntu/deadlyAIchatbot/deadlyai.sock;
      }
  }
  ```
- Symlink the nginx config `sudo ln -s /etc/nginx/sites-available/deadlyai /etc/nginx/sites-enabled`
- Restart the nginx


With Docker
```
version: '3.8'

services:

  redis:
    image: 'redis:5.0.5'
    command: redis-server --requirepass devpassword
    volumes:
      - 'redis:/var/lib/redis/data'
    ports:
      - '6379:6379'

  website:
    build: .
    command: >
      gunicorn -b 0.0.0.0:8000
        --access-logfile -
        --reload
        "src.app:flask_app"
    env_file:
      - '.env'
    volumes:
      - '.:/deadlyai'
    ports:
      - '8000:8000'

  celery:
    build: .
    command: celery -A wsgi_app.celery worker --loglevel=info --pool=solo
    env_file:
      - '.env'
    volumes:
      - '.:/deadlyai'

  flower:
    image: mher/flower
    environment:
      - CELERY_BROKER_URL=redis://:devpassword@redis:6379/0
      - FLOWER_PORT=5555
    ports:
      - 5555:5555

volumes:
  redis:

```

## Instructions
1. Must have docker installed.
2. CD into the root of the project
3. Create a .env file with the following env variables. Place it in the root directory (same level as docker-compose.yaml).
   ```
   COMPOSE_PROJECT_NAME=deadlyai
   PYTHONUNBUFFERED=true
   ```
4. Build the containers
   ```
   docker-compose up --build
   ```
   

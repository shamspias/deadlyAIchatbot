## WhatsAPP AI Chatbot for DeadlyAI

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
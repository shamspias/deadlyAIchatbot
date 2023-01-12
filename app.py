import os
from dotenv import load_dotenv
from flask import Flask, request, session
from deadlyaibot import ask, append_interaction_to_chat_log

app = Flask(__name__)
# if for some reason your conversation with the bot gets weird, change the secret key
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


# app.config['SECRET_KEY'] = '89djhff9lhkd93' # Testing


@app.route('/deadlyai', methods=['POST'])
def deadly_text_chat():
    incoming_msg = request.values['Body']
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                         chat_log)
    msg = answer
    return str(msg)


if __name__ == '__main__':
    app.run(debug=True)

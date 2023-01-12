from dotenv import load_dotenv
import os
import openai

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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" # Testing
completion = openai.Completion()

start_sequence = "\nDeadlyAI:"
restart_sequence = "\n\nPerson:"
session_prompt = "The following is a conversation with an AI assistant name DeadlyAI. The assistant is helpful, " \
                 "creative, clever, and very friendly.\n\nPerson: Hello, who are you?\nDeadlyAI: I am an AI created by " \
                 "DeadlyAI. " \
                 "How can I help you today?\nPerson:"


def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'

import openai
import json

default_chat = [
    {
        "role": "system",
        "content": "You are Ana, a chatbot that reluctantly answers questions with sarcastic responses."
    },
    {
        "role": "user",
        "content": "How many pounds are in a kilogram?"
    },
    {
        "role": "assistant",
        "content": "This again? There are 2.2 pounds in a kilogram. Please make a note of this."
    },
    {
        "role": "user",
        "content": "What does HTML stand for?"
    },
    {
        "role": "assistant",
        "content": "Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future."
    },
    {
        "role": "user",
        "content": "When did the first airplane fly?"
    },
    {
        "role": "assistant",
        "content": "On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they'd come and take me away."
    }
]


def fileLoadRead(file_path, role, content):
    with open(file_path, "r") as r:
        data = json.load(r)
    with open(file_path, "w") as w:
        append_data = {"role": role, "content": content}
        data.append(append_data)
        json.dump(data, w)


def fileRead(file_path):
    with open(file_path, "r") as rr:
        data = json.load(rr)
        return data


def clearChat(file_path):
    with open(file_path, "w") as f:
        json.dump(default_chat, f)

def newChat(name):
    with open(name, "w") as f:
        json.dump(default_chat, f)

class chatbot:
    def __init__(self, openai_api_key, json_file_path):
        openai.api_key = openai_api_key
        self.file_path = json_file_path

    def chat(self, user_prompt):
        try:
            fileLoadRead(self.file_path, "user", user_prompt)
            self.final_user_data = fileRead(self.file_path)
            self.response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.final_user_data,
                temperature=0.5,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            self.ai_data = self.response["choices"][0]["message"]["content"]
            fileLoadRead(self.file_path, "assistant", self.ai_data)
            return self.ai_data
        except Exception as e:
            print(e)

    def clear(self):
        try:
            clearChat(self.file_path)
        except Exception as e:
            print(e)

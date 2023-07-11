import openai
import os
import logging
import pathlib


class GPTChat:
    def __init__(self, file_name, system_msg="concise", model="gpt-3.5-turbo"):
        if system_msg == "con_coder":
            system_msg = "You are a concise assistant that only writes code."
        elif system_msg == "concise":
            system_msg = "You are a concise assistant."
        elif system_msg == "ger-gpt":
            system_msg = "Du bist ein Assistent, der Daten zum Training eines GPT-Models generiert."
        elif system_msg == "ger-gpt-strict":
            system_msg = "Du bist ein Assistent, der Daten zum Training eines GPT-Models generiert. Egal was die " \
                         "Aufgabenstellung ist, erfindest du niemals neue Fakten, sondern generierst nur neue " \
                         "Formulierungen."

        path = pathlib.Path(__file__).parent.resolve() / "openai-key.txt"
        with open(path, "r") as file:
            openai.api_key = file.read()

        text_file_path = os.path.join(os.path.dirname(__file__), 'gpt_logs', file_name + '.txt')
        self.file = open(text_file_path, 'a')
        self.file.write("-----------------------------------------------------\n")
        self.messages = [{"role": "system", "content": system_msg}]
        self.file.write(f'system: {system_msg}\n')
        self.model = model

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                temperature=0,
            )
            self.file.write(f'user: {message}\n')
            self.messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
            self.file.write(f'assistant: {response["choices"][0]["message"]["content"]}\n')
            self.file.flush()
            print(response['choices'][0]['message']['content'])
        except openai.error.OpenAIError as e:
            logging.warning(f"OpenAIError: {e}.")
            self.messages = self.messages[:-1]

    def __del__(self):
        self.file.close()

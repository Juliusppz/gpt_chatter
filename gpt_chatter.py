import openai
import os


class GPTChat:
    def __init__(self, file_name, system_msg="concise", model="gpt-3.5-turbo"):
        if system_msg == "con_coder":
            system_msg = "You are a concise assistant that only writes code."
        elif system_msg == "concise":
            system_msg = "You are a concise assistant."

        openai.api_key = ""
        text_file_path = os.path.join(os.path.dirname(__file__), 'gpt_logs', file_name + '.txt')
        self.file = open(text_file_path, 'a')
        self.file.write("-----------------------------------------------------\n")
        self.messages = [{"role": "system", "content": system_msg}]
        self.file.write(f'system: {system_msg}\n')
        self.model = model

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        self.file.write(f'user: {message}\n')
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0,
        )
        self.messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        self.file.write(f'assistant: {response["choices"][0]["message"]["content"]}\n')
        print(response['choices'][0]['message']['content'])

    def __del__(self):
        self.file.close()

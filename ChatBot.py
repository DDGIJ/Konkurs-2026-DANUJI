import random
import tkinter as tk
from tkinter import scrolledtext


class ChatBot:
    def __init__(self):
        self.name = ""
        self.topic = "name"

        self.topics = {
            "robot": {
                "words": ["робот", "робота", "роботов", "робототехника"],
                "question": "Что твой робот уже умеет?"
            },
            "code": {
                "words": [
                    "python", "питон", "код",
                    "программа", "программу", "программирование"
                ],
                "question": "Что сейчас пишешь?"
            },
            "game": {
                "words": ["игра", "игры", "игру", "играю"],
                "question": "В какую игру играешь?"
            }
        }

        self.topic_names = {
            "robot": "роботы",
            "code": "программирование",
            "game": "игры"
        }

        self.dialog = {
            "robot": {
                "answer": "А чему хочешь научить робота дальше?",
                "next": "robot_plan"
            },
            "robot_plan": {
                "answer": "С чего планируешь начать?",
                "next": ""
            },
            "code": {
                "answer": "Что уже получилось сделать?",
                "next": "code_progress"
            },
            "code_progress": {
                "answer": "Какая часть оказалась самой сложной?",
                "next": ""
            },
            "game": {
                "answer": "Что тебе больше всего нравится в этой игре?",
                "next": "game_details"
            },
            "game_details": {
                "answer": "Ты чаще играешь один или с друзьями?",
                "next": ""
            },
            "hobby": {
                "answer": "Что тебе больше всего нравится в этом занятии?",
                "next": "hobby_details"
            },
            "hobby_details": {
                "answer": "Давно этим увлекаешься?",
                "next": ""
            }
        }

    def prepare_text(self, message):
        text = message.lower().replace("ё", "е")

        for symbol in "!?.,:;":
            text = text.replace(symbol, " ")

        return " ".join(text.split())

    def get_topic_list(self):
        topic_list = ""

        for topic in self.topic_names.values():
            topic_list += topic + ", "

        return topic_list[:-2]

    def find_topic(self, text):
        words = text.split()

        for topic_name, topic_data in self.topics.items():
            for keyword in topic_data["words"]:
                if keyword in words:
                    return topic_name

        return ""

    def continue_dialog(self):
        step = self.dialog[self.topic]
        self.topic = step["next"]
        return step["answer"]

    def reply(self, message):
        text = self.prepare_text(message)

        if text in ["пока", "до встречи", "до свидания"]:
            self.topic = ""
            return "До встречи!"

        if text in ["сменим тему", "давай о другом", "другая тема"]:
            self.topic = "hobby"
            return "Хорошо. Чем любишь заниматься в свободное время?"

        if "как тебя зовут" in text:
            return "Можешь называть меня Бот."

        if "как меня зовут" in text:
            if self.name:
                return f"Тебя зовут {self.name}."

            self.topic = "name"
            return "Пока не знаю. Как тебя зовут?"

        if text.startswith("меня зовут "):
            self.name = text[11:].title()
            self.topic = "day"

            return f"Приятно познакомиться, {self.name}! Как прошёл день?"

        if text in ["спасибо", "благодарю"]:
            return "Пожалуйста!"

        if text in [
            "привет",
            "здравствуй",
            "здравствуйте",
            "добрый день",
            "доброе утро",
            "добрый вечер"
        ]:
            if self.name:
                self.topic = "day"
                return f"Привет, {self.name}! Как прошёл день?"

            self.topic = "name"
            return "Привет! Как тебя зовут?"

        if "как дела" in text:
            self.topic = "day"
            return "Готов поболтать. А у тебя как дела?"

        if self.topic == "name":
            if text in ["не хочу", "не скажу", "секрет"]:
                self.topic = "day"
                return "Хорошо, можно без имени. Как прошёл день?"

            if len(text.split()) > 3:
                return "Можно просто имя. Или напиши «не хочу»."

            self.name = message.strip().title()
            self.topic = "day"

            return f"Приятно познакомиться, {self.name}! Как прошёл день?"

        if self.topic in self.dialog:
            return self.continue_dialog()

        new_topic = self.find_topic(text)

        if new_topic:
            self.topic = new_topic
            return self.topics[new_topic]["question"]

        if self.topic == "day":
            if (
                "не очень" in text
                or "плохо" in text
                or "грустно" in text
            ):
                self.topic = "bad_day"
                return "Жаль, что день не задался. Хочешь рассказать?"

            self.topic = "hobby"
            return "Чем сегодня занимался?"

        if self.topic == "bad_day":
            if text in ["нет", "не хочу"]:
                self.topic = "hobby"
                return "Хорошо. Чем тебе нравится заниматься?"

            if text in ["да", "хочу"]:
                return "Рассказывай. Что произошло?"

            self.topic = ""
            return (
                "Спасибо, что рассказал. "
                "Можешь продолжить или написать «сменим тему»."
            )

        return (
            "Не совсем понял, что вы написали. "
            "Давайте поговорим на эти темы: "
            + self.get_topic_list()
            + "."
        )


class ChatApp:
    def __init__(self, root):
        self.bot = ChatBot()

        root.title("Мой чат-бот")
        root.geometry("680x560")
        root.minsize(480, 360)
        root.configure(bg="#edf0f5")

        bottom = tk.Frame(root, bg="#edf0f5")
        bottom.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            padx=12,
            pady=12
        )

        send_button = tk.Button(
            bottom,
            text="Отправить",
            command=self.send_message,
            bg="#356ac3",
            fg="white",
            font=("Arial", 14),
            padx=12,
            pady=6
        )
        send_button.pack(side=tk.RIGHT, padx=(8, 0))

        self.entry = tk.Entry(
            bottom,
            font=("Arial", 12)
        )
        self.entry.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=6
        )
        self.entry.bind("<Return>", self.send_message)

        top = tk.Frame(root, bg="#edf0f5")
        top.pack(fill=tk.X, padx=12, pady=(10, 0))

        title = tk.Label(
            top,
            text="Небольшой собеседник",
            font=("Arial", 14, "bold"),
            bg="#edf0f5"
        )
        title.pack(side=tk.LEFT)

        restart_button = tk.Button(
            top,
            text="Новый разговор",
            command=self.restart_chat
        )
        restart_button.pack(side=tk.RIGHT)

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="white",
            padx=14,
            pady=14,
            state="disabled"
        )
        self.chat.pack(
            fill=tk.BOTH,
            expand=True,
            padx=12,
            pady=(10, 0)
        )

        self.chat.tag_configure("user", foreground="#2458a6")
        self.chat.tag_configure("bot", foreground="#287544")

        self.add_message(
            "Бот",
            "Привет! Я простой бот по правилам, но попробую "
            "поддержать разговор. Как тебя зовут?",
            "bot"
        )

        self.bot.topic = "name"
        self.entry.focus_set()

    def add_message(self, author, message, tag):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"{author}:\n", tag)
        self.chat.insert(tk.END, f"{message}\n\n")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def send_message(self, event=None):
        message = self.entry.get().strip()

        if message == "":
            return

        self.entry.delete(0, tk.END)

        self.add_message("Ты", message, "user")

        answer = self.bot.reply(message)
        self.add_message("Бот", answer, "bot")

        self.entry.focus_set()

    def restart_chat(self):
        self.bot = ChatBot()
        self.bot.topic = "name"

        self.chat.configure(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state="disabled")

        self.entry.delete(0, tk.END)

        self.add_message(
            "Бот",
            "Начнём заново! Как тебя зовут?",
            "bot"
        )

        self.entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

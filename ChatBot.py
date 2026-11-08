import random
import tkinter as tk
from tkinter import scrolledtext


class Bot:
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
                "answer": "Что тебе нравится в этой игре?",
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

        if text in ["привет", "здравствуй", "здравствуйте"]:
            if self.name:
                self.topic = "day"
                return f"Привет, {self.name}! Как прошёл день?"

            self.topic = "name"
            return "Привет! Как тебя зовут?"

        if text in ["спасибо", "благодарю"]:
            return "Пожалуйста!"

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

        return random.choice([
            "Расскажи немного подробнее.",
            "Не совсем понял. Можешь сказать по-другому?",
            "Можем поговорить о роботах, программах или играх."
        ])


class App:
    def __init__(self, root):
        self.bot = Bot()

        root.title("Бот")
        root.geometry("650x550")
        root.minsize(450, 350)
        root.configure(bg="#af6c6c")

        bottom_frame = tk.Frame(root, bg="#b8abab")
        bottom_frame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            padx=12,
            pady=12
        )

        clear_button = tk.Button(
            bottom_frame,
            text="Очистить диалог",
            command=self.clear_chat,
            bg="#534C4C",
            fg="white",
            padx=8,
            pady=6
        )
        clear_button.pack(side=tk.RIGHT, padx=(6, 0))

        send_button = tk.Button(
            bottom_frame,
            text="Отправить",
            command=self.send_message,
            bg="#534C4C",
            fg="white",
            padx=10,
            pady=6
        )
        send_button.pack(side=tk.RIGHT, padx=(6, 0))

        self.entry = tk.Entry(
            bottom_frame,
            font=("Times New Roman", 14)
        )
        self.entry.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=6
        )
        self.entry.bind("<Return>", self.send_message)

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Times New Roman", 14),
            bg="white",
            padx=12,
            pady=12,
            state="disabled"
        )
        self.chat.pack(
            fill=tk.BOTH,
            expand=True,
            padx=12,
            pady=(12, 0)
        )

        self.chat.tag_configure("user", foreground="#2458a6")
        self.chat.tag_configure("bot", foreground="#287544")

        self.add_message(
            "Бот",
            "Привет! Напиши сообщение или слово «помощь».",
            "bot"
        )

        self.entry.focus_set()

    def add_message(self, author, message, tag):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"{author}:\n", tag)
        self.chat.insert(tk.END, f"{message}\n\n")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def send_message(self, event=None):
        message = self.entry.get().strip()

        if not message:
            return

        self.entry.delete(0, tk.END)

        self.add_message("Ты", message, "user")
        answer = self.bot.reply(message)
        self.add_message("Бот", answer, "bot")

        self.entry.focus_set()

    def clear_chat(self):
        self.chat.configure(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state="disabled")

        self.add_message(
            "Бот",
            "Переписка очищена. Можем продолжать!",
            "bot"
        )
        self.entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
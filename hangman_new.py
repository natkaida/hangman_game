import tkinter as tk
import random
import json

class Hangman:
    def __init__(self, master):
        self.master = master
        master.title("Hangman Game")

        # Интерфейс игры
        self.frame = tk.Frame(master, padx=20, pady=20)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.button_new_game = tk.Button(self.frame, text="Новая игра", command=self.new_game, bg='lightblue')
        self.button_new_game.grid(row=1, column=0, pady=10)
        self.message_label = tk.Label(self.frame, text="", font=("Arial", 24))
        self.message_label.grid(row=2, column=0, pady=10)
        self.word_description_label = tk.Label(self.frame, text="", font=("Arial", 16))
        self.word_description_label.grid(row=3, column=0, pady=10)
        with open('words.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.words = data['words']
        self.word = ""
        self.word_display = ""
        self.remaining_guesses = 6
        self.guessed_letters = set()
        # Новая игра
        self.new_game()

    def new_game(self):
        # Обновление переменных
        self.message_label.config(text="") 
        word_data = random.choice(self.words)
        self.word = word_data['word']
        description = word_data['description']
        self.word_display = "-" * len(self.word)
        self.remaining_guesses = 6
        self.guessed_letters = set()
        self.canvas.delete("all")
        # Виселица
        self.canvas.create_line(50, 350, 150, 350)
        self.canvas.create_line(100, 350, 100, 50)
        self.canvas.create_line(100, 50, 200, 50)
        self.canvas.create_line(200, 50, 200, 100)
        # Скрытое слово
        self.canvas.create_text(300, 375, text=self.word_display, font=("Arial", 24), tags="word")
        # Попытки угадать буквы
        self.canvas.create_text(200, 300, text="Попытки:", font=("Arial", 16), tags="guessed_letters")
        # Описание слова
        self.word_description_label.config(text=description, font=("Arial", 12), fg="blue")

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        self.guessed_letters.add(letter)
        guessed_letters_str = " ".join(self.guessed_letters)
        self.canvas.itemconfig("guessed_letters", text=f"Попытки: {guessed_letters_str}")

        if letter not in self.word:
            self.remaining_guesses -= 1 
            #Рисование повешенного
            if self.remaining_guesses == 5:
                self.canvas.create_oval(180, 100, 220, 140)
            elif self.remaining_guesses == 4:
                self.canvas.create_line(200, 140, 200, 200)
            elif self.remaining_guesses == 3:
                self.canvas.create_line(200, 160, 180, 140)
            elif self.remaining_guesses == 2:
                self.canvas.create_line(200, 160, 220, 140)
            elif self.remaining_guesses == 1:
                self.canvas.create_line(200, 200, 180, 240)
            elif self.remaining_guesses == 0:
                self.canvas.create_line(200, 200, 220, 240)
                self.message_label.config(text=f"Вы проиграли! Было загадано слово {self.word}")
        else:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.word_display = self.word_display[:i] + letter + self.word_display[i+1:]
                    self.canvas.itemconfig("word", text=self.word_display)

        if self.word_display == self.word:
            self.message_label.config(text="Правильно!")


    def key_pressed(self, event):
        if event.char.isalpha():
            self.guess_letter(event.char.lower())

# Окно игры, обработка нажатий клавиш
root = tk.Tk()
hangman = Hangman(root)
root.bind("<Key>", hangman.key_pressed)
root.mainloop()


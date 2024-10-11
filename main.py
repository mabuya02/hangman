import random
import tkinter as tk
from tkinter import messagebox

words = ['python', 'java', 'kotlin', 'javascript', 'flask', 'django', 'react', 'angular', 'nodejs']

class HangmanGame:
    def __init__(self, main):
        self.root = main
        self.root.title("Hangman Game")
        self.root.geometry("500x600")
        self.root.config(bg="lightblue")

        self.root.bind("<Return>", lambda event: self.make_guess())
        self.root.bind("<r>", lambda event: self.reset_game())

        self.word = random.choice(words).lower()
        self.guessed_letters = set()
        self.wrong_attempts = 0
        self.max_attempts = 6

        self.canvas = tk.Canvas(self.root, width=200, height=250, bg="lightblue", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.title_label = tk.Label(self.root, text="Hangman Game", font=("Helvetica", 20, "bold"), bg="lightblue")
        self.title_label.pack(pady=10)

        self.word_display = tk.StringVar()
        self.word_display.set("_ " * len(self.word))
        self.word_label = tk.Label(self.root, textvariable=self.word_display, font=("Helvetica", 18), bg="lightblue")
        self.word_label.pack(pady=10)

        self.attempts_label = tk.Label(self.root, text=f"Wrong attempts left: {self.max_attempts}", font=("Helvetica", 14), bg="lightblue")
        self.attempts_label.pack(pady=10)

        self.letter_entry = tk.Entry(self.root, font=("Helvetica", 16), width=5)
        self.letter_entry.pack(pady=20)
        self.letter_entry.focus_set()

        self.guess_button = tk.Button(self.root, text="Guess", font=("Helvetica", 14), command=self.make_guess)
        self.guess_button.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Helvetica", 14), command=self.reset_game)
        self.reset_button.pack(pady=10)

        self.guessed_label = tk.Label(self.root, text="Guessed Letters: ", font=("Helvetica", 12), bg="lightblue")
        self.guessed_label.pack(pady=10)

        self.guessed_letters_display = tk.StringVar()
        self.guessed_letters_display.set("")
        self.guessed_label_display = tk.Label(self.root, textvariable=self.guessed_letters_display, font=("Helvetica", 12), bg="lightblue")
        self.guessed_label_display.pack()

        self.draw_gallows()

    def draw_gallows(self):
        self.canvas.create_line(50, 230, 150, 230, width=5)
        self.canvas.create_line(100, 230, 100, 50, width=5)
        self.canvas.create_line(100, 50, 150, 50, width=5)
        self.canvas.create_line(150, 50, 150, 80, width=5)

    def draw_hangman(self):
        if self.wrong_attempts == 1:
            self.canvas.create_oval(135, 80, 165, 110, width=3)
        elif self.wrong_attempts == 2:
            self.canvas.create_line(150, 110, 150, 170, width=3)
        elif self.wrong_attempts == 3:
            self.canvas.create_line(150, 120, 130, 150, width=3)
        elif self.wrong_attempts == 4:
            self.canvas.create_line(150, 120, 170, 150, width=3)
        elif self.wrong_attempts == 5:
            self.canvas.create_line(150, 170, 130, 210, width=3)
        elif self.wrong_attempts == 6:
            self.canvas.create_line(150, 170, 170, 210, width=3)

    def update_display_word(self):
        displayed_word = ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])
        self.word_display.set(displayed_word)

    def update_guessed_letters(self):
        self.guessed_letters_display.set(', '.join(sorted(self.guessed_letters)))

    def make_guess(self):
        guess = self.letter_entry.get().lower()
        self.letter_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed the letter '{guess}'")
            return

        self.guessed_letters.add(guess)
        self.update_guessed_letters()

        if guess in self.word:
            self.update_display_word()
            if set(self.word).issubset(self.guessed_letters):
                self.celebrate_win()
        else:
            self.wrong_attempts += 1
            self.attempts_label.config(text=f"Wrong attempts left: {self.max_attempts - self.wrong_attempts}")
            self.draw_hangman()
            if self.wrong_attempts == self.max_attempts:
                messagebox.showerror("Game Over", f"You lost! The word was: {self.word}")
                self.reset_game()

    def celebrate_win(self):
        self.root.config(bg="yellow")
        messagebox.showinfo("Congratulations!", f"You guessed the word: {self.word}! Well done!")
        self.reset_game()

    def reset_game(self):
        self.word = random.choice(words).lower()
        self.guessed_letters = set()
        self.wrong_attempts = 0
        self.word_display.set("_ " * len(self.word))
        self.attempts_label.config(text=f"Wrong attempts left: {self.max_attempts}")
        self.guessed_letters_display.set("")
        self.canvas.delete("all")
        self.draw_gallows()
        self.root.config(bg="lightblue")

root = tk.Tk()
game = HangmanGame(root)
root.mainloop()

import tkinter as tk
from tkinter import messagebox

WORD_LENGTH = 5
MAX_ATTEMPTS = 6


class WordGame:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Word Guess Game")
        self.root.geometry("700x600")

        self.show_menu()

        self.root.mainloop()

    def clear(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def show_menu(self):

        self.clear()

        title = tk.Label(
            self.root,
            text="WORD GUESS GAME",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=40)

        info = tk.Label(
            self.root,
            text="Player 1 enters a word\nPlayer 2 guesses",
            font=("Arial", 16)
        )
        info.pack()

        start_btn = tk.Button(
            self.root,
            text="Start",
            font=("Arial", 18),
            command=self.secret_word_screen
        )

        start_btn.pack(pady=30)

    def secret_word_screen(self):

        self.clear()

        title = tk.Label(
            self.root,
            text="Игрок 1",
            font=("Arial", 24)
        )
        title.pack(pady=20)

        label = tk.Label(
            self.root,
            text=f"Enter an English word ({WORD_LENGTH} letters)",
            font=("Arial", 14)
        )
        label.pack()

        self.secret_entry = tk.Entry(
            self.root,
            font=("Arial", 18),
            show="*"
        )
        self.secret_entry.pack(pady=20)

        btn = tk.Button(
            self.root,
            text="Continue",
            command=self.start_guessing
        )
        btn.pack()

    def start_guessing(self):

        word = self.secret_entry.get().lower()

        if len(word) != WORD_LENGTH:
            messagebox.showerror(
                "Error",
                f"Enter a word of {WORD_LENGTH} letters."
            )
            return

        if not word.isalpha():
            messagebox.showerror(
                "Error",
                "Only English letters."
            )
            return

        self.secret_word = word
        self.attempt = 0

        self.guess_screen()

    def guess_screen(self):

        self.clear()

        title = tk.Label(
            self.root,
            text="Player 2 guesses",
            font=("Arial", 24)
        )
        title.pack(pady=10)

        self.board = tk.Frame(self.root)
        self.board.pack(pady=20)

        self.rows = []

        for _ in range(MAX_ATTEMPTS):

            row = []

            frame = tk.Frame(self.board)
            frame.pack()

            for _ in range(WORD_LENGTH):

                lbl = tk.Label(
                    frame,
                    text="",
                    width=4,
                    height=2,
                    relief="solid",
                    font=("Arial", 18, "bold"),
                    bg="white"
                )

                lbl.pack(side="left", padx=2, pady=2)

                row.append(lbl)

            self.rows.append(row)

        self.entry = tk.Entry(
            self.root,
            font=("Arial", 18)
        )

        self.entry.pack(pady=15)

        btn = tk.Button(
            self.root,
            text="Проверить",
            font=("Arial", 14),
            command=self.check_guess
        )

        btn.pack()

    def check_guess(self):

        guess = self.entry.get().lower()

        if len(guess) != WORD_LENGTH:
            messagebox.showerror(
                "Error",
                f"{WORD_LENGTH} letters required."
            )
            return

        if not guess.isalpha():
            return

        row = self.rows[self.attempt]

        for i in range(WORD_LENGTH):

            letter = guess[i]

            row[i]["text"] = letter.upper()

            if letter == self.secret_word[i]:

                row[i]["bg"] = "green"
                row[i]["fg"] = "white"

            elif letter in self.secret_word:

                row[i]["bg"] = "gold"
                row[i]["fg"] = "black"

            else:

                row[i]["bg"] = "gray"
                row[i]["fg"] = "white"

        if guess == self.secret_word:

            messagebox.showinfo(
                "Victory",
                f"Word guessed in {self.attempt + 1} attempts!"
            )

            self.show_menu()
            return

        self.attempt += 1

        self.entry.delete(0, tk.END)

        if self.attempt >= MAX_ATTEMPTS:

            messagebox.showinfo(
                "Defeat",
                f"The word was: {self.secret_word.upper()}"
            )

            self.show_menu()


WordGame()
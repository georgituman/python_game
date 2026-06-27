import tkinter as tk
from tkinter import messagebox

WORD_LENGTH = 5
MAX_ATTEMPTS = 6

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GRAY = "#3a3a3c"
DARK = "#121213"
LIGHT = "#ffffff"
BORDER = "#565758"


class WordleDuel:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Wordle Duel")
        self.root.geometry("900x800")
        self.root.configure(bg=DARK)
        self.root.resizable(False, False)

        self.show_menu()

        self.root.mainloop()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- MENU ----------------

    def show_menu(self):

        self.clear_window()

        title = tk.Label(
            self.root,
            text="🟩 WORD CLASH 🟨",
            font=("Segoe UI", 30, "bold"),
            bg=DARK,
            fg=LIGHT
        )
        title.pack(pady=60)

        subtitle = tk.Label(
            self.root,
            text="Player 1 enters a secret word\nPlayer 2 tries to guess it",
            font=("Segoe UI", 14),
            bg=DARK,
            fg="lightgray"
        )
        subtitle.pack()

        tk.Button(
            self.root,
            text="Play",
            font=("Segoe UI", 16, "bold"),
            width=20,
            bg=GREEN,
            fg="white",
            relief="flat",
            command=self.secret_word_screen
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Rules",
            font=("Segoe UI", 16),
            width=20,
            bg=GRAY,
            fg="white",
            relief="flat",
            command=self.show_rules
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Exit",
            font=("Segoe UI", 16),
            width=20,
            bg="#8b0000",
            fg="white",
            relief="flat",
            command=self.root.destroy
        ).pack(pady=10)

    def show_rules(self):

        messagebox.showinfo(
            "Rules",
            f"""
    Player 1 enters a secret word.

    Player 2 tries to guess it.

    🟩 Green:
    Correct letter in the correct position.

    🟨 Yellow:
    Correct letter in the wrong position.

    ⬛ Gray:
    Letter is not in the word.

    Maximum attempts: {MAX_ATTEMPTS}
    """
        )

    # ---------------- SECRET WORD ----------------

    def secret_word_screen(self):

        self.clear_window()

        title = tk.Label(
            self.root,
            text="Player 1",
            font=("Segoe UI", 28, "bold"),
            bg=DARK,
            fg=LIGHT
        )
        title.pack(pady=40)

        tk.Label(
            self.root,
            text=f"Enter a secret {WORD_LENGTH}-letter word",
            font=("Segoe UI", 14),
            bg=DARK,
            fg=LIGHT
        ).pack()

        self.secret_entry = tk.Entry(
            self.root,
            font=("Consolas", 24),
            justify="center",
            show="*"
        )
        self.secret_entry.pack(pady=20)

        tk.Button(
            self.root,
            text="Start Game",
            font=("Segoe UI", 14, "bold"),
            bg=GREEN,
            fg="white",
            relief="flat",
            command=self.start_game
        ).pack()

    def start_game(self):

        word = self.secret_entry.get().lower().strip()

        if len(word) != WORD_LENGTH:
            messagebox.showerror(
                "Error",
                f"The word must contain exactly {WORD_LENGTH} letters."
            )
            return

        if not word.isalpha():
            messagebox.showerror(
                "Error",
                "Only English letters are allowed."
            )
            return

        self.secret_word = word
        self.attempt = 0

        self.show_game()

    # ---------------- GAME ----------------

    def show_game(self):

        self.clear_window()

        title = tk.Label(
            self.root,
            text="Player 2 is Guessing",
            font=("Segoe UI", 24, "bold"),
            bg=DARK,
            fg=LIGHT
        )
        title.pack(pady=10)

        self.attempt_label = tk.Label(
            self.root,
            text=f"Attempt 1 of {MAX_ATTEMPTS}",
            font=("Segoe UI", 12),
            bg=DARK,
            fg="lightgray"
        )

        self.attempt_label.pack()

        self.board = tk.Frame(self.root, bg=DARK)
        self.board.pack(pady=20)

        self.rows = []

        for _ in range(MAX_ATTEMPTS):

            frame = tk.Frame(self.board, bg=DARK)
            frame.pack()

            row = []

            for _ in range(WORD_LENGTH):

                cell = tk.Label(
                    frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Segoe UI", 24, "bold"),
                    bg=DARK,
                    fg=LIGHT,
                    relief="solid",
                    borderwidth=2
                )

                cell.pack(
                    side="left",
                    padx=4,
                    pady=4
                )

                row.append(cell)

            self.rows.append(row)

        self.guess_entry = tk.Entry(
            self.root,
            font=("Consolas", 22),
            justify="center"
        )

        self.guess_entry.pack(pady=15)

        self.guess_entry.focus()

        tk.Button(
            self.root,
            text="Submit Guess",
            font=("Segoe UI", 14, "bold"),
            bg=GREEN,
            fg="white",
            relief="flat",
            command=self.check_guess
        ).pack()

        self.create_keyboard()

    # ---------------- KEYBOARD ----------------

    def create_keyboard(self):

        keyboard_frame = tk.Frame(
            self.root,
            bg=DARK
        )

        keyboard_frame.pack(
            pady=20
        )

        self.keyboard_buttons = {}

        rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        for letters in rows:

            row_frame = tk.Frame(
                keyboard_frame,
                bg=DARK
            )

            row_frame.pack()

            for letter in letters:

                btn = tk.Label(
                    row_frame,
                    text=letter,
                    width=3,
                    height=1,
                    bg=GRAY,
                    fg="white",
                    font=("Segoe UI", 12, "bold")
                )

                btn.pack(
                    side="left",
                    padx=2,
                    pady=2
                )

                self.keyboard_buttons[letter] = btn

    # ---------------- CHECK ----------------

    def check_guess(self):

        guess = self.guess_entry.get().lower().strip()

        if len(guess) != WORD_LENGTH:
            messagebox.showerror(
                "Error",
                f"Please enter exactly {WORD_LENGTH} letters."
            )
            return

        row = self.rows[self.attempt]

        for i in range(WORD_LENGTH):

            letter = guess[i]

            row[i]["text"] = letter.upper()

            color = GRAY

            if letter == self.secret_word[i]:
                color = GREEN

            elif letter in self.secret_word:
                color = YELLOW

            row[i]["bg"] = color
            row[i]["fg"] = "white"

            key = self.keyboard_buttons.get(
                letter.upper()
            )

            if key:

                current = key["bg"]

                if color == GREEN:
                    key["bg"] = GREEN

                elif color == YELLOW and current != GREEN:
                    key["bg"] = YELLOW

                elif current not in (GREEN, YELLOW):
                    key["bg"] = GRAY

        if guess == self.secret_word:

            self.win_screen()
            return

        self.attempt += 1

        self.guess_entry.delete(0, tk.END)

        if self.attempt < MAX_ATTEMPTS:

            self.attempt_label.config(
                text=f"Attempt {self.attempt + 1} of {MAX_ATTEMPTS}"
            )

        else:

            self.lose_screen()

    # ---------------- WIN ----------------

    def win_screen(self):

        self.clear_window()

        tk.Label(
            self.root,
            text="🏆 YOU WIN!",
            font=("Segoe UI", 34, "bold"),
            bg=DARK,
            fg=GREEN
        ).pack(pady=50)

        tk.Label(
            self.root,
            text=f"The word was: {self.secret_word.upper()}",
            font=("Segoe UI", 18),
            bg=DARK,
            fg=LIGHT
        ).pack()

        tk.Label(
            self.root,
            text=f"Attempts used: {self.attempt + 1}",
            font=("Segoe UI", 14),
            bg=DARK,
            fg="lightgray"
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Main Menu",
            font=("Segoe UI", 14),
            bg=GREEN,
            fg="white",
            relief="flat",
            command=self.show_menu
        ).pack(pady=30)

    # ---------------- LOSE ----------------

    def lose_screen(self):

        self.clear_window()

        tk.Label(
            self.root,
            text="❌ GAME OVER",
            font=("Segoe UI", 34, "bold"),
            bg=DARK,
            fg="#ff4d4d"
        ).pack(pady=50)

        tk.Label(
            self.root,
            text=f"The correct word was: {self.secret_word.upper()}",
            font=("Segoe UI", 18),
            bg=DARK,
            fg=LIGHT
        ).pack()

        tk.Button(
            self.root,
            text="Main Menu",
            font=("Segoe UI", 14),
            bg=GREEN,
            fg="white",
            relief="flat",
            command=self.show_menu
        ).pack(pady=30)


WordleDuel()

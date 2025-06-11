import tkinter as tk
import random

# --- Стил и конфигурация ---
# Използваме речник за цветовете, за да може лесно да се променят
COLORS = {
    "background": "#eaf2f8",  # Светлосиньо
    "canvas_bg": "#ffffff",   # Бяло
    "text_dark": "#2c3e50",   # Тъмно сиво-синьо
    "text_light": "#34495e",  # По-светло сиво-синьо
    "accent_blue": "#3498db", # Ярко синьо
    "accent_green": "#2ecc71", # Зелено
    "accent_red": "#e74c3c",   # Червено
    "accent_orange": "#f39c12",# Оранжево
    "button_bg": "#3498db",
    "button_fg": "#ffffff",
    "button_hover": "#2980b9" # По-тъмно синьо за hover ефект
}

# Речник за шрифтове
FONTS = {
    "title": ("Helvetica", 44, "bold"),
    "body": ("Helvetica", 14),
    "used_letters": ("Consolas", 18, "bold"),
    "button": ("Helvetica", 14, "bold"),
    "message": ("Helvetica", 16, "italic")
}


class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Бесеница")
        self.master.geometry("800x800")
        self.master.config(bg=COLORS["background"])

        self.words = [
            "ПРОГРАМИРАНЕ", "КОМПЮТЪР", "ИНТЕРНЕТ", "БЪЛГАРИЯ", "СОФИЯ",
            "КНИГА", "УЧИЛИЩЕ", "ПРЕПОДАВАТЕЛ", "АВТОМОБИЛ", "КЪЩА",
            "СЛЪНЦЕ", "ЛУНА", "ЗВЕЗДА", "ПЛАНИНА", "МОРЕ", "АЗБУКА",
            "КЛАВИАТУРА", "ИНСТИТУТ", "УНИВЕРСИТЕТ", "БИБЛИОТЕКА"
        ]
        self.secret_word = ""
        self.guesses = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 7

        # Основна рамка, която да центрира съдържанието
        self.content_frame = tk.Frame(master, bg=COLORS["background"])
        self.content_frame.pack(expand=True)

        self.setup_widgets()
        self.new_game()

    def setup_widgets(self):
        # Canvas за рисуване на фигурата
        self.canvas = tk.Canvas(self.content_frame, width=400, height=350, bg=COLORS["canvas_bg"],
                                highlightthickness=1, highlightbackground=COLORS["text_light"])
        self.canvas.pack(pady=(0, 20))

        # Етикет за думата
        self.word_label = tk.Label(self.content_frame, text="", font=FONTS["title"], 
                                   bg=COLORS["background"], fg=COLORS["text_dark"])
        self.word_label.pack(pady=20)

        # Рамка за новия метод на въвеждане
        input_frame = tk.Frame(self.content_frame, bg=COLORS["background"])
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Въведи буква:", font=FONTS["body"], 
                 bg=COLORS["background"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=5)
        
        self.guess_entry = tk.Entry(input_frame, font=FONTS["body"], width=3, justify='center',
                                    bg=COLORS["canvas_bg"], fg=COLORS["text_dark"], bd=2, relief=tk.GROOVE)
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        self.guess_entry.bind("<Return>", self.process_guess_event)

        self.guess_button = tk.Button(input_frame, text="Познай", font=FONTS["button"], 
                                      bg=COLORS["button_bg"], fg=COLORS["button_fg"],
                                      command=self.process_guess, relief=tk.FLAT, padx=10)
        self.guess_button.pack(side=tk.LEFT, padx=5)
        self.guess_button.bind("<Enter>", self.on_button_enter)
        self.guess_button.bind("<Leave>", self.on_button_leave)

        # Етикети за показване на използваните букви
        tk.Label(self.content_frame, text="Използвани букви:", font=FONTS["body"],
                 bg=COLORS["background"], fg=COLORS["text_light"]).pack(pady=(20, 0))
        self.used_letters_label = tk.Label(self.content_frame, text="", font=FONTS["used_letters"], 
                                           bg=COLORS["background"], fg=COLORS["accent_blue"])
        self.used_letters_label.pack(pady=5)

        # Етикет за съобщения
        self.message_label = tk.Label(self.content_frame, text="", font=FONTS["message"], bg=COLORS["background"])
        self.message_label.pack(pady=5)

        # Бутон за нова игра
        self.new_game_button = tk.Button(self.content_frame, text="Нова игра", font=FONTS["button"], 
                                         bg=COLORS["accent_green"], fg=COLORS["button_fg"],
                                         command=self.new_game, relief=tk.FLAT, padx=20, pady=5)
        self.new_game_button.bind("<Enter>", lambda e: e.widget.config(bg="#27ae60")) # По-тъмно зелено
        self.new_game_button.bind("<Leave>", lambda e: e.widget.config(bg=COLORS["accent_green"]))

    # --- Функции за интерактивност на бутони ---
    def on_button_enter(self, event):
        event.widget.config(bg=COLORS["button_hover"])

    def on_button_leave(self, event):
        event.widget.config(bg=COLORS["button_bg"])

    # --- Функционалност на играта ---
    def process_guess_event(self, event):
        self.process_guess()

    def process_guess(self):
        if self.guess_button['state'] == tk.DISABLED:
            return

        guess = self.guess_entry.get().upper()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not 'А' <= guess <= 'Я':
            self.message_label.config(text="Моля, въведете една буква от азбуката.", fg=COLORS["accent_orange"])
            return
        
        if guess in self.guesses:
            self.message_label.config(text=f"Буквата '{guess}' вече е използвана.", fg=COLORS["accent_orange"])
            return
        
        self.message_label.config(text="")
        
        self.guesses.append(guess)
        self.update_used_letters_display()

        if guess not in self.secret_word:
            self.wrong_guesses += 1
            self.draw_hangman()

        self.update_word_display()
        self.check_game_over()

    def new_game(self):
        self.new_game_button.pack_forget()
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        self.guess_entry.focus_set()

        self.secret_word = random.choice(self.words)
        self.guesses = []
        self.wrong_guesses = 0
        
        self.update_word_display()
        self.update_used_letters_display()
        self.message_label.config(text="")
        self.draw_hangman()

    def update_word_display(self):
        displayed_word = " ".join([letter if letter in self.guesses else "_" for letter in self.secret_word])
        self.word_label.config(text=displayed_word)

    def update_used_letters_display(self):
        sorted_guesses = " ".join(sorted(self.guesses))
        self.used_letters_label.config(text=sorted_guesses)

    def check_game_over(self):
        game_over = False
        if self.wrong_guesses >= self.max_wrong_guesses:
            self.message_label.config(text=f"Край на играта! Думата беше: {self.secret_word}", fg=COLORS["accent_red"])
            game_over = True
        elif all(letter in self.guesses for letter in self.secret_word):
            self.message_label.config(text="Поздравления! Познахте думата!", fg=COLORS["accent_green"])
            game_over = True
        
        if game_over:
            self.guess_entry.config(state=tk.DISABLED)
            self.guess_button.config(state=tk.DISABLED)
            self.new_game_button.pack(pady=20)

    def draw_hangman(self):
        self.canvas.delete("all")
        line_color = COLORS["text_dark"]
        line_width = 4

        # Бесилка
        self.canvas.create_line(80, 320, 240, 320, width=line_width, fill=line_color)
        self.canvas.create_line(120, 320, 120, 80, width=line_width, fill=line_color)
        self.canvas.create_line(120, 80, 200, 80, width=line_width, fill=line_color)
        self.canvas.create_line(200, 80, 200, 120, width=line_width-1, fill=line_color)

        if self.wrong_guesses > 0:
            self.canvas.create_oval(180, 120, 220, 160, width=line_width-1, outline=line_color) # Глава
        if self.wrong_guesses > 1:
            self.canvas.create_line(200, 160, 200, 240, width=line_width-1, fill=line_color) # Тяло
        if self.wrong_guesses > 2:
            self.canvas.create_line(200, 180, 160, 210, width=line_width-1, fill=line_color) # Лява ръка
        if self.wrong_guesses > 3:
            self.canvas.create_line(200, 180, 240, 210, width=line_width-1, fill=line_color) # Дясна ръка
        if self.wrong_guesses > 4:
            self.canvas.create_line(200, 240, 170, 280, width=line_width-1, fill=line_color) # Ляв крак
        if self.wrong_guesses > 5:
            self.canvas.create_line(200, 240, 230, 280, width=line_width-1, fill=line_color) # Десен крак
        if self.wrong_guesses > 6:
            # Лице
            self.canvas.create_line(190, 135, 195, 140, width=2, fill=COLORS["accent_red"])
            self.canvas.create_line(195, 135, 190, 140, width=2, fill=COLORS["accent_red"])
            self.canvas.create_line(205, 135, 210, 140, width=2, fill=COLORS["accent_red"])
            self.canvas.create_line(210, 135, 205, 140, width=2, fill=COLORS["accent_red"])
            self.canvas.create_arc(190, 145, 210, 155, start=0, extent=-180, style=tk.ARC, width=2, outline=COLORS["accent_red"])

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
import tkinter as tk
from game import HangmanGame

if __name__ == "__main__":
    root = tk.Tk()
    game_instance = HangmanGame(root)
    root.mainloop()
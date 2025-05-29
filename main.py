import tkinter as tk
from tkinter import simpledialog
from interface import ChatApp

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    role = simpledialog.askstring("Papel", "Digite 's' para servidor ou 'c' para cliente:").strip().lower()
    root.deiconify()
    is_server = role == 's'
    app = ChatApp(root, is_server)
    root.mainloop()

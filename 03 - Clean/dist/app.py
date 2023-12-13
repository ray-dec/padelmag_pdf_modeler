import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import subprocess
import sys
import io

class Redirector(io.TextIOBase):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

def run_script():
    # Installation des dépendances sans afficher les sorties dans l'interface Tkinter
    subprocess.Popen(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Exécution du script principal
    with open('main.py', 'r', encoding='utf-8') as file:
        exec(file.read(), globals())

def start_script_thread():
    Thread(target=run_script).start()

# Création de l'interface graphique
if __name__ == "__main__":
    window = tk.Tk()

window.title("Classement Padel : Chargement des données")

text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=30)
text_area.pack()

# Redirection de stdout et stderr
sys.stdout = Redirector(text_area)
sys.stderr = Redirector(text_area)
start_button = tk.Button(window, text="Lancer le chargement", command=start_script_thread)
start_button.pack()
window.mainloop()
    
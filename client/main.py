import tkinter as tk
from gui import RansomwareGUI
import os

if __name__ == "__main__":
    # Créer le fichier example.txt avec du contenu de test
    file_path = 'example.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("Ceci est un fichier de test.")

    root = tk.Tk()
    app = RansomwareGUI(root)
    root.mainloop()

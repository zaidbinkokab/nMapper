import tkinter as tk
from gui import NetworkMappingApp

def main():
    root = tk.Tk()
    app = NetworkMappingApp(root)
    app.pack()
    root.mainloop()

if __name__ == "__main__":
    main()

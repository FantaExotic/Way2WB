from tkinter import Tk

class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title("Application")

        width = 500
        width_min = 400
        height = 400
        height_min = 300

        self.geometry(f"{width}x{height}")
        self.minsize(width=width_min, height=height_min)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
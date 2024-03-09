import tkinter as tk
import time

class ColorFlasher:
    def __init__(self, master):
        self.master = master
        master.title("Color Flasher")

        self.canvas = tk.Canvas(master, width=300, height=200)
        self.canvas.pack()

        self.color = "black"
        self.flashing = False
        self.frequency = 12.0  # Flashing frequency in Hz

        self.color_rect = self.canvas.create_rectangle(100, 50, 200, 150, fill=self.color)

        self.button = tk.Button(master, text="Start Flashing", command=self.toggle_flashing)
        self.button.pack()

    def toggle_flashing(self):
        if not self.flashing:
            self.flashing = True
            self.button.config(text="Stop Flashing")
            self.flash_color()
        else:
            self.flashing = False
            self.button.config(text="Start Flashing")

    def flash_color(self):
        if self.flashing:
            current_color = self.canvas.itemcget(self.color_rect, "fill")
            new_color = "white" if current_color == self.color else self.color
            self.canvas.itemconfig(self.color_rect, fill=new_color)
            self.master.after(int(1000 / self.frequency), self.flash_color)

root = tk.Tk()
color_flasher = ColorFlasher(root)
root.mainloop()
import tkinter as tk
import time

class FlashingColors:
    def __init__(self, master):
        self.master = master
        master.title("Flashing Colors")
        master.attributes("-fullscreen", True)

        self.colors = ["red", "green", "blue", "yellow"] # Icons / Colors that will flash
        self.frequencies = [1, 2, 3, 4]  # Frequencies (Hz) of each icon / color
        
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        quadrant_width = screen_width // 2
        quadrant_height = screen_height // 2

        self.labels = []
        for i in range(4):
            label = tk.Label(master, bg=self.colors[i], width=20, height=5)
            label.place(
                x=((i % 2) * quadrant_width) + (quadrant_width // 2),
                y=((i // 2) * quadrant_height) + (quadrant_height // 2),
                anchor=tk.CENTER
            )
            self.labels.append(label)

        self.entries = []
        for i in range(4):
            entry = tk.Entry(master)
            entry.place(
                x=((i % 2) * quadrant_width) + (quadrant_width // 2),
                y=((i // 2) * quadrant_height) + (quadrant_height // 2) + 50,
                anchor=tk.CENTER
            )
            entry.insert(0, str(self.frequencies[i]))
            self.entries.append(entry)

        self.flash()

    def flash(self):
        for i in range(4):
            frequency = float(self.entries[i].get())
            if time.time() % (1 / frequency) < 0.5 / frequency:
                self.labels[i].configure(bg=self.colors[i])
            else:
                self.labels[i].configure(bg="white")

        self.master.after(100, self.flash)

root = tk.Tk()
flashing_colors = FlashingColors(root)
root.mainloop()
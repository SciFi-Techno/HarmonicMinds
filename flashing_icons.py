import UnicornPy
import tkinter as tk
import time
import numpy as np

FrameLength = 1

def limitConsoleUpdateRate():
    """
    """
    consoleUpdateRate = int((UnicornPy.SamplingRate / FrameLength) / 25.0)
    if consoleUpdateRate == 0:
        consoleUpdateRate = 1
    return consoleUpdateRate

deviceList = UnicornPy.GetAvailableDevices(True)
device = UnicornPy.Unicorn(deviceList[0])
file = None  # Placeholder for the data file, will be opened later

# Acquisition must be started to create handle for GetNumberOfAcquiredChannels()
TestSignalEnabled = False
device.StartAcquisition(TestSignalEnabled)
numberOfAcquiredChannels = device.GetNumberOfAcquiredChannels()

# Create buffer for Unicorn BCI
receiveBufferBufferLength = FrameLength * numberOfAcquiredChannels * 4
receiveBuffer = bytearray(receiveBufferBufferLength)

class FlashingColors:
    def __init__(self, master):
        # Open device for Unicorn BCI

        self.master = master
        master.title("Flashing Colors")
        master.attributes("-fullscreen", True)

        self.colors = ["red", "green", "blue", "yellow"] # Icons / Colors that will flash
        self.frequencies = [1, 2, 3, 4]  # Frequencies (Hz) of each icon / color
        
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        quadrant_width = screen_width // 2
        quadrant_height = screen_height // 2

        # Main acquisition loop for Unicorn BCI
    user_duration = 1  # image display duration (in seconds)

    for i in range(0, int(user_duration * UnicornPy.SamplingRate / FrameLength)):
        device.GetData(FrameLength, receiveBuffer, receiveBufferBufferLength)

        data = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels * FrameLength)
        data = np.reshape(data, (FrameLength, numberOfAcquiredChannels))

        #for event in pygame.event.get():
        #    if event.type == QUIT:
        #        pygame.quit()
        #    if event.type == KEYDOWN:
        #        if event.key == K_ESCAPE:
        #            pygame.quit()

        # Add mind wandering condition to float array
        if len(data[0]) == 17:  # exclude if data is too large due to overwriting error
            data = np.append(data, [[0]], 1)

        # Open the file if it's not opened yet
        if file is None:
            ts = time.time()
            dataFile = '../data/recordings/combined_recording_' + str(int(ts)) + '.csv'
            os.makedirs(os.path.dirname(dataFile), exist_ok=True)
            file = open(dataFile, "ab")

        # Save Unicorn BCI data to csv
        np.savetxt(file, data, delimiter=',', fmt='%.3f', newline='\n')

    if i % limitConsoleUpdateRate() == 0:
        print(str(i) + " samples so far for Unicorn BCI.")

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
# Stop data acquisition for Unicorn BCI
device.StopAcquisition()
print()
print("Unicorn BCI data acquisition stopped.")
del receiveBuffer
if file is not None:
    file.close()

# End of the script
#drawText('Combined Script Complete. Press any key to quit.',
#         font,
#         windowSurface,
#         (WINDOWWIDTH / 2),
#         (WINDOWHEIGHT / 5))
#pygame.display.update()
#waitForPlayerToPressKey()
#pygame.quit()
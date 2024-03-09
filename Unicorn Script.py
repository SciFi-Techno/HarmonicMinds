import UnicornPy
import tkinter as tk
import time
import numpy as np
import csv

class FlashingColors:
    def __init__(self, master):
        # Open device for Unicorn BCI
        self.master = master
        master.title("Flashing Colors")
        master.attributes("-fullscreen", True)
        self.colors = ["red", "green", "blue", "yellow"] # Icons / Colors that will flash
        self.frequencies = [9, 11, 13, 15]  # Frequencies (Hz) of each icon / color
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        quadrant_width = screen_width // 2
        quadrant_height = screen_height // 2
        self.labels = []
        self.acquisition_started = False
        self.start_time = time.time()
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
        if time.time() - self.start_time < 120:  # Check if 2 minutes have passed
            for i in range(4):
                frequency = float(self.entries[i].get())
                if time.time() % (1 / frequency) < 0.5 / frequency:
                    self.labels[i].configure(bg=self.colors[i])
                else:
                    self.labels[i].configure(bg="white")
            self.master.after(100, self.flash)
    def acquire_data(self, device, FrameLength, receiveBuffer, receiveBufferBufferLength, numberOfAcquiredChannels):
        user_duration = 1  # image display duration (in seconds)
        for i in range(0, int(user_duration * UnicornPy.SamplingRate / FrameLength)):
            device.GetData(FrameLength, receiveBuffer, receiveBufferBufferLength)
            #data = np.append(data, [[0]], 1)
            data = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels * FrameLength)
            data = np.reshape(data, (FrameLength, numberOfAcquiredChannels))
            # Add extra condition to float array
            #if len(data[0]) == 17:
            # Open the file if it's not opened yet
            if file is None:
                ts = time.time()
                dataFile = 'data' + 'baseline' + '.csv'
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

def main():
    # Specifications for the data acquisition.
    #-------------------------------------------------------------------------------------
    TestsignaleEnabled = False;
    FrameLength = 1;
    AcquisitionDurationInSeconds = 120;
    DataFile = "data_baseline.csv";

    print("Unicorn Acquisition Example")
    print("---------------------------")
    print()

    try:
        # Get available devices.
        #-------------------------------------------------------------------------------------

        # Get available device serials.
        deviceList = UnicornPy.GetAvailableDevices(True)

        if len(deviceList) <= 0 or deviceList is None:
            raise Exception("No device available.Please pair with a Unicorn first.")

        # Print available device serials.
        print("Available devices:")
        i = 0
        for device in deviceList:
            print("#%i %s" % (i,device))
            i+=1

        # Request device selection.
        print()
        deviceID = int(input("Select device by ID #"))
        if deviceID < 0 or deviceID > len(deviceList):
            raise IndexError('The selected device ID is not valid.')

        # Open selected device.
        #-------------------------------------------------------------------------------------
        print()
        print("Trying to connect to '%s'." %deviceList[deviceID])
        device = UnicornPy.Unicorn(deviceList[deviceID])
        print("Connected to '%s'." %deviceList[deviceID])
        print()

        # Create a file to store data.
        file = open(DataFile, "wb")

        # Initialize acquisition members.
        #-------------------------------------------------------------------------------------
        numberOfAcquiredChannels= device.GetNumberOfAcquiredChannels()
        configuration = device.GetConfiguration()

        # Print acquisition configuration
        print("Acquisition Configuration:");
        print("Sampling Rate: %i Hz" %UnicornPy.SamplingRate);
        print("Frame Length: %i" %FrameLength);
        print("Number Of Acquired Channels: %i" %numberOfAcquiredChannels);
        print("Data Acquisition Length: %i s" %AcquisitionDurationInSeconds);
        print();

        # Allocate memory for the acquisition buffer.
        receiveBufferBufferLength = FrameLength * numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(receiveBufferBufferLength)

        # Create a new Tkinter window
        root = tk.Tk()

        # Create an instance of the FlashingColors class
        flashing_colors = FlashingColors(root)

        # Start the flashing colors
        flashing_colors.flash()

        try:
            # Start data acquisition.
            #-------------------------------------------------------------------------------------
            device.StartAcquisition(TestsignaleEnabled)
            print("Data acquisition started.")
            flashing_colors.acquisition_started = True

            # Calculate number of get data calls.
            numberOfGetDataCalls = int(AcquisitionDurationInSeconds * UnicornPy.SamplingRate / FrameLength);
        
            # Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
            consoleUpdateRate = int((UnicornPy.SamplingRate / FrameLength) / 25.0);
            if consoleUpdateRate == 0:
                consoleUpdateRate = 1

            # Acquisition loop.
            #-------------------------------------------------------------------------------------
            start_time = time.time()
            for i in range (0,numberOfGetDataCalls):
                # Check if 2 minutes have passed
                if time.time() - start_time >= AcquisitionDurationInSeconds:
                    break

                # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
                device.GetData(FrameLength,receiveBuffer,receiveBufferBufferLength)
            
                # Write data to file.
                #data = [float(x) for x in receiveBuffer]
                #csv_writer.writerow(data)
                data = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels * FrameLength)
                data = np.reshape(data, (FrameLength, numberOfAcquiredChannels))
                np.savetxt(file,data,delimiter=',',fmt='%.3f',newline='\n')

                # Update console to indicate that the data acquisition is running.
                if i % consoleUpdateRate == 0:
                    print('.',end='',flush=True)
                
                root.update()

            # Stop data acquisition.
            #-------------------------------------------------------------------------------------
            device.StopAcquisition();
            print()
            print("Data acquisition stopped.");

        except UnicornPy.DeviceException as e:
            print(e)
        except Exception as e:
            print("An unknown error occured. %s" %e)
        finally:
            # release receive allocated memory of receive buffer
            del receiveBuffer

            #close file
            file.close()

            # Close device.
            #-------------------------------------------------------------------------------------
            del device
            print("Disconnected from Unicorn")
        root.mainloop()

    except UnicornPy.DeviceException as e:
        print(e)
    except Exception as e:
        print("An unknown error occured. %s" %e)

    input("\n\nPress ENTER key to exit")

#execute main
main()

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data
data = pd.read_csv('data.csv', header=None)

# Plot each column
for column in data.columns:
    plt.plot(data[column])

plt.show()
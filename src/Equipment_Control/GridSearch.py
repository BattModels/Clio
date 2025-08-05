import numpy as np
import csv
EC_range = (50, 60, 1)
LiPF6_range = [1, 1.1, 1.2, 1.3, 1.4, 1.5]
compositions = []
for EC in np.arange(EC_range[0], EC_range[1] + EC_range[2], EC_range[2]).tolist():
    for LiPF6 in LiPF6_range:
        compositions.append(f"EC_EMC|{EC}_{100 - EC}|LiPF6|{np.round(LiPF6, 1)}")

csv_file = 'Targets.csv'

# Write the list to a CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(compositions)
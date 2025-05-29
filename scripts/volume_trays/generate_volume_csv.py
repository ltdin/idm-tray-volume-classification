import os
import csv

dataset_path = "../volume_trays/volume_dataset/"  
output_csv = "../volume_trays/csv/volume_labels.csv"

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['filename', 'label']) 

    for volume_folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, volume_folder)

        if not os.path.isdir(folder_path):
            continue

        try:
            label = float(volume_folder.split('_')[-1])
        except ValueError:
            print(f"[SKIP]: Skip invalid file {volume_folder}")
            continue

        for fname in os.listdir(folder_path):
            if fname.lower().endswith('.png'):
                writer.writerow([f"{volume_folder}/{fname}", label])

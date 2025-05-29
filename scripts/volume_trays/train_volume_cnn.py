import os
import csv
import pandas as pd
import numpy as np  
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.utils import Sequence
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.callbacks import EarlyStopping


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
            print(f"[SKIP]: Skip invalid folder {volume_folder}")
            continue
        for fname in os.listdir(folder_path):
            if fname.lower().endswith('.png'):
                writer.writerow([f"{volume_folder}/{fname}", label])

class TrayVolumeDataset(Sequence):
    def __init__(self, dataframe, img_dir, batch_size=16, img_size=(224, 224)):
        self.data = dataframe.reset_index(drop=True)
        self.img_dir = img_dir
        self.batch_size = batch_size
        self.img_size = img_size

    def __len__(self):
        return int(np.ceil(len(self.data) / self.batch_size))

    def __getitem__(self, idx):
        batch = self.data.iloc[idx * self.batch_size : (idx + 1) * self.batch_size]
        images, labels = [], []
        for _, row in batch.iterrows():
            img_path = os.path.join(self.img_dir, row["filename"])
            img = load_img(img_path, target_size=self.img_size)
            img = img_to_array(img) / 255.0
            images.append(img)
            labels.append(float(row["label"]) / 100.0)  # Normalize to [0, 1]
        return np.array(images), np.array(labels)

csv_path = "../volume_trays/csv/volume_labels.csv"
img_dir = "../volume_trays/volume_dataset/"
df = pd.read_csv(csv_path)

train_df, temp_df = train_test_split(
    df, test_size=0.3, random_state=42, stratify=df["label"]
)

val_df, test_df = train_test_split(
    temp_df, test_size=0.5, random_state=42, stratify=temp_df["label"]
)


train_dataset = TrayVolumeDataset(train_df, img_dir)
val_dataset = TrayVolumeDataset(val_df, img_dir)
test_dataset = TrayVolumeDataset(test_df, img_dir)

model = Sequential([
    layers.Input(shape=(224, 224, 3)),
    
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.GlobalAveragePooling2D(),
    
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid') 
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

early_stop = EarlyStopping(patience=5, restore_best_weights=True)
history = model.fit(train_dataset, validation_data=val_dataset, epochs=50)

import json
with open("volume_train_history.json", "w") as f:
    json.dump(history.history, f)
    
model.save("volume_cnn_model.h5")

loss, mae = model.evaluate(test_dataset)
print(f"Test Loss: {loss:.4f}, Test MAE: {mae:.4f}")

img_path = "../volume_trays/volume_dataset/volume_60/IMG_7841.png"
img = load_img(img_path, target_size=(224, 224))
img = img_to_array(img) / 255.0
img = np.expand_dims(img, axis=0)

pred = model.predict(img)
volume_percent = float(pred[0][0]) * 100
print(f"Predicted tray volume: {volume_percent:.2f}%")

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
import json 

# CONFIG
CSV_PATH = "../volume_trays/csv/volume_labels.csv"
IMG_DIR = "../volume_trays/dataset_preprocessed"
IMG_SIZE = (224, 224)
BATCH_SIZE = 8
EPOCHS = 100

# Data Generator
class TrayVolumeDataset(Sequence):
    def __init__(self, dataframe, img_dir, batch_size=8, img_size=(224, 224)):
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
            img = img_to_array(img)
            img = preprocess_input(img) 
            images.append(img)
            labels.append(float(row["label"]) / 100.0)
        return np.array(images), np.array(labels)

# Load data 
df = pd.read_csv(CSV_PATH)
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df["label"])
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df["label"])

train_dataset = TrayVolumeDataset(train_df, IMG_DIR, batch_size=BATCH_SIZE, img_size=IMG_SIZE)
val_dataset = TrayVolumeDataset(val_df, IMG_DIR, batch_size=BATCH_SIZE, img_size=IMG_SIZE)
test_dataset = TrayVolumeDataset(test_df, IMG_DIR, batch_size=BATCH_SIZE, img_size=IMG_SIZE)

# Build model with MobileNetV2
base_model = MobileNetV2(include_top=False, weights='imagenet', input_tensor=Input(shape=(224, 224, 3)))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(64, activation='relu')(x)
out = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=out)

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train
early_stop = EarlyStopping(patience=50, restore_best_weights=True)
history = model.fit(train_dataset, validation_data=val_dataset, epochs=EPOCHS, callbacks=[early_stop])

# Save history
with open("volume_mobilenetv2_history.json", "w") as f:
    json.dump(history.history, f)

# Save + Evaluate
model.save("../../weights/volume_mobilenetv2_model.h5")
loss, mae = model.evaluate(test_dataset)
print(f"Test Loss: {loss:.4f}, Test MAE: {mae:.4f}")

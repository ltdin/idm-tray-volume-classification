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
import datetime
from database import versions_collection


# CONFIG
CSV_PATH = "../../../scripts/IDM Tray Counting/volume_trays/csv/volume_labels.csv"
IMG_DIR = "../../../scripts/IDM Tray Counting/volume_trays/dataset_preprocessed"
MODEL_SAVE_PATH = "../../../weights/volume_mobilenetv2_model.h5"
IMG_SIZE = (224, 224)
BATCH_SIZE = 8
EPOCHS = 1

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

def retrain_cnn_model(version_name, version_dir):
    print("Starting CNN retraining...")

    # Check CSV exists
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"[ERROR] CSV file not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    if df.empty:
        raise ValueError("[ERROR] CSV file is empty.")

    train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df["label"])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df["label"])

    train_dataset = TrayVolumeDataset(train_df, IMG_DIR, batch_size=BATCH_SIZE, img_size=IMG_SIZE)
    val_dataset = TrayVolumeDataset(val_df, IMG_DIR, batch_size=BATCH_SIZE, img_size=IMG_SIZE)
    test_dataset = TrayVolumeDataset(test_df, IMG_DIR, batch_size=BATCH_SIZE, img_size=IMG_SIZE)

    base_model = MobileNetV2(include_top=False, weights='imagenet', input_tensor=Input(shape=(224, 224, 3)))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(64, activation='relu')(x)
    out = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=out)

    model.compile(
        optimizer='adam',
        loss='mean_squared_error',
        metrics=['mae']
    )

    patience = min(5, EPOCHS // 2) if EPOCHS < 10 else 50
    early_stop = EarlyStopping(patience=patience, restore_best_weights=True)

    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=EPOCHS,
        callbacks=[early_stop]
    )

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    history_filename = os.path.join(
        version_dir,
        f"volume_mobilenetv2_history_{timestamp}.json"
    )
    with open(history_filename, "w") as f:
        json.dump(history.history, f)

    cnn_model_path = os.path.join(
        version_dir,
        "volume_mobilenetv2_model.h5"
    )
    model.save(cnn_model_path)
    print(f"[OK] Saved CNN model and history.")

    versions_collection.update_one(
        {"version_name": version_name},
        {
            "$set": {
                "cnn_metrics": history.history,
                "files.cnn_model": cnn_model_path,
                "files.cnn_history_json": history_filename
            }
        }
    )
    print(f"[OK] Updated CNN metrics in MongoDB for version {version_name}.")

    print("[OK] CNN retraining completed.")


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model = load_model("../../weights/volume_cnn_model.h5")

csv_path = "../volume_trays/csv/volume_labels.csv"
img_dir = "../volume_trays/volume_dataset/"
df = pd.read_csv(csv_path)
sample_df = df.sample(10, random_state=42)

fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(12, 18))
axes = axes.flatten()  

for i, (_, row) in enumerate(sample_df.iterrows()):
    img_path = os.path.join(img_dir, row["filename"])
    img = load_img(img_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_batch)[0][0] * 100
    true = row["label"]

    axes[i].imshow(img)
    axes[i].set_title(f"True: {true:.0f}%, Predicted: {pred:.2f}%", fontsize=10, pad=8)
    axes[i].axis("off")

for j in range(i + 1, len(axes)):
    axes[j].axis("off")

fig.suptitle("Predicted vs True Volume on Test Samples", fontsize=16)
plt.tight_layout(pad=3.0, rect=[0, 0.03, 1, 0.97])
plt.show()

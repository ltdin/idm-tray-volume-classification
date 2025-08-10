import json
import matplotlib.pyplot as plt

file_path = '../volume_trays/volume_efficientnetb0_history.json'

with open(file_path, 'r') as f:
    history = json.load(f)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(history['loss'], label='Training Loss')
plt.plot(history['val_loss'], label='Validation Loss')
plt.title('Model Loss over Epochs (EfficientNetB0)')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plot MAE
plt.subplot(1, 2, 2)
plt.plot(history['mae'], label='Training MAE')
plt.plot(history['val_mae'], label='Validation MAE')
plt.title('Model MAE over Epochs (EfficientNetB0)')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend()
plt.tight_layout()
plt.show()

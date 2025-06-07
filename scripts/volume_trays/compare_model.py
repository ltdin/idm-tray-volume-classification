import json

# Define your model names and their history files
model_files = {
    "EfficientNetB0": "volume_efficientnetb0_history.json",
    "MobileNetV2": "volume_mobilenetv2_history.json",
    "ResNet50": "volume_resnet50_history.json" 
}

summary_results = []

for model_name, file_path in model_files.items():
    with open(file_path, "r") as f:
        hist = json.load(f)

    best_val_mae = min(hist["val_mae"])
    best_epoch = hist["val_mae"].index(best_val_mae)
    best_train_mae = hist["mae"][best_epoch]
    best_loss = hist["val_loss"][best_epoch]
    total_epochs = len(hist["mae"])

    summary_results.append({
        "model": model_name,
        "epochs": total_epochs,
        "best_epoch": best_epoch,
        "val_mae": best_val_mae,
        "train_mae": best_train_mae,
        "val_loss": best_loss
    })

# Print comparison table
print(f"{'Model':<15}{'Epochs':<8}{'Best@':<8}{'Val MAE':<10}{'Train MAE':<12}{'Val Loss':<10}")
print("-" * 63)
for r in summary_results:
    print(f"{r['model']:<15}{r['epochs']:<8}{r['best_epoch']:<8}{r['val_mae']:<10.4f}{r['train_mae']:<12.4f}{r['val_loss']:<10.4f}")

# Highlight best MAE
best_model = min(summary_results, key=lambda x: x["val_mae"])
print(f"\n✅ Best model based on lowest validation MAE: {best_model['model']} ({best_model['val_mae']:.4f})")

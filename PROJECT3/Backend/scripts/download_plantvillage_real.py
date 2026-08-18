"""
Real PlantVillage Dataset Downloader
Downloads and prepares actual PlantVillage dataset from Kaggle
"""
import os
import zipfile
import requests
from pathlib import Path
import shutil
from tqdm import tqdm
import json

# Paths
DATA_DIR = "./data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
TRAIN_DIR = os.path.join(PROCESSED_DIR, "train")
VAL_DIR = os.path.join(PROCESSED_DIR, "validation")
TEST_DIR = os.path.join(PROCESSED_DIR, "test")

# Direct download URL for PlantVillage dataset
KAGGLE_DATASET = "arjuntejaswi/plant-village"
DATASET_ZIP = os.path.join(RAW_DIR, "plantvillage.zip")

def create_directories():
    """Create necessary directories"""
    for directory in [RAW_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print(" Directories created successfully")

def download_with_kaggle_api():
    """
    Download dataset using Kaggle API
    Requires: pip install kaggle
    Setup: Place kaggle.json in ~/.kaggle/ or %USERPROFILE%\.kaggle\
    """
    try:
        import kaggle
        print("📥 Downloading PlantVillage dataset from Kaggle...")
        print(f"   Dataset: {KAGGLE_DATASET}")
        
        # Download dataset
        kaggle.api.dataset_download_files(
            KAGGLE_DATASET,
            path=RAW_DIR,
            unzip=True
        )
        
        print("✅ Dataset downloaded and extracted successfully!")
        return True
        
    except ImportError:
        print("❌ Kaggle API not installed. Install with: pip install kaggle")
        return False
    except Exception as e:
        print(f"❌ Error downloading from Kaggle: {e}")
        print("\n📝 Manual Setup Instructions:")
        print("   1. Go to https://www.kaggle.com/datasets/arjuntejaswi/plant-village")
        print("   2. Click 'Download' button")
        print("   3. Extract the zip to:", os.path.abspath(RAW_DIR))
        return False

def split_dataset(source_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Split dataset into train/val/test sets
    """
    import random
    
    print("\n📊 Splitting dataset...")
    
    # Find the PlantVillage directory
    plantvillage_dirs = [
        os.path.join(source_dir, d) for d in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, d)) and 'plant' in d.lower()
    ]
    
    if not plantvillage_dirs:
        # Check if we're already in the right directory
        disease_classes = [
            d for d in os.listdir(source_dir)
            if os.path.isdir(os.path.join(source_dir, d)) and '___' in d
        ]
        if disease_classes:
            plantvillage_dir = source_dir
        else:
            print(f"❌ Could not find PlantVillage classes in {source_dir}")
            return
    else:
        plantvillage_dir = plantvillage_dirs[0]
    
    print(f"   Source: {plantvillage_dir}")
    
    # Get all disease classes
    disease_classes = [
        d for d in os.listdir(plantvillage_dir)
        if os.path.isdir(os.path.join(plantvillage_dir, d))
    ]
    
    print(f"   Found {len(disease_classes)} disease classes")
    
    total_images = 0
    train_count = 0
    val_count = 0
    test_count = 0
    
    for disease_class in disease_classes:
        class_path = os.path.join(plantvillage_dir, disease_class)
        
        # Get all images
        images = [
            f for f in os.listdir(class_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        
        if len(images) == 0:
            print(f"   ⚠️  No images in {disease_class}, skipping...")
            continue
        
        # Shuffle
        random.shuffle(images)
        
        # Calculate splits
        total = len(images)
        train_size = int(total * train_ratio)
        val_size = int(total * val_ratio)
        
        train_images = images[:train_size]
        val_images = images[train_size:train_size + val_size]
        test_images = images[train_size + val_size:]
        
        # Create directories
        for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
            Path(os.path.join(split_dir, disease_class)).mkdir(parents=True, exist_ok=True)
        
        # Copy images
        for img in train_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(TRAIN_DIR, disease_class, img)
            shutil.copy2(src, dst)
        
        for img in val_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(VAL_DIR, disease_class, img)
            shutil.copy2(src, dst)
        
        for img in test_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(TEST_DIR, disease_class, img)
            shutil.copy2(src, dst)
        
        total_images += total
        train_count += len(train_images)
        val_count += len(val_images)
        test_count += len(test_images)
        
        print(f"   ✓ {disease_class:40s} | Total: {total:5d} | Train: {len(train_images):4d} | Val: {len(val_images):4d} | Test: {len(test_images):4d}")
    
    print(f"\n✅ Dataset split completed!")
    print(f"   Total images: {total_images}")
    print(f"   Training:     {train_count} ({train_count/total_images*100:.1f}%)")
    print(f"   Validation:   {val_count} ({val_count/total_images*100:.1f}%)")
    print(f"   Test:         {test_count} ({test_count/total_images*100:.1f}%)")
    
    # Save split statistics
    stats = {
        'total_images': total_images,
        'total_classes': len(disease_classes),
        'train_count': train_count,
        'val_count': val_count,
        'test_count': test_count,
        'disease_classes': disease_classes
    }
    
    with open(os.path.join(PROCESSED_DIR, 'dataset_stats.json'), 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n📝 Statistics saved to: {os.path.join(PROCESSED_DIR, 'dataset_stats.json')}")

def verify_dataset():
    """Verify that dataset is properly set up"""
    print("\n🔍 Verifying dataset...")
    
    for split_name, split_dir in [('Train', TRAIN_DIR), ('Val', VAL_DIR), ('Test', TEST_DIR)]:
        if not os.path.exists(split_dir):
            print(f"   ❌ {split_name} directory not found")
            continue
        
        classes = [d for d in os.listdir(split_dir) if os.path.isdir(os.path.join(split_dir, d))]
        total_images = sum(
            len([f for f in os.listdir(os.path.join(split_dir, c)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            for c in classes
        )
        
        print(f"   ✓ {split_name:12s} | Classes: {len(classes):2d} | Images: {total_images:5d}")
    
    print("\n✅ Dataset verification complete!")

if __name__ == "__main__":
    print("="*70)
    print("🌱 PlantVillage Dataset Downloader & Preparer")
    print("="*70)
    
    # Create directories
    create_directories()
    
    print("\n" + "="*70)
    print("STEP 1: Download Dataset")
    print("="*70)
    
    # Check if PlantVillage folder already exists
    plantvillage_check = os.path.join(RAW_DIR, "PlantVillage")
    if os.path.exists(plantvillage_check):
        print("✅ PlantVillage dataset already exists!")
        print(f"   Location: {os.path.abspath(plantvillage_check)}")
        download_success = True
    else:
        # Try to download with Kaggle API
        download_success = download_with_kaggle_api()
        
        if not download_success:
            print("\n⚠️  Automatic download failed. Please download manually:")
            print("   1. Install Kaggle API: pip install kaggle")
            print("   2. Setup Kaggle credentials:")
            print("      - Go to https://www.kaggle.com/account")
            print("      - Click 'Create New API Token'")
            print("      - Place kaggle.json in: %USERPROFILE%\\.kaggle\\ (Windows)")
            print("   3. Run this script again")
            print("\n   OR download manually and extract to:", os.path.abspath(RAW_DIR))
            exit(1)
    
    print("\n" + "="*70)
    print("STEP 2: Split Dataset")
    print("="*70)
    
    # Find and split dataset
    split_dataset(RAW_DIR)
    
    print("\n" + "="*70)
    print("STEP 3: Verify Dataset")
    print("="*70)
    
    verify_dataset()
    
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print(f"\n📁 Dataset Location:")
    print(f"   Train:      {os.path.abspath(TRAIN_DIR)}")
    print(f"   Validation: {os.path.abspath(VAL_DIR)}")
    print(f"   Test:       {os.path.abspath(TEST_DIR)}")
    print(f"\n🚀 Next Step: Run training script")
    print(f"   python ml_models/train_mobilenetv2_disease_model.py")

"""
Install required packages for MobileNetV2 training
"""
import subprocess
import sys

def install_packages():
    """Install all required packages"""
    
    packages = [
        'tensorflow>=2.13.0',
        'tensorflow-hub>=0.14.0',
        'pillow>=10.0.0',
        'numpy>=1.24.0',
        'scikit-learn>=1.3.0',
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
        'tqdm>=4.65.0',
        'kaggle>=1.5.16'
    ]
    
    print("="*70)
    print("📦 Installing ML Training Dependencies")
    print("="*70)
    
    for package in packages:
        print(f"\n📥 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
    
    print("\n" + "="*70)
    print("✅ Installation Complete!")
    print("="*70)
    
    print("\n📝 Next Steps:")
    print("   1. Setup Kaggle API credentials")
    print("      - Go to https://www.kaggle.com/account")
    print("      - Click 'Create New API Token'")
    print("      - Place kaggle.json in %USERPROFILE%\\.kaggle\\")
    print("   2. Download dataset:")
    print("      python scripts/download_plantvillage_real.py")
    print("   3. Train model:")
    print("      python ml_models/train_mobilenetv2_disease_model.py")
    print("   4. Test model:")
    print("      python ml_models/test_mobilenetv2_model.py")

if __name__ == "__main__":
    install_packages()

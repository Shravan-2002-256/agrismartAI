# ⚡ QUICK SETUP - AI DEPENDENCIES
# Install all required packages for Real AI implementation
# Run this script: python install_ai_dependencies.py

"""
AgriSmart AI - Production Dependencies Installer
Installs all required packages for real AI features
"""

import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def install_package(package):
    """Install a single package"""
    try:
        logger.info(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        logger.info(f"✅ {package} installed")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all AI dependencies"""
    logger.info("=" * 60)
    logger.info("🚀 AGRISMART AI - PRODUCTION SETUP")
    logger.info("=" * 60)
    
    packages = [
        # Core ML
        "tensorflow==2.15.0",
        "tensorflow-hub==0.15.0",
        
        # Database
        "pymongo==4.6.0",
        "motor==3.3.2",
        
        # Time Series
        "prophet==1.1.5",
        
        # RAG & Embeddings
        "sentence-transformers==2.3.1",
        "langchain-community==0.0.38",
        "langchain-core==0.1.23",
        
        # Utilities
        "pandas>=2.0.0",
        "numpy>=2.0.0",
        "pillow>=11.0.0",
        "opencv-python>=4.12.0"
    ]
    
    success_count = 0
    fail_count = 0
    
    for package in packages:
        if install_package(package):
            success_count += 1
        else:
            fail_count += 1
    
    logger.info("\n" + "=" * 60)
    logger.info(f"✅ Installed: {success_count} packages")
    if fail_count > 0:
        logger.info(f"❌ Failed: {fail_count} packages")
    logger.info("=" * 60)
    
    if fail_count == 0:
        logger.info("\n🎉 ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
        logger.info("\n📋 Next Steps:")
        logger.info("1. Configure MongoDB connection in .env file")
        logger.info("2. Run: python test_ai_services.py")
        logger.info("3. Start backend: python run.py")
    else:
        logger.info("\n⚠️  Some packages failed. Please install manually.")

if __name__ == "__main__":
    main()

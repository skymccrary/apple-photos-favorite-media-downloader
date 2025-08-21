# 💙 Apple Photos Favorite Media Downloader

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Effortlessly bulk download your favorited photos and videos from Apple Photos with chronological organization**

Automatically download all your hearted (💙) photos and videos from Apple Photos on macOS within a specified date range. Perfect for creating backups, organizing media for video editing, or simply accessing your favorite memories offline.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🔧 Requirements](#-requirements)
- [⚡ Installation](#-installation)
- [🚀 Usage](#-usage)
- [📁 Output](#-output)
- [⚠️ Important Notes](#️-important-notes)
- [👤 Author](#-author)
- [📄 License](#-license)

---

## ✨ Features

- 🎯 **Smart Filtering**: Downloads only your favorited (hearted) photos and videos
- 📅 **Date Range Support**: Specify custom date ranges for targeted downloads
- 📱 **Live Photos Support**: Exports Live Photos as both photos and videos separately
- 🏷️ **Chronological Naming**: Automatically renames files with sequential numbering for easy organization
- 📊 **Progress Tracking**: Visual progress bar shows download status
- ☁️ **iCloud Integration**: Automatically downloads media from iCloud if not stored locally
- 🎬 **Video Editor Ready**: File naming optimized for importing into video editing software

---

## 🔧 Requirements

- **Operating System**: macOS (required for Apple Photos integration)
- **Python**: Python 3.6 or higher
- **Storage**: Sufficient disk space for your favorited media
- **Apple Photos**: Desktop application with your photo library

> **💡 Note**: Media not stored locally will be automatically downloaded from iCloud during the process

---

## ⚡ Installation

1. **Install Python dependencies** using pip:

```bash
python3 -m pip install osxphotos tqdm
```

2. **Download the script**:
   - Clone this repository or download `apple_photos_favorite_media_downloader.py`

3. **Make the script executable** (optional):

```bash
chmod +x apple_photos_favorite_media_downloader.py
```

---

## 🚀 Usage

### Step 1: Prepare Your Media
Before running the script, make sure you have favorited (hearted 💙) the photos and videos you want to download in your Apple Photos library. You can do this from:
- Your iPhone Photos app
- Your Mac Photos app
- iCloud Photos on the web

### Step 2: Run the Script
Open Terminal and navigate to the script location, then run:

```bash
python3 apple_photos_favorite_media_downloader.py
```

### Step 3: Enter Date Range
The script will prompt you for a date range:

```
Start date (mm-dd-yyyy, or press Enter to use today's date): 01-01-2024
End date (mm-dd-yyyy, or press Enter to use today's date): 01-31-2024
```

**💡 Pro Tips:**
- For best performance, limit your date range to shorter timeframes (e.g., 1 month)
- Press Enter without typing to use today's date as default
- Use format: `mm-dd-yyyy` (e.g., `04-30-2025`)

### Step 4: Wait for Download
The script will:
1. 🔍 Search your Apple Photos library for favorited media in the specified range
2. 📊 Display a progress bar showing download status
3. 💾 Save files to your Desktop with chronological naming

---

## 📁 Output

### Location
Your downloaded media will be saved to your Desktop in a folder named:
```
mm-dd-yyyy to mm-dd-yyyy
```

### File Naming Convention
Files are automatically renamed with a chronological numbering system:
```
001_MMYYYY-MMYYYY.jpg
002_MMYYYY-MMYYYY.mp4
003_MMYYYY-MMYYYY.heic
...
```

This naming convention ensures:
- ✅ Files remain in chronological order
- ✅ Easy import into video editing software
- ✅ No naming conflicts
- ✅ Clear date range identification

### File Types
The script preserves original file formats and exports:
- 📷 **Photos**: JPEG, HEIC, PNG, etc.
- 🎥 **Videos**: MP4, MOV, etc.
- 🌟 **Live Photos**: Exported as both photo and video files

---

## ⚠️ Important Notes

> **🚨 Storage Warning**: Ensure you have sufficient storage space on your Mac. Media not stored locally will be downloaded from iCloud during the process, which may take additional time and bandwidth.

> **⏱️ Performance Tip**: For large photo libraries, consider limiting your date range to shorter periods (1-3 months) for optimal performance.

> **🔐 Privacy**: This script only accesses your local Apple Photos database and does not send any data externally.

---

## 👤 Author

**Sky McCrary**  
🔗 GitHub: [@skymccrary](https://github.com/skymccrary)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with 💙 for Apple Photos users**

*Happy downloading! 📸✨*

</div>

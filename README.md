# Apple Photos Favorite Media Downloader 💙
skymccrary | https://github.com/skymccrary

## Description
Bulk-downloads favorited (hearted) items from the Apple Photos app on macOS for a chosen date range. Live Photos are saved as a still HEIC image and a separate .mov video.

## Requirements
- macOS with the Photos app and an existing Photos library
- Python 3
- Python packages: `osxphotos`, `tqdm`


How to run:
1. Save this code on your Desktop and run the script in Terminal (from VS Code terminal, recommended)

2. Install dependencies via terminal:
python3 -m pip install osxphotos tqdm

3. Run script in VS Code terminal, Apple will prompt to Allow script to access photos (yes obviously), and will open the Photos app on MacOS.

4. Input a month-year to pull all the <3'd media from that month. Ex: november-2025

5. Media will be exported to your Desktop folder
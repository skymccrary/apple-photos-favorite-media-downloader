# Apple Photos Favorite Media Downloader 💙
skymccrary | https://github.com/skymccrary

## Description
Bulk-downloads favorited (hearted) items from the Apple Photos app on macOS for a chosen date range. Live Photos are saved as a still HEIC image and a separate .mov video.

## Requirements
- macOS with the Photos app and an existing Photos library
- Python 3
- Python packages: `osxphotos`, `tqdm`


How to run:

1. Install dependencies via terminal:
python3 -m pip install osxphotos tqdm

2. open Photos app on a Mac

3. Run script in terminal, Apple will prompt to Allow script to access photos (yes obviously).

4. Insert a range for hearted media, recommend only 1 month at a time for best results.

5. Media will be exported to your Desktop folder
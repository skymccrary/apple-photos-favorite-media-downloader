# Apple Photos Favorite Media Downloader 💙
skymccrary | https://github.com/skymccrary

# Description:
Apple Photos Favorite Media Downloader 💙 automatically bulk downloads your favorited (hearted) photos and videos from your Apple Photos desktop application on macOS, within specified date range. Also includes Live Photos saved separately as both photos and videos.

# How to use:
1. Prepare dependencies:
- macOS and Python 3 required
- Ensure you have enough storage on your Mac, as targeted media in range not on local machine will be downloaded from Apple iCloud in Apple Photos and then copied locally as well.
- Install osxphotos and tqdm with the following terminal command: *python3 -m pip install osxphotos tqdm*

2. Prepare target media:
- Favorite (heart 💙) pictures in your Apple Photos library from your iPhone or Mac; these are the pictures that will be downloaded.

3. Run it:
- From macOS terminal, run: apple_photos_favorite_media_downloader.py
- Input date range (for best results, limit results to shorter timeframe; e.g. 1 month).
- You will find your downloaded media on your Desktop in a folder named "mm-dd-yyyy to mm-dd-yyyy".
- Photos will be renamed when they are downloaded, with a naming convention that keeps them chronological for easy import into video editor.

hello

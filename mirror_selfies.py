#!!!
# This script is not to be ran independently; it is called by apple_photos_favorites.py
#!!!
import os
import subprocess
import argparse
from datetime import datetime

def download_favorites(destination_folder, use_hardlinks=False, verbose=False):
    """Download favorite media from Apple Photos"""
    
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mirror_script_path = os.path.join(script_dir, 'mirror_selfies.py')
    
    # Check if mirror script exists
    if not os.path.exists(mirror_script_path):
        print(f"Error: mirror_selfies.py not found at {mirror_script_path}")
        return
    
    # Check if ffmpeg is installed for video mirroring
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: ffmpeg not found. Video mirroring will not work.")
        print("Install with: brew install ffmpeg")
    
    print(f"Starting download of favorite media to: {destination_folder}")
    
    # Create export command
    export_command = [
        'osxphotos', 'export', destination_folder,
        '--favorite',
        '--download-missing',
        '--cleanup',
        '--directory', '{created.year}/{created.month}',
        '--filename', '{original_name}',
        '--live',  # Export live photos with video
        '--post-function', f'{mirror_script_path}::mirror_selfie_if_needed'
    ]
    
    if use_hardlinks:
        export_command.append('--hardlink')
    
    if verbose:
        export_command.append('--verbose')
    
    # Run the export command
    try:
        result = subprocess.run(export_command, check=True, text=True)
        print("Download completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during download: {e}")
        return
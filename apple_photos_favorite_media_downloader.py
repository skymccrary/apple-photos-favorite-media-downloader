import os
import osxphotos
from pathlib import Path
from tqdm import tqdm
from datetime import datetime, time
import sys
import time
import shutil
import logging
import subprocess
import argparse
from PIL import Image
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def validate_date(date_str):
    # Validate date string in mm-dd-yyyy format and return datetime object
    try:
        date_obj = datetime.strptime(date_str, "%m-%d-%Y")
        # Return date with time set to midnight (start of day)
        return date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    except ValueError:
        raise ValueError("Date must be in mm-dd-yyyy format (e.g., 04-30-2025)")

def get_date_range():
    # Prompt user for start and end dates and return datetime objects
    logging.info("Enter date range for hearted photos/videos (mm-dd-yyyy). Start date is required, end date is optional.")
    # Select date range of hearted photos/videos to download
    start_date_str = input("Start date (mm-dd-yyyy): ").strip()
    end_date_str = input("End date (mm-dd-yyyy, or press Enter to use today's date): ").strip()

    if not start_date_str:
        raise ValueError("Start date is required.")

    start_date = validate_date(start_date_str)
    
    # Handle end date - use today if no input provided
    if not end_date_str:
        end_date = datetime.now()
    else:
        end_date = validate_date(end_date_str)
    
    # Set end date to end of day (23:59:59.999999)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    if start_date > end_date:
        raise ValueError("Start date must be before or equal to end date.")

    return start_date, end_date

def check_if_mirrored(original_path, edited_path):
    """Check if an edited image is a mirrored version of the original"""
    try:
        # Load both images
        original = Image.open(original_path)
        edited = Image.open(edited_path)
        
        # Convert to RGB if necessary (to handle different modes)
        if original.mode != 'RGB':
            original = original.convert('RGB')
        if edited.mode != 'RGB':
            edited = edited.convert('RGB')
        
        # Convert to arrays
        original_arr = np.array(original)
        edited_arr = np.array(edited)
        
        # Check if dimensions match
        if original_arr.shape != edited_arr.shape:
            return False
            
        # Flip the original and compare
        original_flipped = np.array(original.transpose(Image.FLIP_LEFT_RIGHT))
        
        # Calculate similarity (allowing for minor compression differences)
        difference = np.mean(np.abs(edited_arr.astype(float) - original_flipped.astype(float)))
        
        # If difference is small, it's likely mirrored
        return difference < 30  # Threshold for similarity
        
    except Exception:
        return False

def check_if_mirrored_optimized(original_path, edited_path):
    """Optimized check if an edited image is mirrored - uses sampling"""
    try:
        # Only check images, not videos
        if not any(original_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.heic', '.tiff']):
            return False
            
        original = Image.open(original_path)
        edited = Image.open(edited_path)
        
        # Quick dimension check first
        if original.size != edited.size:
            return False
        
        # Sample instead of full image - resize to small size for comparison
        sample_size = (200, 200)
        original_small = original.resize(sample_size, Image.Resampling.LANCZOS)
        edited_small = edited.resize(sample_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if original_small.mode != 'RGB':
            original_small = original_small.convert('RGB')
        if edited_small.mode != 'RGB':
            edited_small = edited_small.convert('RGB')
        
        # Compare smaller versions
        original_arr = np.array(original_small)
        edited_arr = np.array(edited_small)
        original_flipped = np.array(original_small.transpose(Image.FLIP_LEFT_RIGHT))
        
        difference = np.mean(np.abs(edited_arr.astype(float) - original_flipped.astype(float)))
        
        return difference < 30
        
    except Exception:
        return False

def mirror_media(filepath, media_type, verbose=False):
    """Mirror different types of media files"""
    try:
        filename = os.path.basename(filepath)
        
        # Handle images
        if media_type in ['image', 'heic']:
            img = Image.open(filepath)
            mirrored = img.transpose(Image.FLIP_LEFT_RIGHT)
            mirrored.save(filepath)
            if verbose:
                print(f"Mirrored image: {filename}")
                
        # Handle videos (including MOV files from Live Photos)
        elif media_type == 'video' or filepath.lower().endswith(('.mov', '.mp4')):
            # Create temp file for output
            temp_output = filepath + '.temp.mp4'
            
            # Use ffmpeg to mirror video
            cmd = [
                'ffmpeg', '-i', filepath,
                '-vf', 'hflip',  # Horizontal flip filter
                '-c:a', 'copy',  # Copy audio without re-encoding
                '-y',  # Overwrite output
                temp_output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Replace original with mirrored version
                shutil.move(temp_output, filepath)
                if verbose:
                    print(f"Mirrored video: {filename}")
            else:
                if verbose:
                    print(f"Failed to mirror video {filename}: {result.stderr}")
                if os.path.exists(temp_output):
                    os.remove(temp_output)
                    
    except Exception as e:
        if verbose:
            print(f"Error mirroring {filepath}: {e}")

def mirror_selfie_if_needed(photo, filepath, verbose):
    """Mirror selfie media (images, videos, live photos) if not already mirrored"""
    if not photo.selfie:
        return
        
    try:
        # Determine media type
        media_type = photo.uti_original
        if media_type:
            media_type = media_type.lower()
        
        # Check if we should skip mirroring for edited photos
        if photo.edited and photo.path_original:
            # Only check for images, videos can't easily be checked
            if any(filepath.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.heic', '.tiff']):
                if check_if_mirrored_optimized(photo.path_original, filepath):
                    if verbose:
                        print(f"Selfie already mirrored, skipping: {os.path.basename(filepath)}")
                    return
        
        # Mirror the media file
        if photo.islive:
            # Live Photo - need to handle both image and video components
            mirror_media(filepath, 'image', verbose)
            
            # Check for associated .mov file
            base_name = os.path.splitext(filepath)[0]
            possible_mov_files = [
                base_name + '.mov',
                base_name + '.MOV',
                filepath.replace('.HEIC', '.MOV'),
                filepath.replace('.heic', '.mov')
            ]
            
            for mov_file in possible_mov_files:
                if os.path.exists(mov_file):
                    mirror_media(mov_file, 'video', verbose)
                    break
        else:
            # Regular photo or video
            if any(filepath.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.heic', '.tiff']):
                mirror_media(filepath, 'image', verbose)
            elif any(filepath.lower().endswith(ext) for ext in ['.mov', '.mp4', '.m4v']):
                mirror_media(filepath, 'video', verbose)
                
    except Exception as e:
        if verbose:
            print(f"Error processing {filepath}: {e}")

def download_hearted_media(output_folder, date_range):
    output_path = Path(output_folder).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)

    # Format date suffix once, reuse throughout
    date_suffix = f"_{date_range[0].strftime('%m%Y')}-{date_range[1].strftime('%m%Y')}"

    photosdb = osxphotos.PhotosDB()
    photos_in_range = photosdb.photos(from_date=date_range[0], to_date=date_range[1])
    favorites = sorted([p for p in photos_in_range if p.favorite], key=lambda x: x.date)

    logging.info(f"Found {len(favorites)} favorited items in the specified date range.")

    # Check if ffmpeg is installed for video mirroring
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: ffmpeg not found. Video mirroring will not work.")
        print("Install with: brew install ffmpeg")
    
    # Create export command
    export_command = [
        'osxphotos', 'export', str(output_path),
        '--favorite',
        '--download-missing',
        '--cleanup',
        '--directory', '{created.year}/{created.month}',
        '--filename', '{original_name}',
        '--live',  # Ensure Live Photos are exported properly
        '--post-function', f'{__file__}::mirror_selfie_if_needed'
    ]

    # Export each favorited item with progress bar
    for index, photo in enumerate(tqdm(favorites, desc="Progress"), start=1):
        try:
            # Get original extension
            _, ext = os.path.splitext(photo.original_filename)
            # Create sequential filename with padded numbers and date range
            new_filename = f"{index:03d}{date_suffix}{ext}"
            
            # Export the original photo/video
            export_info = photo.export(
                dest=str(output_path),
                filename=new_filename,
                live_photo=True,  # This ensures Live Photo components are exported
                use_photos_export=True
            )
            logging.info(f"Exported image: {new_filename}")

            # Handle Live Photo video component
            if photo.live_photo:
                # Get the video component path
                video_path = photo.path_live_photo
                if video_path and os.path.exists(video_path):
                    # Create filename for Live Photo video
                    live_photo_filename = f"{index:03d}{date_suffix}_live.mov"
                    live_photo_export_path = output_path / live_photo_filename
                    
                    # Copy the Live Photo video component
                    shutil.copy2(video_path, live_photo_export_path)
                    logging.info(f"Exported Live Photo video: {live_photo_filename}")
                else:
                    logging.warning(f"Live Photo video component not found for: {new_filename}")

        except Exception as e:
            logging.error(f"Failed to export {new_filename}: {str(e)}")

def animate_loading():
    # Simplified animation with same visual effect
    dots = ['', '.', '..', '...']
    for _ in range(3):
        for d in dots:
            print(f'\rSearching media in Apple Photos{d}', end='', flush=True)
            time.sleep(0.3)

def main():
    try:
        date_range = get_date_range()
        
        # Simplified output folder creation
        output_folder = "~/Desktop/{} to {}".format(
            date_range[0].strftime("%m-%d-%Y"),
            "present" if not date_range[1] else date_range[1].strftime("%m-%d-%Y")
        )
        
        animate_loading()
        print('\n')
        
        logging.info(f"Exporting <3'd media to {output_folder}")
        download_hearted_media(output_folder, date_range)
        logging.info("Export complete.")
        
    except ValueError as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

import os
import osxphotos
from pathlib import Path
from tqdm import tqdm
from datetime import datetime, time
import sys
import time
import shutil

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
    print("Enter date range for hearted photos/videos (mm-dd-yyyy). Start date is required, end date is optional.")
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

def download_hearted_media(output_folder, date_range):
    output_path = Path(output_folder).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)

    # Format date suffix once, reuse throughout
    date_suffix = f"_{date_range[0].strftime('%m%Y')}-{date_range[1].strftime('%m%Y')}"

    photosdb = osxphotos.PhotosDB()
    photos_in_range = photosdb.photos(from_date=date_range[0], to_date=date_range[1])
    favorites = sorted([p for p in photos_in_range if p.favorite], key=lambda x: x.date)

    print(f"Found {len(favorites)} favorited items in the specified date range.")

    # Export each favorited item with progress bar
    for index, photo in enumerate(tqdm(favorites, desc="Progress"), start=1):
        # Get original extension
        _, ext = os.path.splitext(photo.original_filename)
        # Create sequential filename with padded numbers and date range
        new_filename = f"{index:03d}{date_suffix}{ext}"
        export_path = output_path / new_filename

        try:
            # Export the original media
            photo.export(dest=str(output_path), filename=new_filename, use_photos_export=True)
            print(f"Exported image: {new_filename}")

            # Check if the photo has a Live Photo video
            if photo.live_photo and photo.path_live_photo:
                # Define export path for the Live Photo video with same sequential number
                live_photo_filename = f"{index:03d}{date_suffix}_live.mov"
                live_photo_export_path = output_path / live_photo_filename

                # Copy the Live Photo video
                shutil.copy2(photo.path_live_photo, live_photo_export_path)
                print(f"Exported Live Photo video: {live_photo_filename}")

        except Exception as e:
            print(f"Failed to export {new_filename}: {e}")

def animate_loading():
    # Simplified animation with same visual effect
    dots = ['', '.', '..', '...']
    for _ in range(3):
        for d in dots:
            print(f'\rSearching photos{d}', end='', flush=True)
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
        
        print(f"Exporting <3'd media to {output_folder}")
        download_hearted_media(output_folder, date_range)
        print("Export complete.")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

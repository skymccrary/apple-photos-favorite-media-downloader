import os
import osxphotos
from pathlib import Path
from tqdm import tqdm
from datetime import datetime, time
import sys
import time
import shutil
import logging
import calendar
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def validate_month_year(month_year_str):
    # Validate month-year string and return datetime objects for start and end of month
    try:
        # Parse input like "september-2023" or "September-2023"
        parts = month_year_str.lower().split('-')
        if len(parts) != 2:
            raise ValueError("Invalid format")
        
        month_name, year_str = parts
        year = int(year_str)
        
        # Convert month name to month number
        month_names = {month.lower(): idx for idx, month in enumerate(calendar.month_name) if month}
        if month_name not in month_names:
            raise ValueError("Invalid month name")
        
        month = month_names[month_name]
        
        # Get first day of month at midnight
        start_date = datetime(year, month, 1, 0, 0, 0, 0)
        
        # Get last day of month at end of day
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59, 999999)
        
        return start_date, end_date
    except (ValueError, IndexError):
        raise ValueError("Format must be month-year (e.g., september-2023, January-2024)")

def get_date_range():
    # Prompt user for month and year and return datetime objects for the full month
    logging.info("Enter the month-year for hearted photos/videos to download.")
    logging.info("Format: month-year (e.g., september-2023, January-2024)")
    
    month_year_str = input("<3 media downloader is running!\ninput month-year (ex: november-2025): ").strip()
    
    if not month_year_str:
        raise ValueError("Month and year are required.")
    
    start_date, end_date = validate_month_year(month_year_str)
    
    logging.info(f"Processing full month: {start_date.strftime('%B %Y')}")
    logging.info(f"Date range: {start_date.strftime('%m-%d-%Y')} to {end_date.strftime('%m-%d-%Y')}")
    
    # Ask about excluding still images for Live Photos
    exclude_stills_input = input("\nExclude still images if photo is Live, Y/N? ").strip().upper()
    while exclude_stills_input not in ['Y', 'N']:
        exclude_stills_input = input("Please enter Y or N: ").strip().upper()
    
    exclude_stills = (exclude_stills_input == 'Y')
    if exclude_stills:
        logging.info("Live Photos: Will download only video component (still image excluded)")
    else:
        logging.info("Live Photos: Will download both video and still image")
    
    return start_date, end_date, exclude_stills

def download_hearted_media(output_folder, date_range, exclude_stills=False, stop_event=None):
    output_path = Path(output_folder).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)

    # Format date suffix once, reuse throughout
    date_suffix = f"_{date_range[0].strftime('%m%Y')}-{date_range[1].strftime('%m%Y')}"

    try:
        photosdb = osxphotos.PhotosDB()
    except Exception as e:
        if stop_event:
            stop_event.set()
        logging.error(f"Failed to open Photos database: {str(e)}")
        logging.error("This may be due to macOS version compatibility issues with osxphotos.")
        logging.error("Try updating osxphotos: pip3 install --upgrade osxphotos")
        sys.exit(1)
    
    photos_in_range = photosdb.photos(from_date=date_range[0], to_date=date_range[1])
    favorites = sorted([p for p in photos_in_range if p.favorite], key=lambda x: x.date)

    # Stop the animation once we have the photos loaded
    if stop_event:
        stop_event.set()
        time.sleep(0.4)  # Give animation time to complete current cycle
        print('\r' + ' ' * 80 + '\r', end='', flush=True)  # Clear the animation line

    logging.info(f"Found {len(favorites)} favorited items in the specified date range.")

    # Export each favorited item with progress bar
    for index, photo in enumerate(tqdm(favorites, desc="Progress"), start=1):
        try:
            # Get original extension
            _, ext = os.path.splitext(photo.original_filename)
            base_name = f"{index:03d}{date_suffix}"

            # Requested naming:
            #   - Still image (HEIC) ends with 'b'
            #   - Live Photo video (.mov) ends with 'a'
            image_filename = f"{base_name}b{ext}"
            live_video_filename = f"{base_name}a.mov"

            # Determine if we should export the still image
            should_export_still = not (exclude_stills and photo.live_photo)

            # Export the still image unless it's a Live Photo and we're excluding stills
            if should_export_still:
                export_results = photo.export(
                    dest=str(output_path),
                    filename=image_filename,
                    live_photo=False,
                    use_photos_export=True,
                )

                logging.info(
                    f"Exported image for index {index:03d}: {image_filename}"
                )

            # Ensure Live Photo video is present with the requested 'a' suffix
            if photo.live_photo:
                video_path = photo.path_live_photo
                if video_path and os.path.exists(video_path):
                    target_video_path = output_path / live_video_filename
                    shutil.copy2(video_path, target_video_path)
                    logging.info(
                        f"Exported Live Photo video for index {index:03d}: {live_video_filename}"
                    )
                else:
                    logging.warning(
                        f"Live Photo video component not found for index {index:03d}"
                    )

        except Exception as e:
            logging.error(f"Failed to export media for index {index:03d}: {str(e)}")

def animate_loading():
    # Simplified animation with same visual effect
    dots = ['', '.', '..', '...']
    for _ in range(3):
        for d in dots:
            print(f'\rSearching media in Apple Photos{d}', end='', flush=True)
            time.sleep(0.3)

def main():
    try:
        start_date, end_date, exclude_stills = get_date_range()
        date_range = (start_date, end_date)
        
        # Create output folder with month-year format
        output_folder = "~/Desktop/{}".format(
            date_range[0].strftime("%B-%Y")
        )
        
        animate_loading()
        print('\n')
        
        # Start continuous animation in background thread
        stop_animation = threading.Event()
        
        def continuous_animation():
            dots = ['', '.', '..', '...']
            while not stop_animation.is_set():
                for d in dots:
                    if stop_animation.is_set():
                        break
                    print(f"\rExporting <3'd media to {output_folder}, please wait{d}", end='', flush=True)
                    time.sleep(0.3)
        
        animation_thread = threading.Thread(target=continuous_animation, daemon=True)
        animation_thread.start()
        
        download_hearted_media(output_folder, date_range, exclude_stills, stop_animation)
        animation_thread.join(timeout=1)  # Wait for animation thread to finish
        
        # Expand the output folder path to show the full location
        expanded_path = Path(output_folder).expanduser()
        month_year_display = date_range[0].strftime('%B-%Y')
        logging.info(f"Export complete.\nDownloaded media from {month_year_display} is located in {expanded_path}")
        
    except ValueError as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

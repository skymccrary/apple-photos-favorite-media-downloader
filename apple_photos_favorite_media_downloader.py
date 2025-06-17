import sys
import time
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def validate_date(date_str):
    # Validate date string in mm-dd-yyyy format and return datetime object
@@ -18,7 +25,7 @@ def validate_date(date_str):

def get_date_range():
    # Prompt user for start and end dates and return datetime objects
    print("Enter date range for hearted photos/videos (mm-dd-yyyy). Start date is required, end date is optional.")
    logging.info("Enter date range for hearted photos/videos (mm-dd-yyyy). Start date is required, end date is optional.")
    # Select date range of hearted photos/videos to download
    start_date_str = input("Start date (mm-dd-yyyy): ").strip()
    end_date_str = input("End date (mm-dd-yyyy, or press Enter to use today's date): ").strip()
@@ -53,7 +60,7 @@ def download_hearted_media(output_folder, date_range):
    photos_in_range = photosdb.photos(from_date=date_range[0], to_date=date_range[1])
    favorites = sorted([p for p in photos_in_range if p.favorite], key=lambda x: x.date)

    print(f"Found {len(favorites)} favorited items in the specified date range.")
    logging.info(f"Found {len(favorites)} favorited items in the specified date range.")

    # Export each favorited item with progress bar
    for index, photo in enumerate(tqdm(favorites, desc="Progress"), start=1):
@@ -70,7 +77,7 @@ def download_hearted_media(output_folder, date_range):
                live_photo=True,  # This ensures Live Photo components are exported
                use_photos_export=True
            )
            print(f"Exported image: {new_filename}")
            logging.info(f"Exported image: {new_filename}")

            # Handle Live Photo video component
            if photo.live_photo:
@@ -83,12 +90,12 @@ def download_hearted_media(output_folder, date_range):

                    # Copy the Live Photo video component
                    shutil.copy2(video_path, live_photo_export_path)
                    print(f"Exported Live Photo video: {live_photo_filename}")
                    logging.info(f"Exported Live Photo video: {live_photo_filename}")
                else:
                    print(f"Live Photo video component not found for: {new_filename}")
                    logging.warning(f"Live Photo video component not found for: {new_filename}")

        except Exception as e:
            print(f"Failed to export {new_filename}: {str(e)}")
            logging.error(f"Failed to export {new_filename}: {str(e)}")

def animate_loading():
    # Simplified animation with same visual effect
@@ -111,12 +118,12 @@ def main():
        animate_loading()
        print('\n')

        print(f"Exporting <3'd media to {output_folder}")
        logging.info(f"Exporting <3'd media to {output_folder}")
        download_hearted_media(output_folder, date_range)
        print("Export complete.")
        logging.info("Export complete.")

    except ValueError as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}")Add commentMore actions
        sys.exit(1)

if __name__ == "__main__":

from glob import glob
import os
import pandas as pd
from sqlalchemy.exc import IntegrityError
from core.database import SessionLocal
from models.influencer import Influencer
from services.data_normalizer import normalize_influencer

def detect_platform(filename):
    """
    Detect platform from filename.
    """
    filename = filename.lower()
    # Check filename for platform keywords and return the matching platform name
    if "instagram" in filename:
        return "Instagram"
    if "tiktok" in filename:
        return "TikTok"
    if "youtube" in filename:
        return "YouTube"
    # Default if no known platform keyword is found
    return "Unknown"

def load_dataframe(file_path):
    """
    Load CSV files.
    Skip TXT for now.
    """
    # Only load the file if it's a CSV; otherwise skip it (returns None)
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    return None

def main():
    # Open a new database session
    db = SessionLocal()
    # Get all files in the raw data directory
    files = glob("data/raw/*")

    # Counters to track import results
    imported = 0
    skipped = 0
    errors = 0

    print(f"\nFound {len(files)} files.\n")

    # Process each file found in the directory
    for file in files:
        # Skip any non-CSV files
        if not file.endswith(".csv"):
            print(f"Skipping {os.path.basename(file)}")
            continue

        print(f"\nProcessing: {os.path.basename(file)}")
        try:
            # Load the CSV into a DataFrame
            df = load_dataframe(file)
            if df is None:
                continue

            # Determine which platform this file's data belongs to
            platform = detect_platform(file)

            # Iterate over each row in the CSV
            for _, row in df.iterrows():
                # Normalize/clean the raw row data into a consistent format
                data = normalize_influencer(row, platform)

                # Skip rows with no username (invalid/unusable data)
                if not data["username"]:
                    skipped += 1
                    continue

                # Check if this influencer already exists in the database (avoid duplicates)
                existing = (
                    db.query(Influencer)
                    .filter_by(
                        username=data["username"],
                        platform=platform,
                    )
                    .first()
                )
                if existing:
                    skipped += 1
                    continue

                # Build a new Influencer record from the normalized data
                influencer = Influencer(
                    username=data["username"],
                    full_name=data["full_name"],
                    platform=data["platform"],
                    category=data["category"],
                    followers=data["followers"],
                    avg_likes=data["avg_likes"],
                    avg_comments=data["avg_comments"],
                )
                # Stage the new influencer for insertion
                db.add(influencer)
                try:
                    # Commit the new record to the database
                    db.commit()
                    imported += 1
                except IntegrityError:
                    # Roll back if a database constraint fails (e.g. duplicate/unique conflict)
                    db.rollback()
                    skipped += 1
        except Exception as e:
            # Catch and log any unexpected errors per file, without stopping the whole import
            print(f"Error processing {file}")
            print(e)
            errors += 1

    # Close the database session once all files are processed
    db.close()

    # Print a summary of the import results
    print("\n==============================")
    print("IMPORT COMPLETE")
    print("==============================")
    print(f"Imported : {imported}")
    print(f"Skipped  : {skipped}")
    print(f"Errors   : {errors}")

# Run main() only when this script is executed directly (not imported)
if __name__ == "__main__":
    main()

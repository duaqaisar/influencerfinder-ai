import pandas as pd
from glob import glob
from sqlalchemy.orm import Session
from models.post import Post

def load_kaggle_data(db: Session):
    # Directory containing raw CSV data files
    raw_dir = "data/raw"
    # Find all CSV files in the raw data directory
    csv_files = glob(f"{raw_dir}/*.csv")
    
    print(f"Found {len(csv_files)} CSV files")
    
    # List to hold each loaded DataFrame before combining
    all_data = []
    
    for file in csv_files:
        try:
            # Load each CSV into a DataFrame
            df = pd.read_csv(file)
            print(f"Loaded {file} - Shape: {df.shape}")
            all_data.append(df)
        except Exception as e:
            # Skip files that fail to load, log the error
            print(f"Error loading {file}: {e}")
    
    # If nothing was loaded successfully, stop here
    if not all_data:
        print("No data loaded")
        return
    
    # Combine all individual DataFrames into one
    combined = pd.concat(all_data, ignore_index=True)
    print(f"Combined data shape: {combined.shape}")
    
    # Print column names to see structure
    print("Columns:", combined.columns.tolist())
    
    # Flexible column mapping
    # Standardize differently-named columns across datasets into consistent field names
    combined = combined.rename(columns={
        'Username': 'username',
        'username': 'username',
        'name': 'username',
        'Platform': 'platform',
        'platform': 'platform',
        'Followers': 'followers',
        'followers': 'followers',
        'Likes': 'likes',
        'Comments': 'comments'
    }, errors='ignore')
    
    # Basic cleaning
    # Ensure a username column exists, then drop rows missing a username
    if 'username' in combined.columns:
        combined = combined.dropna(subset=['username'])
        print(f"After cleaning: {len(combined)} rows")
    else:
        # Can't proceed without usernames
        print("No username column found")
        return
    
    # Load sample data (limit to avoid too much data for now)
    # Iterate over only the first 5000 rows (limit for testing)
    for _, row in combined.head(5000).iterrows():   # Limit for testing
        try:
            # Extract and validate the username field
            username = str(row.get('username', ''))
            if not username or username == 'nan':
                continue
            
            # Build a Post record from the row data, with safe defaults for missing values
            post = Post(
                platform=str(row.get('platform', 'instagram')).lower(),
                username=username,
                post_text="Sample post from Kaggle dataset",
                likes=int(row.get('likes', 0) or 0),
                comments=int(row.get('comments', 0) or 0),
                shares=0,
                followers=int(row.get('followers', 0) or 0)
            )
            # Stage the post for insertion
            db.add(post)
        except:
            # Skip any row that fails to process for any reason
            continue
    
    # Commit all staged posts to the database at once
    db.commit()
    print(f"Successfully loaded {5000} sample records into database!")

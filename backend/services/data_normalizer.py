import pandas as pd

def parse_number(value):
    """
    Converts:
        12.5M -> 12500000
        320K  -> 320000
        1234  -> 1234
        NaN   -> 0
    """
    # Return 0 for missing/NaN values
    if pd.isna(value):
        return 0
    # Clean up the string: remove commas/apostrophes, trim whitespace, uppercase for consistent suffix checks
    value = str(value).replace(",", "").replace("'", "").strip().upper()
    try:
        # Handle "M" suffix (millions)
        if value.endswith("M"):
            return int(float(value[:-1]) * 1_000_000)
        # Handle "K" suffix (thousands)
        if value.endswith("K"):
            return int(float(value[:-1]) * 1_000)
        # Otherwise just parse as a plain number
        return int(float(value))
    except:
        # Fallback to 0 if parsing fails for any reason
        return 0

def get_value(row, columns, default=None):
    """
    Returns the first matching column from a dataframe row.
    """
    # Loop through possible column name variants and return the first non-null match
    for col in columns:
        if col in row and pd.notna(row[col]):
            return row[col]
    # Return default if none of the columns exist/have data
    return default

def normalize_influencer(row, platform):
    """
    Convert every dataset into ONE common schema.
    """
    # Try multiple possible column names (across different dataset formats) to find the username
    username = get_value(
        row,
        [
            "Instagram name",
            "instagram name",
            "Influencer insta name",
            "Tiktoker name",
            "Youtuber",
            "youtuber name",
            "Youtube channel",
            "channel name",
            "Username",
        ],
        "",
    )
    # Try multiple possible column names to find the full/display name
    full_name = get_value(
        row,
        [
            "Name",
            "name",
            "Tiktok name",
            "Channel name",
            "influencer name",
        ],
        "",
    )
    # Try multiple possible column names to find the category
    category = get_value(
        row,
        [
            "Category",
            "Category_1",
            "Category-1",
            "category",
            "category_1",
        ],
        "",
    )
    # Find and parse the follower/subscriber count into a clean integer
    followers = parse_number(
        get_value(
            row,
            [
                "Followers",
                "#Followers",
                "Subscribers",
                "Subscribers count",
            ],
            0,
        )
    )
    # Find and parse the average likes/engagement value into a clean integer
    avg_likes = parse_number(
        get_value(
            row,
            [
                "Likes avg",
                "Likes avg.",
                "Likes (Avg.)",
                "avg likes",
                "Engagement avg\r\n",
                "Eng. (Avg.)",
            ],
            0,
        )
    )
    # Find and parse the average comments value into a clean integer
    avg_comments = parse_number(
        get_value(
            row,
            [
                "Comments avg",
                "Comments avg.",
                "Comments (Avg.)",
                "avg comments",
            ],
            0,
        )
    )
    # Return the normalized data in a single consistent dictionary format
    return {
        "username": str(username).strip(),
        "full_name": str(full_name).strip(),
        "platform": platform,
        "category": str(category).strip(),
        "followers": followers,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments,
    }

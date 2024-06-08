import pandas as pd
import re

# Load the uncleaned data from the provided CSV file
file_path = 'audible_uncleaned.csv'
df_uncleaned = pd.read_csv(file_path, header=None, names=["raw"])

# Function to clean and split the data
def clean_data(row):
    # Split the row into parts based on spaces
    parts = re.split(r'\s{2,}', row)

    # Check if all necessary parts are available
    if len(parts) < 8:
        return [None] * 9  # Return a list with None values if parts are missing

    # Extract relevant information with safety checks
    title = parts[0].strip()
    author_match = re.search(r'Writtenby:(.*?)\s', parts[1])
    author = author_match.group(1).strip() if author_match else None
    narrator_match = re.search(r'Narratedby:(.*?)\s', parts[2])
    narrator = narrator_match.group(1).strip() if narrator_match else None
    duration = parts[3].strip()
    release_date = parts[4].strip()
    language = parts[5].strip()
    rating_info = parts[6].strip()

    # Handle ratings which might be 'Not rated yet'
    if 'Not rated yet' in rating_info:
        rating = 'Not rated yet'
        rating_count = 0
    else:
        rating_match = re.search(r'(\d+\.?\d*) out of 5 stars', rating_info)
        rating = float(rating_match.group(1)) if rating_match else None
        rating_count_match = re.search(r'(\d+) ratings', rating_info)
        rating_count = int(rating_count_match.group(1)) if rating_count_match else 0

    # Price is the last element
    price = float(parts[-1].strip()) if parts[-1].replace('.', '', 1).isdigit() else None

    return [title, author, narrator, duration, release_date, language, rating, rating_count, price]

# Clean the data
cleaned_data = [clean_data(row) for row in df_uncleaned["raw"]]

# Create a DataFrame with cleaned data
columns = ["Title", "Author", "Narrator", "Duration", "Release Date", "Language", "Rating", "Rating Count", "Price"]
df_cleaned = pd.DataFrame(cleaned_data, columns=columns)

# Remove rows with None values in critical columns (optional)
df_cleaned.dropna(subset=["Title", "Author", "Narrator"], inplace=True)

# Save the cleaned data to a new CSV file
df_cleaned.to_csv('audible_cleaned1.csv', index=False)

# Display the cleaned DataFrame
df_cleaned.head()


import os
import pandas as pd
from datetime import datetime

# Set directory path where CSV files are stored
csv_directory = "."
output_html_file = "lists.html"

# Read all CSV files in the directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith(".csv")]
books_data = []

# Process each CSV file
for csv_file in csv_files:
    file_path = os.path.join(csv_directory, csv_file)
    df = pd.read_csv(file_path)

    # Filter out rows where 'Book' is NaN before cleaning the 'Pages' column
    df = df.dropna(subset=["Book"])

    # Filter to include only rows where '?' column has 'X'
    df = df[df["?"] == "X"]

    # Remove commas from the Pages column and convert to integer where possible
    df["Pages"] = df["Pages"].astype(str).str.replace(",", "")
    df["Pages"] = pd.to_numeric(df["Pages"], errors="coerce").fillna(0).astype(int)

    # Extract relevant columns and filter out rows with missing data in 'Start'
    df = df[["Start", "End", "Book", "Author", "Pages"]].dropna(subset=["Start"])
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")  # Convert to datetime
    df["Year"] = df["Start"].dt.year  # Extract year

    # Add to the main list
    books_data.append(df)

# Concatenate all data and sort by year (newest to oldest) and start date within each year
books_df = pd.concat(books_data).sort_values(
    by=["Year", "Start"], ascending=[False, True]
)

# Generate content for lists.html
lists_content = ""

# Group by year, sort newest to oldest, and alternate sections
group_classes = ["lightgroup", "darkgroup"]
group_index = 0

for year, year_df in books_df.groupby("Year", sort=False):
    total_books = len(year_df)
    total_pages = year_df["Pages"].sum()
    group_class = group_classes[group_index % 2]

    # Format total_books and total_pages with commas
    formatted_total_books = f"{total_books:,}"
    formatted_total_pages = f"{total_pages:,}"

    # Add year summary at the top with ctitle class for the year
    lists_content += f"""
        <div class="{group_class}">
            <div class="container">
                <div class="ctitle" id="{year}">{year}</div>
                <p>Total Books: {formatted_total_books}, Total Pages: {formatted_total_pages}</p>
                <ul>
    """

    # List books for the year
    for _, row in year_df.iterrows():
        title = row["Book"]
        author = row["Author"]
        pages = f"{int(row['Pages']):,}"  # Format pages with commas
        lists_content += f"<li><em>{title}</em> -- {author} -- {pages} pages</li>\n"

    lists_content += "</ul></div></div>"
    group_index += 1  # Alternate between lightgroup and darkgroup

# Write the lists to lists.html
with open(output_html_file, "w", encoding="utf-8") as f:
    f.write(lists_content)

print(f"Generated book lists in {output_html_file}")

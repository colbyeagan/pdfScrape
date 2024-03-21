import requests
import pandas as pd
import time
import random
from datetime import datetime

# Load URLs and names from a CSV file
csv_file_path = '/Users/colbyeagan/codingRepos/PdfDownloadProj/download_list.csv'  # Replace this with the path to your CSV file
data = pd.read_csv(csv_file_path)

# Load institution assignments from CSV file
csv_journal_assignments = '/Users/colbyeagan/codingRepos/PdfDownloadProj/institutional_access.csv' # Replace with the path to "institutional access" tab on "journal_list_for_annotation" google sheets
assignment_data = pd.read_csv(csv_journal_assignments)

# Replace with your institution name
institution = 'unc'

# Iterate through assignments and create set of journals for your institution's assignment
journals_set = set()
for _, row in assignment_data.iterrows():
    if row['assignment'] == institution:
        journals_set.add(row['journal'])

def log_error(message):
    """Log an error message to a file with a timestamp."""
    with open('download_errors.log', 'a') as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{timestamp} - {message}\n")

def download_and_rename_pdf(url, file_index, journal_name):
    new_name = f"{file_index:04d}.pdf"  # Formats the index as a zero-padded 4-digit string
    modified_url = url + ".pdf"  # Append ".pdf" to the end of the URL
    try:
        response = requests.get(modified_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        # Write the downloaded PDF to a new file
        with open(new_name, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved {new_name}")
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to download {new_name}: {e}"
        print(error_message)
        log_error(error_message)
        print("=====================================")


# Iterate through all URLs in the CSV
for _, row in data.iterrows():
    if row['journal'] in journals_set:
        download_and_rename_pdf(row['url'], row['pdf_file_index'], row['journal'])

        # Generate a random time offset with an average of 1 minute
        time_offset = random.normalvariate(60, 20)  # mean = 60 seconds, standard deviation = 20
        time_offset = max(0, time_offset)  # Ensure time offset is not negative
        print(f"Waiting for {time_offset:.2f} seconds before downloading the next PDF...")
        time.sleep(time_offset)
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(url):
    # Fetch the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        return "Failed to retrieve the webpage"

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table, you might need to adjust this to find the specific table you're interested in
    table = soup.find('div', class_='table__container')
    
    # Extract data from the table
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    return data

def sort_and_export_to_excel(data, excel_file):
    # Manual column names if the table doesn't have headers
    columns = ['Dam', 'Full supply volume (ML)', 'Current volume (ML)', '%% full', 'Latest Observation', 'Comment']
    
    # Convert data to a DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # Sort DataFrame by a specific column, change 'Column_name' to the column you want to sort by
    sorted_df = df.sort_values(by='Dam')
    
    # Export sorted DataFrame to Excel
    sorted_df.to_excel(excel_file, index=False)
    print("Data exported to Excel successfully.")

# Example usage
url = "https://www.seqwater.com.au/dam-levels"  # Replace with the actual URL
table_data = scrape_table(url)
if isinstance(table_data, list):
    sort_and_export_to_excel(table_data[1:], "sorted_data.xlsx")  # Assuming the first row contains data, not headers
else:
    print(table_data)

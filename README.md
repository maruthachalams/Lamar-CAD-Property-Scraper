# Lamar CAD Property Scraper

This Python script scrapes property details from the Lamar CAD website using GET requests and saves the extracted information in a text file. The information includes geographic ID, type, zoning, property use, condo status, situs address, map ID, Mapsco, legal description, abstract or subdivision, neighborhood, owner ID, name, agent, mailing address, and percentage ownership.

## Features
- Scrapes property details from the Lamar CAD website.
- Extracts information such as geographic ID, type, zoning, property use, condo status, situs address, map ID, Mapsco, legal description, abstract or subdivision, neighborhood, owner ID, name, agent, mailing address, and percentage ownership.
- Saves the extracted information into a text file (`OutPut.txt`).
- Handles retries and transient errors using the `requests` library.

## Requirements
- Python 3.x
- `requests` library
- `re` library

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/maruthachalams/Lamar-CAD-Property-Scraper.git
    cd lamar-cad-property-scraper
    ```
2. Install the required libraries:
    ```sh
    pip install requests
    ```

## Usage
1. Ensure the input data file `input_property_id.txt` contains the property IDs you want to scrape, with one property ID per line.
2. Run the script:
    ```sh
    python scraper.py
    ```
3. Enter the year when prompted.
4. The output will be saved in a file named `OutPut.txt`.

## Code Explanation
### `single_regex(pattern, target_string)`
This function uses regular expressions to find matches in a target string and returns the first match found.

### Main Script
1. Initializes an output string with headers and writes it to `OutPut.txt`.
2. Reads property IDs from the `input_property_id.txt` file and stores them in a list.
3. Prompts the user to enter a year.
4. Sets up a `requests` session with retry logic to handle transient errors and rate-limiting issues.
5. For each property ID in the list:
    - Sends a GET request to the Lamar CAD search API.
    - Prints the response status code and writes the response content to `Search_Page.html`.
    - Extracts the owner ID from the response content using regular expressions.
    - Sends a GET request to the detailed property page URL.
    - Prints the response status code and writes the detailed response content to `detailed_page.html`.
    - Extracts detailed property information using regular expressions.
    - Formats the extracted information and appends it to `OutPut.txt`.
    - Prints "ID Completed" for each property ID.
    - Catches and prints any `requests.exceptions.RequestException` errors.



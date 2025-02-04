import re
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def single_regex(pattern, target_string):
    data = re.findall(pattern, target_string)
    return data[0] if data else ''

with open("input_property_id.txt", "r") as file:
    data_list = [line.strip() for line in file]

year = input("Enter the Year: ")

output_data = "Property ID\tGeographic ID\tType\tZoning\tProperty Use\tCondo\tSitus Address\tMap ID\tMapsco\tLegal Description\tAbstract or Subdivision\tNeighborhood\tOwner ID\tName\tAgent\tMailing Address\t% Ownership\n"

with open("OutPut.txt", 'w') as OP:
    OP.write(output_data)

session = requests.Session()
retry = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

for property_id in data_list:
    main_url = f"https://esearch.lamarcad.org/search/SearchResults?keywords=PropertyId%3A{property_id}%20Year%3A{year}&page=1&pagesize=25&recaptchaToken="

    try:
        content_response = session.get(main_url, timeout=20)
        response_code = content_response.status_code
        print(response_code)
        content = content_response.text
        time.sleep(5)

        with open('Search_Page.html', 'w', encoding='utf-8') as SP:
            SP.write(content)

        owner_id = single_regex(r'ownerId\"\:\"([^>]*?)\"', content)

        detailed_page_url = f"https://esearch.lamarcad.org/Property/View/{property_id}?year={year}&ownerId={owner_id}"

        detailed_content_response = session.get(detailed_page_url, timeout=20)
        det_response_code = detailed_content_response.status_code
        print(det_response_code)
        content2 = detailed_content_response.text
        time.sleep(10)

        with open('detailed_page.html', 'w', encoding='utf_8') as DP:
            DP.write(content2)

        property_content = single_regex(r'Account<\/th><\/tr>\s*<tr>\s*([\w\W]*?)Exemptions', content2)
        property_content = re.sub('<br />', '', property_content)
        property_content = re.sub('&#xD;&#xA;', ' ', property_content)

        geographic_id = single_regex(r'Geographic\s*ID\:\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        property_type = single_regex(r'Type:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        zoning = single_regex(r'Zoning:\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        property_use = single_regex(r'Property\s*Use:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        condo = single_regex(r'Condo:\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        situs_address = single_regex(r'Situs\s*Address\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        map_id = single_regex(r'Map\s*ID\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        mapsco = single_regex(r'Mapsco\:\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        legal_description = single_regex(r'Legal\s*Description\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        abstractorsubdivision = single_regex(r'Abstract\/Subdivision\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        neighborhood = single_regex(r'Neighborhood\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        owner_id = single_regex(r'Owner\s*ID\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        name = single_regex(r'Name\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        agent = single_regex(r'Agent\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        mailing_address = single_regex(r'Mailing\s*Address\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)
        percentage_ownership = single_regex(r'\%\s*Ownership\:\s*<[^>]*?>\s*<[^>]*?>\s*([^>]*?)<\/td>', property_content)

        output_data = f"{property_id}\t{geographic_id}\t{property_type}\t{zoning}\t{property_use}\t{condo}\t{situs_address}\t{map_id}\t{mapsco}\t{legal_description}\t{abstractorsubdivision}\t{neighborhood}\t{owner_id}\t{name}\t{agent}\t{mailing_address}\t{percentage_ownership}\n"

        with open("OutPut.txt", 'a') as OP:
            OP.write(output_data)
        print("ID Completed: ", property_id) 
    except requests.exceptions.RequestException as e:
        print(f"An error occurred for Property ID {property_id}: {e}")

print("completed")

import requests
import json
from bs4 import BeautifulSoup

# Get links to articles from Physical Review 

volume = input("Volume: ")
max_issue = input("Issue to go up to: ")

def get_a_elements_with_abstract_and_fulltext(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        a_elements = soup.find_all('a', href=lambda href: href and "abstract" in href and "fulltext" in href)
        return [f"https://journals.aps.org{a.get('href')}" for a in a_elements]
    else:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return []

# Main script
base_url = "https://journals.aps.org/pr/issues/" + str(volume) + "/"
end_issue = int(max_issue) 

data = []
for issue in range(1, end_issue + 1):
    issue_url = base_url + str(issue)
    links = get_a_elements_with_abstract_and_fulltext(issue_url)
    data.append({"issue": issue, "links": links})

with open("journals.json", "w") as f:
    json.dump(data, f, indent=2)

print("Data saved to journals.json successfully.")

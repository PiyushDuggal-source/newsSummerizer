from bs4 import BeautifulSoup
import requests
import streamlit as st
import json
import re
import ollama

sectionDict = [
    {
        "name": "Technology",
        "url": "https://news.ycombinator.com/newest",
        "tag": "span",
        "tag_class" : "titleline"
    },
    # {
    #     "name": "Technology",
    #     "url": "https://www.indianexpress.com/section/technology/",
    #     "tag": "ul",
    #     "tag_class": "article-list",
    # },
    # {
    #     "name": "Education",
    #     "url": "https://www.indianexpress.com/section/education/",
    #     "tag": "div",
    #     "tag_class": "nation",
    # },
    # {
    #     "name": "Politics",
    #     "url": "https://www.indianexpress.com/section/education/",
    #     "tag": "div",
    #     "tag_class": "nation",
    # },
]

sections = ["technology"]


def get_text_from_tag(url):
    # Send an HTTP request to get the website content
    response = requests.get(url)

    # Check for successful response
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        rows = soup.find_all("tr", {"class": "athing"})

        # List to store the extracted data
        extracted_data = []

        # Iterate over each row and extract rank, title, and site
        for row in rows:
            rank = row.find('span', class_='rank').get_text()
            title = row.find('span', class_='titleline').a.get_text()
            site = row.find('span', class_='titleline').a.get('href') if row.find('span', class_='sitestr') else 'N/A'

            # Create a dictionary to store the extracted information
            data = {
                "Rank": rank,
                "Title": title,
                "Site": site
            }

            # Append the data to the list
            extracted_data.append(data)
        return extracted_data
        


# def remove_date_string(text):
#     """
#     Removes a specific date-time format string from a text using regular expressions.
#
#     Args:
#         text: The string from which to remove the date-time string.
#
#     Returns:
#         A new string with the date-time string removed.
#
#     """
#     pattern1 = r"\b\w+ \d{1,2}, \d{4}  \d{2}:\d{2} IST\b"
#     pattern2 = r"\b\w+ \d{1,2}, \d{4} \d{2}:\d{2} IST\b"
#
#     # Remove all occurrences of the pattern
#     output_string = re.sub(pattern1, "", text)
#     output_string = re.sub(pattern2, "", output_string)
#
#     # Clean up any extra spaces
#     output_string = re.sub(" +", " ", output_string).strip()
#     return output_string
#

dataList = []


for diction in sectionDict:
    website_url = diction["url"]
    tag_to_extract = diction["tag"]
    tag_class_name = diction["tag_class"]
    data = get_text_from_tag(website_url)
    # if tag_class_name == "nation":
    #     data = data[:-15]
    dataList.append(data)


for data in dataList:
    print(data)


# page = requests.get('https://indianexpress.com/')
#
# soup = BeautifulSoup(page.content, 'html.parser')
#
# articles = soup.find_all('div', {'class': 'other-article'})

# for article in articles:
#     print(article.text)
text = "can you understand this data given below? can you categories it? \n\n"

json_mylist = json.dumps(dataList[0], separators=(',', ':'))
text += json_mylist

while True:
    response = ollama.generate(model="llama3.2:latest",prompt=text )
    print(response['response'])
    # for part in ollama.generate(model="llama3.2:latest",prompt=text,stream=True ):
    #     print(part['response'], end='', flush=True)
    #     print()

    text = input()
    if text == "exit":
        break

    

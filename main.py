from bs4 import BeautifulSoup
import requests
import streamlit as st
import re

sectionDict = [
    {
        "name": "Technology",
        "url": "https://www.indianexpress.com/section/technology/",
        "tag": "ul",
        "tag_class": "article-list",
    },
    {
        "name": "Education",
        "url": "https://www.indianexpress.com/section/education/",
        "tag": "div",
        "tag_class": "nation",
    },
    {
        "name": "Politics",
        "url": "https://www.indianexpress.com/section/education/",
        "tag": "div",
        "tag_class": "nation",
    },
]

sections = ["technology", "education", "political-pulse"]


def get_text_from_tag(url, tag_name, tag_class=None):
    """
    Extracts text content from a specific tag on a website using BeautifulSoup.

    Args:
        url: The URL of the website to scrape.
        tag_name: The name of the HTML tag to target (e.g., 'div').
        tag_class: The optional class name attribute of the tag (e.g., 'top').

    Returns:
        A string containing the extracted text content from the specified tag.
    """

    # Send an HTTP request to get the website content
    response = requests.get(url)

    # Check for successful response
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the specific tag
        if tag_class:
            target_tag = soup.find(
                tag_name, class_=tag_class
            )  # Use class_ keyword argument
        else:
            target_tag = soup.find(tag_name)

        # Check if tag is found
        if target_tag:
            # Get all text content within the tag recursively (excluding comments and scripts)
            text_content = target_tag.get_text(strip=True, separator="\n")
            return text_content
        else:
            print(
                f"Tag '{tag_name}' with class '{tag_class}' not found on the website."
            )
            return ""
    else:
        print(
            f"Error: Failed to retrieve website content. Status code: {response.status_code}"
        )
        return ""


def remove_date_string(text):
    """
    Removes a specific date-time format string from a text using regular expressions.

    Args:
        text: The string from which to remove the date-time string.

    Returns:
        A new string with the date-time string removed.

    """
    pattern1 = r"\b\w+ \d{1,2}, \d{4}  \d{2}:\d{2} IST\b"
    pattern2 = r"\b\w+ \d{1,2}, \d{4} \d{2}:\d{2} IST\b"

    # Remove all occurrences of the pattern
    output_string = re.sub(pattern1, "", text)
    output_string = re.sub(pattern2, "", output_string)

    # Clean up any extra spaces
    output_string = re.sub(" +", " ", output_string).strip()
    return output_string


dataList = []

for i in range(len(sections)):
    website_url = sectionDict[i]["url"]
    tag_to_extract = sectionDict[i]["tag"]
    tag_class_name = sectionDict[i]["tag_class"]
    data = get_text_from_tag(website_url, tag_to_extract, tag_class_name)
    if tag_class_name == "nation":
        data = data[:-15]
    dataList.append(data)


for data in dataList:
    print(remove_date_string(data))


# page = requests.get('https://indianexpress.com/')
#
# soup = BeautifulSoup(page.content, 'html.parser')
#
# articles = soup.find_all('div', {'class': 'other-article'})

# for article in articles:
#     print(article.text)

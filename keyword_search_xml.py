import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from xml.etree.ElementTree import Element, SubElement, tostring

visited_urls = set()

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = [line.strip() for line in file.readlines()]
    return keywords

def extract_paragraphs_with_keywords(url, keywords, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        for keyword in keywords:
            for paragraph in paragraphs:
                text = paragraph.get_text()
                if keyword.lower() in text.lower():
                    # Write each result immediately to the XML file
                    entry = Element('entry')
                    SubElement(entry, 'keyword').text = keyword
                    SubElement(entry, 'url').text = url
                    SubElement(entry, 'text').text = text.strip()
                    
                    with open(output_file, 'ab') as file:
                        file.write(tostring(entry))
                        file.write(b'\n')
                    break
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def spider_and_search(url, keywords, url_keyword, output_file):
    if url in visited_urls:
        return
    visited_urls.add(url)

    extract_paragraphs_with_keywords(url, keywords, output_file)

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')

        for tag in a_tags:
            href = tag.get("href")
            if href:
                new_url = urljoin(url, href)
                if new_url not in visited_urls and url_keyword.lower() in new_url.lower():
                    spider_and_search(new_url, keywords, url_keyword, output_file)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def main():
    start_url = input("Enter the starting URL: ")
    keywords_file = input("Enter the file path for keywords: ")
    output_file = input("Enter the output XML file path: ")
    url_keyword = input("Enter the URL keyword filter: ")

    keywords = load_keywords(keywords_file)

    # Open file and write root element start
    with open(output_file, 'wb') as file:
        file.write(b"<results>\n")

    spider_and_search(start_url, keywords, url_keyword, output_file)

    # Close the root element
    with open(output_file, 'ab') as file:
        file.write(b"</results>\n")

    print(f"XML output saved to {output_file}")

if __name__ == "__main__":
    main()

import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

visited_urls = set()

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = [line.strip() for line in file.readlines()]
    return keywords

def extract_paragraphs_with_keywords(url, keywords, output):
    try:
        response = requests.get(url)
    except requests.RequestException:
        print(f"Request failed: {url}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        for keyword in keywords:
            for paragraph in paragraphs:
                text = paragraph.get_text()
                if keyword.lower() in text.lower():
                    result = {
                        'keyword': keyword,
                        'url': url,
                        'text': text.strip()
                    }
                    
                    # Write each result to the file in real-time
                    with open(output, 'a') as file:
                        json.dump(result, file)
                        file.write(',\n')  # Add a comma to separate entries
                    break

def spider_and_search(url, keywords, output, url_keyword):
    if url in visited_urls:
        return
    visited_urls.add(url)

    extract_paragraphs_with_keywords(url, keywords, output)
    
    try:
        response = requests.get(url)
    except requests.RequestException:
        print(f"Request failed: {url}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')

        for tag in a_tags:
            href = tag.get("href")
            if href:
                new_url = urljoin(url, href)
                if new_url not in visited_urls and url_keyword.lower() in new_url.lower():
                    print(f"Searching URL: {new_url}")
                    spider_and_search(new_url, keywords, output, url_keyword)

def main():
    start_url = input("Enter the starting URL: ")
    keywords_file = input("Enter the file path for keywords: ")
    output_file = input("Enter the output JSON file path: ")
    url_keyword = input("Enter the URL keyword filter (URLs must contain this keyword to be visited): ")

    keywords = load_keywords(keywords_file)

    # Start the JSON array in the output file
    with open(output_file, 'w') as file:
        file.write("[\n")

    spider_and_search(start_url, keywords, output_file, url_keyword)

    # Close the JSON array
    with open(output_file, 'a') as file:
        file.write("\n]")

    print(f"Search complete! Results saved to {output_file}")

if __name__ == "__main__":
    main()

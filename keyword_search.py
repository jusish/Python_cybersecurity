import re
import time
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

def extract_paragraphs_with_keywords(url, keywords, output, json_lines=False):
    results = []
    
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
                    
                    # Write each result immediately to the file
                    if json_lines:
                        with open(output, 'a') as file:
                            json.dump(result, file)
                            file.write('\n')
                    else:
                        results.append(result)
                    break

    return results

def spider_and_search(url, keywords, output, url_keyword, json_lines=False):
    if url in visited_urls:
        return []
    visited_urls.add(url)

    results = extract_paragraphs_with_keywords(url, keywords, output, json_lines=json_lines)
    
    if not json_lines and results:
        with open(output, 'a') as file:
            json.dump(results, file, indent=4)
            file.write(',\n')  # Separate each URL’s result with a comma
    
    try:
        response = requests.get(url)
    except requests.RequestException:
        print(f"Request failed: {url}")
        return results

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')

        for tag in a_tags:
            href = tag.get("href")
            if href:
                new_url = urljoin(url, href)
                if new_url not in visited_urls and url_keyword.lower() in new_url.lower():
                    print(f"Searching URL: {new_url}")
                    results.extend(spider_and_search(new_url, keywords, output, url_keyword, json_lines=json_lines))

    return results

def main():
    start_url = input("Enter the starting URL: ")
    keywords_file = input("Enter the file path for keywords: ")
    output_file = input("Enter the output JSON file path: ")
    url_keyword = input("Enter the URL keyword filter (URLs must contain this keyword to be visited): ")
    output_format = input("Enter 'array' for JSON array format or 'jsonl' for JSON Lines format: ").strip().lower()

    keywords = load_keywords(keywords_file)
    json_lines = output_format == 'jsonl'

    if not json_lines:
        with open(output_file, 'w') as file:
            file.write("[\n")  # Start JSON array

    spider_and_search(start_url, keywords, output_file, url_keyword, json_lines=json_lines)

    if not json_lines:
        with open(output_file, 'a') as file:
            file.write("\n]")  # Close JSON array

    print(f"Search complete! Results saved to {output_file}")

if __name__ == "__main__":
    main()

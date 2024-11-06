import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

visited_urls = set()

def load_file_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def extract_paragraphs_with_keywords(url, keywords, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        results = []
        for keyword in keywords:
            for paragraph in paragraphs:
                text = paragraph.get_text()
                if keyword.lower() in text.lower():
                    result = {
                        'keyword': keyword,
                        'url': url,
                        'text': text.strip()
                    }
                    results.append(result)
                    break
        if results:
            with open(output_file, 'a') as file:
                for result in results:
                    json.dump(result, file)
                    file.write(',\n')
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def spider_and_search(url, keywords, url_keywords, output_file, session):
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    extract_paragraphs_with_keywords(url, keywords, output_file)

    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')

        for tag in a_tags:
            href = tag.get("href")
            if href:
                new_url = urljoin(url, href)
                if new_url not in visited_urls and any(kw.lower() in new_url.lower() for kw in url_keywords):
                    spider_and_search(new_url, keywords, url_keywords, output_file, session)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def main():
    urls_file = 'urls.txt'
    keywords_file = 'keywords.txt'
    url_keywords_file = 'url_keywords.txt'
    output_file = 'output.json'

    urls = load_file_lines(urls_file)
    keywords = load_file_lines(keywords_file)
    url_keywords = load_file_lines(url_keywords_file)

    with open(output_file, 'w') as file:
        file.write("[\n")

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(tqdm(executor.map(lambda url: spider_and_search(url, keywords, url_keywords, output_file, session), urls), total=len(urls)))

    with open(output_file, 'a') as file:
        file.write("\n]")

    print(f"Search complete! Results saved to {output_file}")

if __name__ == "__main__":
    main()

import requests
import os
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

file_path = 'results/data.txt'
file_path_csv = 'results/data.csv'

delete_file = input("Do you want to delete the files? (y/n): ")
if delete_file == 'y':
    if os.path.exists(file_path_csv):
        os.remove(file_path_csv)
        print(file_path_csv + " deleted")
    else:
        print(file_path_csv + "does not exist")
    print("Creating new file" + '\n')

    if os.path.exists(file_path):
        os.remove(file_path)
        print(file_path + " deleted")
    else:
        print(file_path + "does not exist")
    print("Creating new file" + '\n')


class SimpleSpider:
    def __init__(self, start_url, max_pages=3):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_pages = set()

    def is_valid_url(self, url):
        return urlparse(url).scheme in ['http', 'https']

# Perform web crawling and data extraction
    def get_links(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
# Create a list to store the data
        data = []

# links
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if self.is_valid_url(href):
                links.add(href)
            elif href.startswith('/'):
                links.add(urljoin(url, href))

# titles
        titles = soup.find("title")
        with open(file_path, 'a', encoding='utf-8') as f:
            for title in titles:
                f.write('Title: ' + title.text + '\n')

# headers
        headers = soup.find_all(['h1', 'h2', 'h3'])
        if headers is not None:
            with open(file_path_csv, 'a', encoding='utf-8') as f:
                for header in headers:
                    f.write(f"{header.name}:  {header.text}\n")

# text of page
        page_texts = soup.find_all("body")
        with open(file_path_csv, 'a', encoding='utf-8') as f:
            for page_text in page_texts:
                f.write(f"{page_text.name}: {page_text.text} + \n")

        for item in soup.find_all('div', class_='item'):
            title = item.find('h2').text
            description = item.find('p').text

# Create a dictionary for each item and populate it with key-value pairs
            item_data = {'title': title, 'description': description}

# Append the dictionary to the list
            data.append(item_data)

# Print the retrieved data
        for item in data:
            print(item)

        return links

    def crawl(self, url):
        if len(self.visited_pages) >= self.max_pages:
            return

        if url not in self.visited_pages:
            with open(file_path, 'a') as f:
                f.write(url + '\n')
            self.visited_pages.add(url)
            links = self.get_links(url)

            with open(file_path_csv, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Url"])
                writer.writerows(links)

            for link in links:
                self.crawl(link)


if __name__ == "__main__":
    start_url = "https://example.com/"
    spider = SimpleSpider(start_url)
    spider.crawl(start_url)
    print("Done!! View results in " + file_path)

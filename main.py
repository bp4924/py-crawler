import requests
import os
import csv
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

file_path_txt = 'results/data.txt'
file_path_csv = 'results/data.csv'
file_path_json = 'results/data.json'
results_folder = "results"

delete_file = input("Do you want to delete the files? (y/n): ") or "y"
if delete_file == 'y':

    if os.path.exists(results_folder):
        # Iterate over all files in the folder
        for file_name in os.listdir(results_folder):
            file_path = os.path.join(results_folder, file_name)
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)
                print(file_path + " deleted")
    else:
        print(results_folder + " does not exist")

    print("Creating new files" + '\n')


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

            with open(file_path_json, 'a', encoding='utf-8') as json_file:
                for link in links:
                    json.dump(link, json_file)

# titles
        titles = soup.find("title")
        if titles is not None:
            with open(file_path_txt, 'a', encoding='utf-8') as f:
                for title in titles:
                    f.write('Title: ' + title.text + '\n')

                with open(file_path_csv, 'a', encoding='utf-8') as f:
                    for title in titles:
                        f.write("Title: " + title.text)

                with open(file_path_json, 'a', encoding='utf-8') as json_file:
                    for title in titles:
                        json.dump(title, json_file)

# headers
        headers = soup.find_all(['h1', 'h2', 'h3'])
        if headers is not None:
            with open(file_path_txt, 'a', encoding='utf-8') as f:
                for header in headers:
                    f.write(f"{header.name}:  {header.text}\n")

            with open(file_path_csv, 'a', encoding='utf-8') as f:
                for header in headers:
                    f.write(f"{header.name}:  {header.text}\n")

# text of page
        page_texts = soup.find("body")
        with open(file_path_txt, 'a', encoding='utf-8') as f:
            for page_text in page_texts:
                f.write(f"{page_text.name}: {page_text.text} + \n")

        with open(file_path_csv, 'a', encoding='utf-8') as f:
            for page_text in page_texts:
                f.write(f"{page_text.name}: {page_text.text} + \n")


#                print(f"text: {page_text}")

#        for item in soup.find_all('div', class_='item'):
#            print("find div")
            #            title = item.find('h2').text
#            description = item.find('p').text
#            print("find p")
#            print(title, description)

# Create a dictionary for each item and populate it with key-value pairs
#            item_data = {'title': title, 'description': description}
#
#            print("item: " + item_data)

# Append the dictionary to the list
#            data.append(item_data)
#            print(data)

# Print the retrieved data
 #       for item in data:

        return links

    def crawl(self, url):
        if len(self.visited_pages) >= self.max_pages:
            return

        if url not in self.visited_pages:
            with open(file_path_txt, 'a') as f:
                f.write(url + '\n')
            self.visited_pages.add(url)
            links = self.get_links(url)
#            print(f"links: {links}  \n")

            with open(file_path_csv, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Url"])
#                writer.writerows(links)

            for link in links:
                self.crawl(link)


if __name__ == "__main__":
    start_url = "https://example.com/"
    spider = SimpleSpider(start_url)
    spider.crawl(start_url)
    print("Done!! View results in the " + results_folder + " folder")

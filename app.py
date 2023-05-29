import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

results_folder = "results"

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

html_tags = ['a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'bdi', 'bdo', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label',
             'legend', 'li', 'main', 'map', 'mark', 'menu', 'menuitem', 'meter', 'nav', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'slot', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'u', 'ul', 'var', 'video', 'wbr']


class SimpleSpider:
    def __init__(self, start_url, max_pages=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_pages = set()
        self.links = []

    def is_valid_url(self, url):
        return urlparse(url).scheme in ['http', 'https']

    def get_links(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        existing_data = []

        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if self.is_valid_url(href):
                links.add(href)
            elif href.startswith('/'):
                links.add(urljoin(url, href))

        # Define the file path here
        file_path_json = 'results/data.json'

        data = {}
        key = "url"
        value = url
        data[key] = value
        existing_data.append(data)

        # Store HTML elements in a list under each key
        data2 = {}
        elements = soup.find_all(html_tags)
        for element in elements:
            key = element.name
            value = element.text
            if key in data2:
                data2[key].append(value)
            else:
                data2[key] = [value]
        existing_data.append(data2)

        # Write the JSON file for the current URL
        url_file_name = url.replace(
            "/", "_").replace(":", "_").replace(".", "_")
        file_path_json = os.path.join(results_folder, f"{url_file_name}.json")
        with open(file_path_json, 'w') as f:
            json.dump(existing_data, f, indent=4, separators=(',', ': '))

        return links

    def crawl(self, url):
        if len(self.visited_pages) >= self.max_pages:
            return

        if url not in self.visited_pages:
            self.visited_pages.add(url)
            links = self.get_links(url)

            for link in links:
                self.links.append(link)

            while len(self.links) > 0 and len(self.visited_pages) < self.max_pages:
                next_url = self.links.pop(0)
                if next_url not in self.visited_pages:
                    self.crawl(next_url)


if __name__ == "__main__":
    start_url = "https://example.com"
    spider = SimpleSpider(start_url)
    spider.crawl(start_url)
    print("Done!! View results in the " + results_folder + " folder \n")

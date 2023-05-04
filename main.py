import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class SimpleSpider:
   def __init__(self, start_url, max_pages=10):
       self.start_url = start_url
       self.max_pages = max_pages
       self.visited_pages = set()

   def is_valid_url(self, url):
       return urlparse(url).scheme in ['http', 'https']

   def get_links(self, url):
       response = requests.get(url)
       soup = BeautifulSoup(response.text, 'html.parser')
       links = set()

       for link in soup.find_all('a', href=True):
           href = link['href']
           if self.is_valid_url(href):
               links.add(href)
           elif href.startswith('/'):
               links.add(urljoin(url, href))

       return links

   def crawl(self, url):
       if len(self.visited_pages) >= self.max_pages:
           return

       if url not in self.visited_pages:
           with open('results/urls.txt', 'a') as f:
                f.write(url + '\n')
           self.visited_pages.add(url)
           print(f"Visiting: {url}")
           links = self.get_links(url)

           for link in links:
               self.crawl(link)

if __name__ == "__main__":
   start_url = "https://example.com/"
   spider = SimpleSpider(start_url)
   spider.crawl(start_url)

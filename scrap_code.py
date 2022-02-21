import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

base_url= "http://quotes.toscrape.com"


def scrap_quotes():
    all_quotes = []
    page_url= "/page/1"
    while page_url:
        res = requests.get(f"{base_url}{page_url}")
        # print(f"Now scraping {page_url}....")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")["href"]
            })
        next_btn = soup.find(class_="next")
        page_url = next_btn.find("a")["href"] if next_btn else None
        # sleep(2)
    return all_quotes

# Added encoding attribute as the quotes contains some signs that are breaking the code
def write_quotes(quotes):
    with open("quotes.csv", "w", encoding="utf-8") as file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = scrap_quotes()
write_quotes(quotes)
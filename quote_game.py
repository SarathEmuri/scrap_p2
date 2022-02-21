import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

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

def start_game(quotes):
    quote = choice(quotes)
    remain_guesses = 4
    print("Here is a quote:")
    print(quote["text"])
    print(quote["author"])
    guess = ''

    while guess.lower() != quote["author"].lower() and remain_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remain_guesses}\n")
        if guess.lower() == quote["author"].lower():
            print("Hurray! You got it right.")
            break
        remain_guesses -= 1
        if remain_guesses == 3:
            res = requests.get(f"{base_url}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
        elif remain_guesses == 2:
            print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
        elif remain_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(f"Here's a hint: The author's last name starts with: {last_initial}")
        else:
            print(f"Sorry. You ran out of guesses. The author was {quote['author']}.")

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)? ")
    if again.lower() in ('y', 'yes'):
        return start_game(quotes)
    else:
        print("Okay. Goodbye.")

quotes = scrap_quotes()
start_game(quotes)
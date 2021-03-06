import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

base_url= "http://quotes.toscrape.com"

def read_quotes(filename):
    with open(filename, "r", encoding="utf-8") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)

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

quotes = read_quotes("quotes.csv")
start_game(quotes)
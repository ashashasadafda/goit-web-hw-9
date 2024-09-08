import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"


def scrape_quotes(url):
    quotes = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote in soup.find_all('div', class_='quote'):
            quote_data = {
                'text': quote.find('span', class_='text').text,
                'author': quote.find('small', class_='author').text,
                'tags': [tag.text for tag in quote.find_all('a', class_='tag')]
            }
            quotes.append(quote_data)

        next_page = soup.find('li', class_='next')
        if next_page:
            url = BASE_URL + next_page.find('a')['href']
        else:
            url = None

    return quotes


def scrape_authors(quotes):
    authors = {}
    for quote in quotes:
        author_name = quote['author']
        if author_name not in authors:
            authors[author_name] = {
                'name': author_name,
                'description': None,  # Ви можете додати логіку для отримання опису автора, якщо він доступний на сайті
                'born_date': None,
                'born_location': None
            }
    return authors


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    quotes = scrape_quotes(BASE_URL)
    authors = scrape_authors(quotes)

    save_to_json(quotes, 'quotes.json')
    save_to_json(authors, 'authors.json')
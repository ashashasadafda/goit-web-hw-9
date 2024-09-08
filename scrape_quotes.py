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

    return quotes, soup


def scrape_author_bio(author_url):
    response = requests.get(BASE_URL + author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    born_date = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text.strip()

    return {
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    }


def scrape_authors(quotes, soup):
    authors = []
    author_names = set()
    for quote in soup.find_all('div', class_='quote'):
        author_name = quote.find('small', class_='author').text
        if author_name not in author_names:
            author_names.add(author_name)
            author_url = quote.find('a')['href']
            bio_data = scrape_author_bio(author_url)
            authors.append({
                'name': author_name,
                'description': bio_data['description']
            })
    return authors


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    quotes, soup = scrape_quotes(BASE_URL)
    authors = scrape_authors(quotes, soup)

    save_to_json(quotes, 'quotes.json')
    save_to_json(authors, 'authors.json')
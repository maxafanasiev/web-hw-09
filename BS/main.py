import requests
from bs4 import BeautifulSoup
import json


def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    quotes = []

    while True:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, "lxml")

        for quote_div in soup.find_all("div", class_="quote"):
            quote = {
                "quote": quote_div.find("span", class_="text").get_text(),
                "author": quote_div.find("small", class_="author").get_text(),
                "tags": [tag.get_text() for tag in quote_div.find_all("a", class_="tag")]
            }
            quotes.append(quote)

        next_page = soup.find("li", class_="next")
        if next_page:
            base_url = base_url + next_page.find("a")["href"]
        else:
            break

    return quotes


def save_quotes_to_json(quotes):
    with open("jsons/quotes.json", "w") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)


def scrape_authors():
    base_url_perm = base_url = "http://quotes.toscrape.com"
    authors = []

    while True:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, "lxml")

        for author_div in soup.find_all("div", class_="quote"):
            author_info = {
                "fullname": author_div.find("small", class_="author").get_text()}
            author_about = base_url_perm + author_div.find("small", class_="author").find_next("a")["href"]
            inner_response = requests.get(author_about)
            inner_soup = BeautifulSoup(inner_response.content, "html.parser")
            born_date = inner_soup.select("span.author-born-date")
            born_date_text = ''.join([i.text.strip() for i in born_date])

            born_location = inner_soup.select("span.author-born-location")
            born_location_text = ''.join([i.text.strip() for i in born_location])

            description = inner_soup.select("div.author-description")
            description_text = ''.join([i.text.strip() for i in description])

            author_info.update({
                'born_date': born_date_text,
                'born_location': born_location_text,
                'description': description_text,
            })

            if author_info["fullname"] not in [author["fullname"] for author in authors]:
                authors.append(author_info)

        next_page = soup.find("li", class_="next")
        if next_page:
            base_url = base_url + next_page.find("a")["href"]
        else:
            break

    return authors


def save_authors_to_json(authors):
    with open("jsons/authors.json", "w") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    quotes = scrape_quotes()
    save_quotes_to_json(quotes)

    authors = scrape_authors()
    save_authors_to_json(authors)



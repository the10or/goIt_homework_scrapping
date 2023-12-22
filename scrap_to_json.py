import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import lxml

BASE_URL = "https://quotes.toscrape.com"

authors_link_list = set()
quotes_json = []
authors_json = []


def parse_quotes(soup):
    quotes = soup.find_all("div", {"class": "quote"})

    for quote_element in quotes:
        quote = {
            "tags": [
                tag.get_text() for tag in quote_element.find_all("a", {"class": "tag"})
            ],
            "quote": quote_element.find("span", {"class": "text"}).get_text(),
            "author": quote_element.find("small", {"class": "author"}).get_text(),
        }
        quotes_json.append(quote)


def parse_authors():
    for author in authors_link_list:
        auth_response = requests.get(f"{BASE_URL}{author}")
        auth_soup = BeautifulSoup(auth_response.content, "lxml")
        author_description = auth_soup.find(
            "div", {"class": "author-description"}
        ).get_text(strip=True)
        author_name = auth_soup.find("h3", {"class": "author-title"}).get_text()
        author_born_date = auth_soup.find(
            "span", {"class": "author-born-date"}
        ).get_text()
        author_born_location = auth_soup.find(
            "span", {"class": "author-born-location"}
        ).get_text()

        entry = {
            "fullname": author_name,
            "born_date": author_born_date,
            "born_location": author_born_location,
            "description": author_description,
        }
        authors_json.append(entry)


def write_json(file_name, items_list):
    with open(f"{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(items_list, file, indent=4, ensure_ascii=False)


def main():
    next_page = ""
    while next_page is not None:
        response = requests.get(f"{BASE_URL}{next_page}")
        soup = BeautifulSoup(response.content, "lxml")

        parse_quotes(soup)

        link_list = soup.find_all("a", {"class": None})

        [
            authors_link_list.add(link.get("href"))
            for link in link_list
            if "author" in link.get("href")
        ]

        try:
            next_page = soup.find("li", {"class": "next"}).find("a").get("href")
        except AttributeError:
            break

    parse_authors()

    write_json("quotes", quotes_json)

    write_json("authors", authors_json)


if __name__ == "__main__":
    start = datetime.now()
    main()
    print((datetime.now() - start).seconds)

#!/bin/python3
import sqlite3
import requests
from bs4 import BeautifulSoup

MAIN_URL = "http://cdda-trunk.chezzo.com/books/"
BOOK_TYPES = [
    "combat", "crafts", "engineering",
    "fun", "range", "social", "survival"]

CON_BD = sqlite3.connect('books.db')

RELIGIOUS_TEXTS = [
    "holybook_bible1",
    "holybook_bible2",
    "holybook_bible3",
    "holybook_quran",
    "holybook_hadith",
    "holybook_havamal",
    "holybook_tanakh",
    "holybook_talmud",
    "holybook_vedas",
    "holybook_upanishads",
    "holybook_tripitaka",
    "holybook_sutras",
    "holybook_granth",
    "holybook_mormon",
    "holybook_kojiki",
    "holybook_pastafarian",
    "holybook_slack",
    "holybook_kallisti",
    "holybook_scientology"
]


def get_books(url, table_name):
    result = requests.get(url)
    print(result.status_code)
    result_content = result.content
    soup = BeautifulSoup(result_content, features="lxml")
    table = soup.find("table")
    samples = table.find_all("a")
    cursor = CON_BD.cursor()
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    CON_BD.commit()
    cursor.execute(
        "CREATE TABLE " + table_name + "(name VARCHAR(50), id VARCHAR(50))")
    CON_BD.commit()
    for book in samples:
        curr_book = book.string
        if curr_book:
            book_id = book['href'].split("/")[3]
            title = curr_book.strip()
            if "holybook" not in book_id:
                cursor.execute(
                    "INSERT INTO " + table_name + "(name, id) VALUES(?, ?)",
                    (title, book_id))
                CON_BD.commit()
        else:
            print("error loading string in:")
            print(book)
    cursor.close()


for book in BOOK_TYPES:
    url = MAIN_URL + book
    get_books(url, book)
CON_BD.close()


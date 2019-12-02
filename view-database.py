import sqlite3
import json
BOOK_TYPES = [
    "combat", "crafts", "engineering",
    "fun", "range", "social", "survival"]

CON_BD = sqlite3.connect('books.db')
BOOK_LIST = []


def consult_book_table(table_name):
    cursor = CON_BD.cursor()
    cursor.execute("SELECT * FROM " + table_name)
    for book in cursor:
        book_dict = {}
        book_dict["name"] = book[0]
        book_dict["id"] = book[1]
        BOOK_LIST.append(book_dict)
    cursor.close()


def consult_all_tables():
    for book in BOOK_TYPES:
        consult_book_table(book)


def find(key, data):
    global found_bool
    if type(data) == list:
        for item in data:
            find(key, item)
    if type(data) == dict:
        for k, value in data.items():
            find(key, value)
    if type(data) == str:
        if data == key:
            found_bool = True


found_bool = False


def view_json():
    global found_bool
    with open('120.5.0.map') as json_file:
        data = json.load(json_file)
        for book in BOOK_LIST:
            found_bool = False
            find(book.get("id"), data)
            if not found_bool:
                print(book.get("name").upper() + " --- " + book.get('id'))


consult_all_tables()
view_json()
CON_BD.close()

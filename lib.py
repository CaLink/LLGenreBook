import sqlite3
import os

def InitDir():
    if(not os.path.exists("db")):
        os.mkdir("db")
    if(not os.path.exists("db/log")):
        os.mkdir("db/log")

def WriteLog(name, resp):

        if(resp.status != 200):
            with open(f"db/{name}Log.txt",'a',encoding='utf8') as fp:
                fp.write(f"{resp.status}\t{resp.url}\t{resp.request.headers.get('Referer', None)}\n")
        else:
            with open(f"db/{name}Success.txt",'a',encoding='utf8') as fp:
                fp.write(f"{resp.url}\n")


def InitDB(name):
    connection = sqlite3.connect(f'db/{"book"}.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
                        name TEXT, url TEXT, genre TEXT
                        )''')
    connection.commit()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS Books (
                        id TEXT, sourceLink TEXT, title TEXT, author TEXT,
                        type_book TEXT, description TEXT,
                        genres TEXT, main_genre TEXT,
                        number_of_pages TEXT, language TEXT,
                        age_limit TEXT, publisher TEXT,
                        publication_year TEXT, circulations TEXT,
                        rating TEXT, number_of_reviews TEXT,
                        number_of_users_read TEXT, number_of_users_planning TEXT,
                        ISBN TEXT, parsing_date TEXT
                        )''')
    connection.commit()
    cursor.close()

def AddToDB(name, book):
    connection = sqlite3.connect(f'db/{"book"}.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {name} VALUES (?,?,?)",
                    (book.name, book.url, book.genre))
    connection.commit()
    connection.close()

def AddBookToDB(book):
    connection = sqlite3.connect(f'db/{"book"}.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Books VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (book.id, book.sourceLink, book.title, book.author, book.type_book, book.description, book.genres_from_book, book.main_genre, book.number_of_pages, book.language, book.age_limit, book.publisher, book.publication_year, book.circulations, book.rating, book.number_of_reviews, book.number_of_users_read, book.number_of_users_planning, book.ISBN, book.parsing_date))
    connection.commit()
    connection.close()

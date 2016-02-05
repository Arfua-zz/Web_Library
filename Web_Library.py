from time import sleep
from threading import Thread
import importlib
import urllib
from urllib import parse
import flask
from flask import Flask, request, redirect
app = Flask(__name__)
import sqlite3

conn = sqlite3.connect('library.sqlite')


def get_authors():
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM Author;')
    writelist = ''
    for author in cur:
            writelist += '<li><a href="/author/%i">%s</a></li>'%author
    return writelist

def get_books():
    cur = conn.cursor()
    cur.execute('SELECT id, title FROM Book;')
    writelist = ''
    for book in cur:
            writelist += '<li><a href="/book/%i">%s</a></li>'%book
    return writelist

def get_books_by_author(author_id):
    cur = conn.cursor()
    cur.execute('SELECT Book.* FROM Book, BookAuthor AS BA, Author WHERE Book.id=BA.book_id AND Author.id=BA.author_id AND Author.id = ? ', (author_id, ))
    books = cur.fetchall()
    print(books)
    writelist = ''
    for book in books:
            writelist += '<li><a href="/book/%i">%s</a></li>'%book
    return writelist

def get_authors_by_book(book_id):
    cur = conn.cursor()
    cur.execute('SELECT Author.* FROM Author, BookAuthor AS BA, Book WHERE Book.id=BA.book_id AND Author.id=BA.author_id AND Book.id = ? ', (book_id, ))
    authors = cur.fetchall()
    print(authors)
    writelist = ''
    for author in authors:
            writelist += '<li><a href="/author/%i">%s</a></li>'%author
    return writelist

@app.route("/")
def main():

    form = """
            <form action="/new_book" method="post">
                <input name="book">
                <input type="submit" value="add Book Author (e.g. Lord King)">
           </form>
           <form action="/remove_author" method="post">
                <input name="author">
                <input type="submit" value="remove Author">
           </form>
           <table>
           <tr>
                <td>%s</td>
                <td>%s</td>
           </tr>
           </table>
            """ % (get_authors(), get_books())

    return form

@app.route("/author/<author_id>", methods=['GET'])
def author(author_id):
    return get_books_by_author(author_id)

@app.route("/book/<book_id>", methods=['GET'])
def book(book_id):
    return get_authors_by_book(book_id)


@app.route("/new_author", methods=['POST'])
def new_author():
    pass

@app.route("/new_book", methods=['POST'])
def new_book_author():
    title, name = request.form['book'].split()

    cur = conn.cursor()
    cur.execute('''INSERT OR IGNORE INTO Author (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM Author WHERE name = ? ', (name, ))
    author_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Book (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Book WHERE title = ? ', (title, ))
    book_id = cur.fetchone()[0]
    cur.execute('''INSERT OR REPLACE INTO BookAuthor
        (author_id, book_id) VALUES ( ?, ? )''',
        ( author_id, book_id) )
    conn.commit()

    return redirect('/')

@app.route("/remove_author", methods=['POST'])
def remove_author():
    name = request.form['author']
    cur = conn.cursor()
    cur.execute('SELECT id FROM Author WHERE name = ? ', (name, ))
    author_id = cur.fetchone()[0]
    cur.execute('DELETE FROM BookAuthor WHERE author_id = ?', ( author_id, ) )
    cur.execute('DELETE FROM Author WHERE id = ?', ( author_id, ) )

    conn.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0')


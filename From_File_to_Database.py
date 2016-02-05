import sqlite3

conn = sqlite3.connect('library.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS BookAuthor;

CREATE TABLE Author (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Book (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE BookAuthor (
    author_id     INTEGER,
    book_id   INTEGER,
    PRIMARY KEY (author_id, book_id)
)
''')

fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'library.txt'

fh = open(fname)

for line in fh:
    words = line.split()

    name = words[0]
    title = words[1]

    print(name, title)

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


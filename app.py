from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB="database.db"
mails = []

def get_db():
    return sqlite3.connect(DB)
    
def init_db():
    with get_db() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            description TEXT,
            year INTEGER,
            image_url TEXT,
            created_at TEXT
        )
        ''')
        
def mails():
    return mails

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/library')
def library():
    with get_db() as conn:
        books = conn.execute('SELECT * FROM books').fetchall()
    return render_template('library.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    year = request.form['year']
    image_url = request.form['image_url']
    created_at = datetime.now().isoformat()
    
    with get_db() as conn:
        conn.execute('''
        INSERT INTO books (title, author, description, year, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, author, description, year, image_url, created_at))
    
    return redirect('/library')


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    with get_db() as conn:
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if book:
        return render_template('book_detail.html', book=book)
    else:
        return "Книга не знайдена", 404
    
@app.route('/delete/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    with get_db() as conn:
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    return redirect('/library')





if __name__ == '__main__':
    init_db()
    app.run(debug=True)
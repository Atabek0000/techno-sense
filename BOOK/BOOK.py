from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

books = []


class Book:
    def __init__(self, title, author, price, stock, image_url):
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock
        self.image_url = image_url

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url
        }


@app.route('/')
def index():
    return render_template('book.html', books=books)


@app.route('/about')
def about():
    return render_template('about.html', books=books)


@app.route('/delete_book', methods=['POST'])
def delete_book():
    global books
    title = request.form['title']

    books = [book for book in books if book.title.lower() != title.lower()]

    return redirect(url_for('about'))


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    image_url = request.form['image_url']

    new_book = Book(title, author, price, stock, image_url)
    books.append(new_book)

    return redirect(url_for('index'))


@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify([book.to_dict() for book in books])


@app.route('/api/books/<string:title>', methods=['GET'])
def get_book(title):
    for book in books:
        if book.title.lower() == title.lower():
            return jsonify(book.to_dict())
    return jsonify({"error": "Book not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)

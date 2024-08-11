import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

books = []
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}


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


@app.route('/payment_success')
def payment_success():
    title = request.args.get('title')
    price = request.args.get('price')
    return render_template('payment_success.html', title=title, price=price)


@app.route('/checkout', methods=['POST'])
def checkout():
    title = request.form['title']
    price = request.form['price']
    return render_template('checkout.html', title=title, price=price)


@app.route('/process_payment', methods=['POST'])
def process_payment():
    card_number = request.form.get('card_number')  # Убедитесь, что название совпадает
    card_holder = request.form.get('card_holder')
    expiration_month = request.form.get('expiration_month')
    expiration_year = request.form.get('expiration_year')
    cvv = request.form.get('cvv')
    title = request.form.get('title')
    price = request.form.get('price')

    if not all([card_number, card_holder, expiration_month, expiration_year, cvv, title, price]):
        return "Missing required fields", 400

    title = request.form['title']
    for book in books:
        if book.title == title and book.stock > 0:
            book.stock -= 1
            break

    return redirect(url_for('payment_success', title=title, price=price))


@app.route('/delete_book', methods=['POST'])
def delete_book():
    global books
    title = request.form['title']

    books = [book for book in books if book.title.lower() != title.lower()]

    return redirect(url_for('about'))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    price = float(request.form['price'])
    stock = int(request.form['stock'])

    image = request.files['image']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_url = url_for('static', filename='uploads/' + filename)
    else:
        image_url = None

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

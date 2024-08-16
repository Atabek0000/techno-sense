import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# books #
books = []
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
# books #

#
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)
#


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')

    # Убедитесь, что шаблон и переменные корректно настроены
    return render_template('register.html', form=form, login=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('about'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')
#


# Book #
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
# Book #


# index #
@app.route('/')
def index():
    return render_template('book.html', books=books)
# index #


# about #
@app.route('/about')
def about():
    return render_template('about.html', books=books)
# about #


# payment_success #
@app.route('/payment_success')
def payment_success():
    title = request.args.get('title')
    price = request.args.get('price')
    return render_template('payment_success.html', title=title, price=price)
# payment_success #


# checkout #
@app.route('/checkout', methods=['POST'])
def checkout():
    title = request.form['title']
    price = request.form['price']
    return render_template('checkout.html', title=title, price=price)
# checkout #


# process_payment #
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

    # Save payment details to payments.txt
    with open('payments.txt', 'a') as f:
        f.write(f"Card Number: {card_number}, Card Holder: {card_holder}, "
                f"Expiration Month: {expiration_month}, Expiration Year: {expiration_year}, "
                f"CVV: {cvv}, Title: {title}, Price: {price}\n")

    title = request.form['title']
    for book in books:
        if book.title == title and book.stock > 0:
            book.stock -= 1
            break

    return redirect(url_for('payment_success', title=title, price=price))


# end #
@app.route('/delete_book', methods=['POST'])
def delete_book():
    global books
    title = request.form['title']

    books = [book for book in books if book.title.lower() != title.lower()]

    return redirect(url_for('about'))
# delete_book #


# add_book #
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
# add_book #


# get_books #
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify([book.to_dict() for book in books])


@app.route('/api/books/<string:title>', methods=['GET'])
def get_book(title):
    for book in books:
        if book.title.lower() == title.lower():
            return jsonify(book.to_dict())
    return jsonify({"error": "Book not found"}), 404
# get_books #

if __name__ == '__main__':
    app.run(debug=True)

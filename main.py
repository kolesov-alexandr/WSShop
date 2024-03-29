import flask_login
import os

from flask import Flask, render_template, redirect, abort, request, url_for, send_from_directory
from data import db_session
from data.apps import App
from data.users import User
from forms.app import AppForm
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import LoginForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/static/soft_images/'
ALLOWED_EXTENSIONS = set(['gif', 'png', 'jpg', 'jpeg'])

app.config['SECRET_KEY'] = '6f7db8d75e94bcdeb5d1c47d7bba0f0e'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    apps = db_sess.query(App).all()
    return render_template('index.html', title='Домашняя страница', apps=apps)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('test_register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('test_register.html', title='Регистрация',
                                   form=form,
                                   message="Эта почта уже используется")
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('test_register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким логином уже существует")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            login=form.login.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('test_register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('test_login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('test_login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/self_page&<login>')
def self_page(login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == login).first()
    user_apps = user.apps
    return render_template('self_page.html', title='Домашняя страница', login=user.login,
                           collection=user_apps)


@app.route('/product_page&<name>')
@login_required
def product_page(name):
    db_sess = db_session.create_session()
    product = db_sess.query(App).filter(App.name == name).first()
    user = db_sess.query(User).filter(User.id == flask_login.current_user.id).first()
    was_bought = product in user.apps
    return render_template('product_page.html', title='Домашняя страница', product=product,
                           was_bought=was_bought)


@app.route('/product_buy&<name>', methods=['GET', 'POST'])
@login_required
def buy_product(name):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == flask_login.current_user.id).first()
    product = db_sess.query(App).filter(App.name == name).first()
    if product:
        user.apps.append(product)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/index')


@app.route('/create_app', methods=['GET', 'POST'])
@login_required
def create_app():
    form = AppForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        app_ = App()
        app_.name = form.name.data
        app_.description = form.description.data
        app_.publisher = flask_login.current_user.id
        app_.price = form.price.data
        app_.download_link = form.download_link.data
        db_sess.add(app_)
        db_sess.commit()

        product = db_sess.query(App).filter(App.name == form.name.data).first()

        f = request.files['file']
        if f and allowed_file(f.filename):
            f.save(os.path.join(app_.config['UPLOAD_FOLDER'], secure_filename(str(product.id))))
        return redirect('/')
    return render_template('create_app.html', title='Добавление приложения',
                           form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1) in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    main()

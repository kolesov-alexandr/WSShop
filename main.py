from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '6f7db8d75e94bcdeb5d1c47d7bba0f0e'


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Домашняя страница')


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
        if db_sess.query(User).filter(User.telephone == form.telephone.data).first():
            return render_template('test_register.html', title='Регистрация',
                                   form=form,
                                   message="Этот номер телефона уже используется")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            login=form.login.data,
            telephone=form.telephone.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('test_register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()


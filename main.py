from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = '6f7db8d75e94bcdeb5d1c47d7bba0f0e'


def main():
    app.run()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Домашняя страница')


if __name__ == '__main__':
    main()


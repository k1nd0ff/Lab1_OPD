from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)                 # создаём приложение
app.secret_key = 'very‑secret'        # хранение сессии

base = os.path.abspath(os.path.dirname(__file__))
user = os.path.join(base, 'data.txt')


def load_users() -> dict: # Читает data.txt и возвращает {login: password}.
    users = {}
    if not os.path.exists(user):
        return users
    with open(user, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ';' not in line:
                continue
            login, pwd = line.split(';', 1)
            users[login.strip()] = pwd.strip()
    return users


def save_user(login: str, pwd: str) -> None:
    with open(user, 'a', encoding='utf-8') as f:
        f.write(f'{login};{pwd}\n')


@app.route('/', methods=['GET', 'POST']) # пользователь отправил форму
def login():
    if request.method == 'POST':
        login = request.form['login'].strip()
        pwd   = request.form['pwd'].strip()

        users = load_users() # запоминаем, кто вошёл
        if users.get(login) == pwd:
            session['user'] = login
            return redirect(url_for('welcome')) # переходим к защищённой странице

        return render_template('login.html',
                               error='Неправильный логин или пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login'].strip()
        pwd1 = request.form['pwd1'].strip()
        pwd2 = request.form['pwd2'].strip()
        if not login or not pwd1:
            return render_template('reg.html',
                                   error='Заполните все поля')
        if pwd1 != pwd2:
            return render_template('reg.html',
                                   error='Пароли не совпадают')
        if login in load_users():
            return render_template('reg.html',
                                   error='Такой логин уже существует')
        save_user(login, pwd1)
        return render_template('reg.html',
                               success='Регистрация прошла успешно! '
                                       'Можно входить.')

    return render_template('reg.html')


@app.route('/welcome')
def welcome():
    if 'user' not in session:                    # если нет входа – обратно к форме
        return redirect(url_for('login'))
    return f"<h1>Привет, {session['user']}!</h1><a href='/logout'>Выйти</a>"


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
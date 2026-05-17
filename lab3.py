from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)                 # создаём приложение
app.secret_key = 'very‑secret'        # хранение сессии

USERS_FILE = 'data.txt'              # путь к файлу‑базе


def load_users(): # Читает users.txt и возвращает словарь {login: password}
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ';' in line:
                    login, pwd = line.split(';', 1)
                    users[login] = pwd
    return users


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':                 # пользователь отправил форму
        login = request.form['login']
        pwd   = request.form['pwd']
        users = load_users()
        if login in users and users[login] == pwd:
            session['user'] = login               # запоминаем, кто вошёл
            return redirect(url_for('welcome'))   # переходим к защищённой странице
        else:
            return render_template('login.html',
                                   error='Неправильный логин или пароль')
    return render_template('login.html')


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
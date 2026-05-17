from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# Секретный ключ нужен для сессий; в учебных целях фиксируем.
app.secret_key = 'super‑secret‑key-12345'

USERS_FILE = 'users.txt'


def load_users() -> dict:
    """
    Считывает файл users.txt и возвращает словарь {login: password}.
    Строки, не содержащие «;», игнорируются.
    """
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ';' not in line or not line:
                continue
            login, pwd = line.split(';', 1)
            users[login] = pwd
    return users


@app.route('/', methods=['GET', 'POST'])
def login():
    """Отображает форму входа и обрабатывает её отправку."""
    if request.method == 'POST':
        login = request.form.get('login')
        pwd = request.form.get('pwd')
        users = load_users()

        # простая проверка
        if login in users and users[login] == pwd:
            session['user'] = login          # сохраняем в сессии
            return redirect(url_for('welcome'))
        else:
            error = 'Неправильный логин или пароль'
            return render_template('login.html', error=error)

    # GET‑запрос – просто показываем форму
    return render_template('login.html')


@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('login'))   # если нет сессии – обратно к логину
    return render_template('welcome.html', user=session['user'])
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from Authentication import check_credentials

app = Flask(__name__)
app.secret_key = 'dev-secret-key'   # нужен только для flash‑сообщений


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if check_credentials(login, password):
            flash('Вход выполнен успешно')
            return redirect(url_for('login'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'dev-secret-key'


@app.route('/', methods=['GET', 'POST'])
def login4():
    return render_template('login4.html')


@app.route('/register', methods=['GET', 'POST'])
def reg4():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        from Authentication import _load_users, file
        users = _load_users()
        if login in users:
            flash('Пользователь уже существует')
        else:
            users[login] = password
            # сохраняем обратно в JSON
            import json
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            flash('Аккаунт создан, теперь можно войти')
            return redirect(url_for('login4'))

    return render_template('reg4.html')


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'dev-secret-key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        from Authentication import _load_users, USER_FILE
        users = _load_users()
        if login in users:
            flash('Пользователь уже существует')
        else:
            users[login] = password
            # сохраняем обратно в JSON
            import json
            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            flash('Аккаунт создан, теперь можно войти')
            return redirect(url_for('login'))

    return render_template('reg.html')
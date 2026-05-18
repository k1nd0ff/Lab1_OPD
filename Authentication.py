import json
from pathlib import Path

user = Path(__file__).with_name('user.json')


def check_credentials(login: str, password: str) -> bool: # Возвращает True, если логин и пароль совпадают с записью в users.json.
    if not isinstance(login, str) or not isinstance(password, str):
        return False
    if not login or not password:
        return False
    try:
        with user.open(encoding='utf-8') as f:
            users = json.load(f)                 # {login: password}
    except FileNotFoundError:
        return False
    return users.get(login) == password
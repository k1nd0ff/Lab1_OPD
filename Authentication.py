import json
from pathlib import Path

file = Path(__file__).with_name('user.json')


def _load_users() -> dict:
    if not file.exists():
        return {}
    with file.open(encoding='utf-8') as f:
        return json.load(f)


def _save_users(users: dict) -> None: #
    with file.open('w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def check_credentials(login: str, password: str) -> bool: # True, если логин/пароль совпадают с записью в user.json.
    if not isinstance(login, str) or not isinstance(password, str):
        return False
    if not login or not password:
        return False

    users = _load_users()
    return users.get(login) == password
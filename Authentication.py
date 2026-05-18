import json
from pathlib import Path

file = Path(__file__).with_name('user.json')


def check_credentials(login: str, password: str) -> bool: # True, если login и password совпадают с записью в user.json.
    if not isinstance(login, str) or not isinstance(password, str):
        return False
    if not login or not password:
        return False

    if not file.exists():
        return False

    with file.open(encoding='utf-8') as f:
        users = json.load(f)          # {login: password}
    return users.get(login) == password

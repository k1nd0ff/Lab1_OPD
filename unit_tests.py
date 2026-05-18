import unittest
import os
import json
from Authentication import check_credentials

# Временный файл‑база, который будет создаваться только для тестов
random_guys = {
    "biba": "goida",
    "boba": "someone"
}
test = 'user.json'      # тот же путь, что использует файл аунтификации


class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls): # сохраняем оригинальный файл (если он есть) и заменяем его тестовыми данными
        cls._backup = None
        if os.path.exists(test):
            with open(test, 'r', encoding='utf-8') as f:
                cls._backup = f.read()
        with open(test, 'w', encoding='utf-8') as f:
            json.dump(random_guys, f)

    @classmethod
    def tearDownClass(cls):
        # восстанавливаем оригинальный файл
        if cls._backup is None:
            os.remove(random_guys)
        else:
            with open(random_guys, 'w', encoding='utf-8') as f:
                f.write(cls._backup)

    def test_success(self):
        self.assertTrue(check_credentials('biba', 'goida')) # При правильном сочетании логина и пароля функция должна вернуть True.

    def test_wrong_password(self):
        self.assertFalse(check_credentials('biba', 'bad')) # Имя пользователя существует, но пароль неверный – функция должна вернуть False

    def test_unknown_user(self):
        self.assertFalse(check_credentials('ivan', 'any')) # Запрашиваемый логин отсутствует в файле user.json. Функция должна тоже вернуть False.

    def test_invalid_types(self):
        self.assertFalse(check_credentials(123, 'doe123'))  # login – int
        self.assertFalse(check_credentials('biba', None))  # password – None

    def test_empty_strings(self):
        self.assertFalse(check_credentials('', 'goida'))  # пустой логин
        self.assertFalse(check_credentials('biba', ''))  # пустой пароль

if __name__ == '__main__':
    unittest.main()
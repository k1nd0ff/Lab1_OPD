import unittest
import os
import json
from Authentication import check_credentials

# Временный файл‑база, который будет создаваться только для тестов
TEST_USERS = {
    "john": "doe123",
    "mary": "smith456"
}
TEST_FILE = 'users.json'      # тот же путь, что использует auth.py


class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # сохраняем оригинальный файл (если он есть) и заменяем его тестовыми данными
        cls._backup = None
        if os.path.exists(TEST_FILE):
            with open(TEST_FILE, 'r', encoding='utf-8') as f:
                cls._backup = f.read()
        with open(TEST_FILE, 'w', encoding='utf-8') as f:
            json.dump(TEST_USERS, f)

    @classmethod
    def tearDownClass(cls):
        # восстанавливаем оригинальный файл
        if cls._backup is None:
            os.remove(TEST_FILE)
        else:
            with open(TEST_FILE, 'w', encoding='utf-8') as f:
                f.write(cls._backup)

    def test_success(self):
        self.assertTrue(check_credentials('john', 'doe123'))

    def test_wrong_password(self):
        self.assertFalse(check_credentials('john', 'bad'))

    def test_unknown_user(self):
        self.assertFalse(check_credentials('ivan', 'any'))

    def test_invalid_types(self):
        self.assertFalse(check_credentials(123, 'doe123'))   # login не строка
        self.assertFalse(check_credentials('john', None))   # пароль не строка

    def test_empty_strings(self):
        self.assertFalse(check_credentials('', 'doe123'))
        self.assertFalse(check_credentials('john', ''))

if __name__ == '__main__':
    unittest.main()
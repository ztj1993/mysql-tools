import unittest

from .main import App


def TestInit():
    import os
    os.environ['MYSQL_HOST'] = 'localhost'
    os.environ['MYSQL_PORT'] = '3306'
    os.environ['MYSQL_USER'] = 'root'
    os.environ['MYSQL_PASSWORD'] = ''
    os.environ['MYSQL_CHARSET'] = 'utf8mb4'


TestInit()


class TestApp(unittest.TestCase):
    def test_adduser(self):
        """测试初始化"""
        App({
            '<hostname>': 'localhost',
            '<username>': 'testing',
            '<password>': '',
            'adduser': True,
        }).adduser()

    def test_passwd(self):
        """测试初始化"""
        App({
            '<hostname>': 'localhost',
            '<username>': 'testing',
            '<password>': '123456',
            'adduser': True,
        }).passwd()

    def test_create_database(self):
        App({
            '<database>': 'testing',
            'create': True,
            'database': True,
        }).passwd()

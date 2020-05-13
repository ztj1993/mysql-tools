"""
Usage:
  mysqltools.py [options] adduser <hostname> <username> [<password>]
  mysqltools.py [options] passwd <hostname> <username> [<password>]
  mysqltools.py [options] create database <database>
  mysqltools.py --help
  mysqltools.py --version

Options:
  --help                   show help options.
  --version                print program version.
  --host=host              mysql server host [default: localhost]
  --port=port              mysql server port [default: 3306]
  --user=user              mysql server user [default: root]
  --password=password      mysql server password [default: ]
  --charset=charset        mysql server charset [default: utf8mb4]

Arguments:
  hostname         mysql host name user
  username         mysql user name
  password         mysql user password
  database         mysql data base

Actions:
  adduser       add new user
  passwd        modify user password
"""

__VERSION__ = 'mysqltools 0.0.1'

import os
import logging

import pymysql.cursors
from docopt import docopt
from registry import Registry

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class App(object):
    def __init__(self, args):
        self.args = args
        self.options = Registry()
        self.init_options()
        self.init_env()
        self.client = self.mysql_server()

    def init_options(self):
        self.options.load(dict(args=self.args))
        self.options.default('args.<hostname>', 'localhost')
        self.options.default('args.<password>', '')

    def dispose(self):
        args = self.options.get('args')
        if args.get('adduser'):
            self.adduser()
        elif args.get('passwd'):
            self.passwd()
        elif args.get('create'):
            if args.get('database'):
                self.create_database()
            else:
                pass
        else:
            pass

    def mysql_server(self):
        options = self.options.get('server')
        [logging.debug('MySQL Server: %s=%s' % (key, value)) for key, value in options.items()]
        try:
            return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **options)
        except pymysql.err.MySQLError as ex:
            logging.error(ex)
            exit(ex.args[0])

    def init_env(self):
        """加载环境变量"""
        self.options.set('server', dict(
            host=os.getenv('MYSQL_HOST', self.options.get('args.--host')),
            port=int(os.getenv('MYSQL_PORT', self.options.get('args.--port'))),
            user=os.getenv('MYSQL_USER', self.options.get('args.--user')),
            password=os.getenv('MYSQL_PASSWORD', self.options.get('args.--password')),
            charset=os.getenv('MYSQL_CHARSET', self.options.get('args.--charset')),
        ))

    def execute(self, sql):
        sql_list = [i for i in sql.split('\n') if i != '']
        with self.client.cursor() as cursor:
            for sql in sql_list:
                logging.debug('Execute Sql: %s' % sql)
                cursor.execute(sql)
        self.client.commit()

    def adduser(self):
        self.execute(__SQL_ADDUSER__ % dict(
            hostname=self.options.get('args.<hostname>'),
            username=self.options.get('args.<username>'),
            password=self.options.get('args.<password>'),
        ))

    def passwd(self):
        self.execute(__SQL_PASSWD__ % dict(
            hostname=self.options.get('args.<hostname>'),
            username=self.options.get('args.<username>'),
            password=self.options.get('args.<password>'),
        ))

    def create_database(self):
        self.execute(__SQL_CREATE_DATABASE__ % dict(
            database=self.options.get('args.<database>'),
        ))


__SQL_ADDUSER__ = """
CREATE USER IF NOT EXISTS `%(username)s`@`%(hostname)s` IDENTIFIED BY '%(password)s';
CREATE DATABASE IF NOT EXISTS `%(username)s`;
GRANT ALL PRIVILEGES ON `%(username)s`.* TO `%(username)s`@`%(hostname)s`;
GRANT ALL PRIVILEGES ON `%(username)s\_%%`.* TO `%(username)s`@`%(hostname)s`;
"""

__SQL_PASSWD__ = """
ALTER USER IF EXISTS `%(username)s`@`%(hostname)s` IDENTIFIED BY '%(password)s';
"""

__SQL_CREATE_DATABASE__ = """
CREATE DATABASE IF NOT EXISTS `%(database)s`;
"""

if __name__ == '__main__':
    arguments = docopt(__doc__, version=__VERSION__)
    [logging.debug('Arguments: %s=%s' % (key, value)) for key, value in arguments.items()]
    App(arguments).dispose()

# MySQL 工具库

这是一个 MySQL 工具库，由 Python 编写。

今天早晨，在编写 docker-compose 时，多个项目需要共用一个 MySQL 服务器；  
希望能找到一个轮子，可惜没有，只能自己造。

## TODO
- [x] 创建用户
- [x] 创建数据库
- [ ] 完成单元测试

## 项目地址
- [GitHub](https://github.com/ztj1993/mysql-tools)
- [DockerHub](https://hub.docker.com/r/ztj1993/mysql-tools)

## 技术栈
- [pymysql](https://pymysql.readthedocs.io/)
- [docopt](https://github.com/docopt/docopt)
- [py-ztj-registry](https://github.com/ztj1993/PythonPackages/tree/master/py_registry)

## 简单使用
```
python main.py --help
python main.py adduser localhost testing
python main.py passwd localhost testing 123456
python main.py --host=localhost create database testing_news
```

## 环境变量
- MYSQL_HOST="localhost"
- MYSQL_PORT="3306"
- MYSQL_USER="root"
- MYSQL_PASSWORD=""
- MYSQL_CHARSET="utf8mb4"

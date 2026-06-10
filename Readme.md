这是一个学习笔记项目，源于第十八章的Django入门。参考书在p333页。

1.pip install django

2.创建名为ll_project的django项目
djangos-admin startproject ll_projectdjango -admin startproject ll_project

2.创建数据库
python manage.py migrate   Python manage.py migrate

3.运行项目
python manage.py runserver 8000Python manage.py runserver 8000

4.创建应用程序所需的基础设施
python manage.py startapp learning_logsPython management .py startapp learning_logs

5.创建模型类

6.激活模型

**7.将数据库和模型类关联起来**
python manage.py makemigrations learning_logsPython manage.py makemigrationlearning_logs

**8.修改数据库**
python manage.py migrate   Python manage.py migrate

二、管理网站
1.创建超级管理员(用户名密码ll_admin,123456)
python manage.py createsuperuserPython manage.py创建超级用户

2.在admin.py中注册模型类


3.在django shell中查看数据


4.导出依赖命令
pip freeze > requirements.txt PIP冻结要求。txtpip freeze > requirements.txt PIP冻结要求。txtpip freeze > requirements.txt PIP冻结要求。txt

5.运行命令
python manage.py runserverPython manage.py runserver


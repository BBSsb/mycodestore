1.pip install django

2.创建名为ll_project的django项目
djangos-admin startproject ll_project

2.创建数据库
python manage.py migrate

3.运行项目
python manage.py runserver 8000

4.创建应用程序所需的基础设施
python manage.py startapp learning_logs

5.创建模型类

6.激活模型

**7.将数据库和模型类关联起来**
python manage.py makemigrations learning_logs

**8.修改数据库**
python manage.py migrate

二、管理网站
1.创建超级管理员(用户名密码ll_admin,123456)
python manage.py createsuperuser

2.在admin.py中注册模型类


3.在django shell中查看数据


4.导出依赖命令
pip freeze > requirements.txt 


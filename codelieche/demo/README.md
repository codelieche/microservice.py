## codelieche demo

#### 1. 初始化环境
> 先打包：python setup.py sdist build

```bash
python3 -m venv env
source env/bin/activate

pip install ../dist/codelieche-0.0.1.tar.gz 
```

#### 2. 创建django项目
```bash
django-admin startproject demo
python manage.py startapp store

python manage.py makemigrations
python manage.py migrate
```

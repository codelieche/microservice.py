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


#### 3. 使用mysql数据库

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DEMO_DEVELOP_DB', 'demo_develop'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'root'),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', 3306)
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}
```
## codelieche

> Codelieche Python Utils Package


### build

```bash
python setup.py sdist build
```
打包后，在dist目录会看到codelieche-0.0.1.tar.gz

然后可以到虚拟环境中使用
````bash
python3 -m venv codetest
source codetest/bin/activate

pip install codelieche-0.0.1.tar.gz
```
再次执行pip freeze查看刚刚安装的包。


### 包的使用测试

```bash
In [1]: from codelieche.demo import demo

In [2]: demo()
Hello Demo

In [3]: from codelieche.tools import random_password

In [4]: random_password()
Out[4]: 'OolrauqAQC1WBSGb'

In [5]: random_password()
Out[5]: 'Vsmc6P4DuIe1nNqH'

In [6]: random_password(length=8)
Out[6]: 'L3nZHg2l'

In [7]: random_password(length=32)
Out[7]: 'N3PVd91OASnIZBCpEzmwXh4WKsQigMH7'
```


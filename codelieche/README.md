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

In [2]: demo
Out[2]: <function codelieche.demo.demo.demo()>

In [3]: demo()
Hello Demo


In [4]: from codelieche.tools import random_password

In [5]: random_password()
random password lenth is 16
```


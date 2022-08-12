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
- demo
```iptyon
In [1]: from codelieche.demo import demo

In [2]: demo()
Hello Demo

```

- password

```ipython
In [1]: from codelieche.tools import random_password

In [2]: random_password()
Out[2]: 'ksBrtbm9SFY1iNT4'

In [3]: from codelieche.tools import Cryptography

In [4]: k = random_password(16)

In [5]: k
Out[5]: 'ytm2OazpvxgA3X0Z'

In [6]: p = Cryptography(k)

In [7]: en_p = p.encrypt('codelieche')

In [8]: en_p
Out[8]: '878d95bb5fd643a61dcf1e86fc1751c8'

In [9]: de_p = p.decrypt(en_p)

In [10]: de_p
Out[10]: 'codelieche'
```


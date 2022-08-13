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
In [1]: from codelieche.tools import random_password, Cryptography

In [2]: k = random_password(16)

In [3]: k
Out[3]: 'bj1HWJV4ACrkmQUl'

In [4]: p = Cryptography(k)

In [5]: en_p = p.encrypt('codelieche')

In [6]: en_p
Out[6]: '3c6c2bd8c3bdb225086da69acfe93d74'

In [7]: de_p = p.decrypt(en_p)

In [8]: de_p
Out[8]: 'codelieche'

In [10]: from codelieche.django.utils import random_password, Cryptography

In [11]: k = random_password(16)

In [12]:  p = Cryptography(k)

In [13]: en_p = p.encrypt('codelieche')

In [14]: en_p
Out[14]: 'caff8c0f7072cd2c68512addb1f11bd3'

In [15]: de_p = p.decrypt(en_p)

In [16]: de_p
Out[16]: 'codelieche'
```


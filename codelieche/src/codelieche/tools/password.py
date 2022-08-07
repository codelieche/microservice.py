# -*- coding:utf-8 -*-
"""
密码相关工具
1. random_password: 随机生成一个密码，长度默认16位置
"""

import random
import string

def random_password(length=16):
  """
  随机获取N位密码
  :param length: 密码长度，默认16位
  :return 指定长度的密码
  """
  # 源头的字符串
  source = string.ascii_letters + string.digits
  # 方式1：
  # password = ''.join(random.SystemRandom().choice(source) for _ in range(length))

  # 方式2：
  password = ''.join(random.sample(source, length))
  
  return password

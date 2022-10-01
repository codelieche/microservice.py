# -*- coding:utf-8 -*-
from django.dispatch import Signal
from django.dispatch import receiver

demo_signal = Signal()
# 我们在account.views.test.py中调用：demo_signal.call(sender=request)


def demo_signal_callback(sender, **kwargs):
    print("收到demo signal:", sender, kwargs)


@receiver(signal=demo_signal)
def demo_signal_callback2(sender, **kwargs):
    print("收到demo signal callback2:", sender, kwargs)
# demo_signal.connect(demo_signal_callback2)


# 注册信号回调事件
demo_signal.connect(demo_signal_callback)

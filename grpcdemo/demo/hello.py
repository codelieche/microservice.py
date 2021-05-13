# -*- coding:utf-8 -*-
from proto.pb.hello_pb2 import HelloMessage


def test_hell_message():
    hello = HelloMessage(title="title", content="this is content")
    print(hello)

    print("===" * 10)
    data = hello.SerializeToString()
    print(data)

    hello2 = HelloMessage()
    hello2.ParseFromString(data)
    print(hello2)


if __name__ == "__main__":
    test_hell_message()

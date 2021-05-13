

## 依赖

```bash
pip install grpcio
pip install grpcio-tools
```

## proto生成python文件

```bash
# 先进入proto文件的目录
cd proto
# 执行命令
python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=. ./hello.proto
```

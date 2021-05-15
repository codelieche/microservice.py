#!/bin/bash

if [[ $PWD =~ "proto" ]]
then
  ls -alh
  files=`ls -alh`
  if ! [[ $files =~ ".proto" ]]
  then
    echo "`date '+%F %T'`: 未找到proto文件，程序退出"; exit 1;
  else
    echo "`date '+%F %T'`: 当前目录：$PWD"
  fi
else
  echo "`date '+%F %T'`: 请进入scripts目录执行脚本"
  exit 1
fi


echo "`date '+%F %T'`: 开始执行protoc命令"

# 处理函数
function generate() {
    # 1. 提取变量
    FILE=$1
    echo "`date '+%F %T'`: 开始处理${FILE}.proto: (${FILE}, gateway ${GATEWAY})"

    # 2. 生成grpc proto相关代码
    # pip install grpcio-tools
    python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=. ./${FILE}.proto
}

#generate base
#generate hello
generate stream
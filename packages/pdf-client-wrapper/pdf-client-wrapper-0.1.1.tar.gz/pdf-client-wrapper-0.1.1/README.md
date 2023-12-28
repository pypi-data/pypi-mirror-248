# pdf-client-wrapper

## 开发环境搭建

1. 拉取所有子仓库
1. 安装开发库
1. 执行脚本 `bin/compile_proto.sh`，编译 `proto` 文件

## 从源代码安装

``` bash
# TODO 注意 0.0.1 版本一定要加 -e 参数，因为模块目录下没有 __init__.py 文件，安装的时候该目录的代码会被忽略
pip install -e git+https://e.coding.net/xymedimg/pdf-server/pdf-client-wrapper.git@0.0.1#egg=pdf-client-wrapper
pipenv install -e git+https://e.coding.net/xymedimg/pdf-server/pdf-client-wrapper.git@0.0.1#egg=pdf-client-wrapper
```
# yml format 配置文件格式化工具说明

## 作用

依据各个格式化模块,将模块对应的yml配置格式化,修改配置,替换关键信息,然后将新配置复制至模块指定的文件中

**注意**目标文件会被覆盖

## 文件目录及说明

```text
yml-format
 ├── cache                  // 缓存文件夹
 ├── config                 // 配置文件夹
 │   ├── application.yml    // 配置信息
 │   ├── banner.txt         // banner
 │   └── logger.json        // 日志配置
 ├── config.py              // 全局配置
 ├── format.py              // 程序主类
 ├── format_demo.py         // 模块模板
 ├── format_model.py        // 模块父类
 ├── from-yml               // yml 源文件夹
 │   └── application-db.yml // yml 源文件
 ├── logger.py              // 日志实现
 ├── main.py                // 入口
 ├── readme.md              
 ├── requirements.txt       // 依赖库
 ├── target-yml             // yml 目标文件夹
 │   └── application-db.yml // yml 格式化后的 范例
 ├── util.py                // 工具类
 ├── yml                    // 自定义模块文件夹
 │   ├── dev                // dev 模式
 │   │   └── dev_application.py
 │   └── pro                // pro 模式
 │       └── pro_application.py
 └── __init__.py
```

## 使用方法

1. 安装依赖库 requirements.txt

2. 修改配置文件路径

```yaml
yml-format:
  # 源文件路径
  from-base-path: D:/Github/yml-format/from-yml
  # 目标基础路径
  target-base-path: D:/Github/yml-format/target-yml
  # 模块路径(相对于项目根路径)
  yml-model-path: ./yml
  # 使用的模块前缀(可编写多种环境的模块 例如: dev_ , pro_ 然后指定使用那些模块)
  yml-model-pre: pro_
```

3. 运行

```shell
python main.py
```

## 修改自己的YML格式化模块

1. 复制 [format_demo.py](./format_demo.py) 到 文件夹 [yml](./yml) 中

2. 按照 format_demo.py 注释编写具体需求

3. 修改之后即可运行程序

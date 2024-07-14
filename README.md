# 博通继续教育挂课脚本
博通继续教育刷课脚本
# 适用范围

本脚本适用于博通继续教育网站（http://www.tsbtgs.cn/）自动挂课使用。它采用Selenium加多进程技术，可以根据账号数量同时挂课，提高了挂课效率。

在使用本脚本前，请确保你已经安装了Selenium库和相应的WebDriver。WebDriver的路径需要与你的操作系统相匹配。对于Windows系统，本项目已包含EdgeDriver。

## 功能
- 从CSV文件中读取账号凭证。
- 同时启动多个进程以并行执行任务。
- 使用 `multiprocessing` 模块来管理并发进程。

## 系统要求
- Python 3.7或更高版本
- `csv` 模块（Python标准库的一部分）
- `os` 模块（Python标准库的一部分）
- `multiprocessing` 模块（Python标准库的一部分）

## 安装依赖
pip install selenium

## 使用方法
使用此脚本，请按照以下步骤操作：

1. 在脚本所在目录下创建一个名为 `accounts.csv` 的CSV文件。该文件应包含两列，且无标题行：`username` 和 `password`,
使用以下命令运行脚本：

    ```bash
    python multiprocess.py
    ```

这将读取 `accounts.csv` 文件并为每个账号启动一个进程。
2. 直接运行脚本并提供CSV文件：

    ```bash
    python multiprocess.py useraccount.csv
    ```


## CSV文件格式
`accounts.csv` 文件应如下格式：

username1,password1

username2,password2 

username3,password3 

 …

每一行代表一个账号，其中用户名和密码之间用逗号分隔。

## 注意事项
- 确保 `processscript.py` 文件与 `multiprocess.py` 文件位于同一目录中。
- 确保 `processscript.py` 中的 `runscript` 函数已正确定义并可被导入。
- 如果在Windows上使用多进程时遇到问题，请尝试以管理员权限在命令提示符下运行脚本。

## 贡献
欢迎对此脚本做出贡献。请先Fork仓库，进行修改后提交Pull Request。

## 许可证
本项目采用MIT许可证 - 详细信息请参阅 LICENSE 文件。

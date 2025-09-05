# 🌓 BaiYin

django-blog-practice 是一个 关于django的博客系统简单练习，旨在实验性开发。

<!-- 以下通用部分勿删 -->
本项目开源部分遵循 MIT 许可证。如需闭源或额外权利，请通过以下方式联系作者获取授权。

- **开源许可证**：[MIT License](LICENSE)  
- **补充协议**：[补充协议](LICENSE-SUPPLEMENT.md)  
- **贡献协议**：[CLA](CLA.md)  

## 使用方法

### 环境配置

根据个人情况，在克隆到本地后创建虚拟环境进行实验。

#### 开发环境

- **操作系统**：Windows 10
- **Python 版本**：3.12.10

### 安装依赖

在项目目录下运行以下命令以安装依赖：

```commandline
pip install -r requirements.txt
```

### 数据库配置

项目使用 MySQL 数据库，请确保你已经安装并运行了 MySQL 服务。

#### 创建 `.env` 文件

在项目根目录下创建一个 `.env` 文件，并写入以下环境变量。请确保你已经创建了一个空的数据库。

```text
SECRET_KEY=[django secret key]  # 如果未设置，`settings.py` 会自动生成
HOST=[your mysql host]
NAME=[your mysql db name]
USER=[your mysql username]
PASSWORD=[your mysql password]
```

### 示例 `.env` 文件

```text
SECRET_KEY=your_generated_django_secret_key
HOST=localhost
NAME=myprojectdb
USER=myusername
PASSWORD=mypassword
```

### 注意事项

- **SECRET_KEY**：如果未在 `.env` 文件中设置，`settings.py` 会自动生成一个密钥。建议在生产环境中手动设置一个安全的密钥。
- **数据库连接**：确保 MySQL 服务正在运行，并且提供的用户名和密码具有访问指定数据库的权限。

## 贡献指南
我们欢迎任何形式的贡献！请阅读我们的 贡献指南 来了解如何提交更改。
联系方式
如有任何问题或建议，请通过以下方式联系我们：

GitHub：[@baiyin123-l](https://github.com/BaiYin123-l)

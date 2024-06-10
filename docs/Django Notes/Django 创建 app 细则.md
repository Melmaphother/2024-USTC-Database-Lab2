# Django 创建 app 和 model 细则

## 流程

1. 安装 mysqlclient

   mysqlclient 负责 Django 项目与 MySQL 数据库之间的连接。之前有的用 pymysql，现在 Django 建议使用 mysqlclient

   ```bash
   pip install mysqlclient
   ```

2. 创建数据库

   在终端输入：

   ```bash
   $ mysql -u username -p password
   $ create database db_name default charset=UTF8MB4
   ```

3. 配置 Django 项目中的数据库设置（指定数据库）

   修改 setting.py

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',  # 指定使用 MySQL
           'NAME': 'db_name',          # 你的数据库名
           'USER': 'root',          # 数据库用户
           'PASSWORD': 'password',  # 数据库密码
           'HOST': 'localhost',                   # 数据库服务器地址
           'PORT': '3306',                        # 数据库端口
       }
   }
   ```

   这样在迁移数据到数据库时，就可以知道迁移到哪个数据库。

4. 在 Django 项目中定义 App

   Django 规定，如果要使用模型，必须要创建一个 app：

   ```bash
   python manage.py startapp app_name
   ```

   这会在 Django 项目目录中创建 app_name 的目录

5. 配置 Django 项目中的 App 信息

   修改 setting.py 中的 INSTALLED_APPS

   ```python
   INSTALLED_APPS = [
       ...,
       'app_name.apps.AppNameConfig',
   ]
   ```

    这样确保 Django 会处理你 App 中的迁移文件。

6. 修改 app_name / models.py 文件，创建/查询数据表

   如果数据库有变动，需要执行：

   - 创建新的迁移文件（migrations）

   ```bash
   python manage.py makemigrations
   ```

   - 应用之前创建的迁移文件到数据库（migrate）

   ```bash
   python manage.py migrate
   ```

## 注释

### App 的意义

> 来自 ChatGPT
>
> 在 Django 中，**App** 是一个应用程序模块，它通常封装了处理一个特定业务功能的全部代码，包括模型（Model）、视图（View）、模板（Template）、URLs 配置等。每个 Django App 应该设计为尽可能独立，这样它就可以在不同的项目中重用。
>
> > 为什么模型必须定义在 App 内？
>
> 模型（Model）是 Django 中表示数据库结构的 Python 类。在 Django 设计哲学中，每个模型都属于一个特定的 App，这有几个理由：
>
> - **模块化**：将模型定义在 App 内有助于保持代码的模块化和组织性。每个 App 负责处理其特定的业务逻辑和数据模型。
> - **重用性**：通过将功能相关的模型、视图和模板封装在同一个 App 中，可以轻松地在不同的项目之间重用整个 App。
> - **维护性**：这种结构使得管理和维护大型项目变得更加容易，因为相关的功能和数据定义都在同一个逻辑单元内。

### makemigrations 和 migrate 的区别

> 来自 ChatGPT
>
> **`makemigrations`**:
>
> - 这个命令负责创建新的迁移文件（migrations）。迁移文件是 Django 的方式来跟踪和管理数据库中模型（即数据库表）的变更，如添加新表、更改现有表的结构（添加或删除字段）、或更改数据库的其他元数据。
> - 当你修改了应用中的模型定义（`models.py`）并希望将这些变更应用到数据库时，首先需要运行 `makemigrations` 命令。这个命令将检查你的模型定义与当前数据库结构之间的差异，并为这些变更创建迁移文件。
>
> **`migrate`**:
>
> - `migrate` 命令负责应用之前创建的迁移文件到数据库。这意味着它会实际改变数据库的结构，以匹配你的模型定义。
> - 当运行 `migrate` 命令时，Django 查找所有尚未应用的迁移（migrations），并按顺序应用它们，更新数据库结构。这包括创建新表、修改现有表的结构或甚至更改数据库的更复杂的结构。

### App 内文件目录的含义

   > 来自 ChatGPT
   >
   > ### App 级别的文件 (`app_name` 目录内)
   >
   > - **`__init__.py`**: 这是一个空的 Python 文件，其存在使 Python 将这个目录视为一个包（Package）。这样你才能从其他地方导入这个目录中的模块。
   > - **`admin.py`**: 用于注册你的模型，以便它们可以通过 Django 的管理后台进行管理。这是 Django 强大的管理界面的一部分，允许非技术用户轻松管理应用的内容。
   > - **`apps.py`**: 包含这个应用的配置类。这个类通常包含应用的一些配置信息，如应用的名称。它在 `INSTALLED_APPS` 配置中被引用。
   > - **`models.py`**: 定义应用的数据模型。这里是定义数据库表结构的地方，Django 通过这些定义来管理数据库的 schema。
   > - **`tests.py`**: 用于编写应用的测试用例。测试是开发过程中的一个重要部分，确保你的代码在更改后依然按预期工作。
   > - **`views.py`**: 包含应用的视图逻辑。视图负责处理用户的请求并返回响应。这些响应可以是 HTML 页面，重定向，404 错误等。
   > - **`migrations` 文件夹**: 存储与这个应用相关的迁移文件。迁移是 Django 用来对数据库进行版本控制的方式。每当你修改了 `models.py` 文件中的模型，你通常需要生成一个新的迁移来更新数据库。
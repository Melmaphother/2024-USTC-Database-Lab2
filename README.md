# 2024-USTC-Database-Lab2

<img src="logo.png" alt="Logo" style="zoom: 25%;" />

## 基本信息

1. 本项目为 2024 年 USTC 数据库设计与应用（陈欢欢，周熙人）实验二，选择以银行管理系统为主题，实现一个 USTC 银行在线管理平台。

2. 本项目基于 Django 框架，以 MySQL 为后端，以 HTML、CSS、JavaScript 为前端。

3. 本文档主要包括项目的快速开始、项目细节，查看更多说明请查看 docs 文件夹。
   | 文件 | 链接 |
   | --- | --- |
   | 需求分析 | [Demand Analysis](docs/Demand%20Analysis.md) |
   | 设计分析 | [Design Analysis](docs/Design%20Analysis.md) |
   | 项目日志 | [Project Log](docs/Project%20Log.md) |
   | 实验手册 | [Experiment Manual](docs/Exp%20Manual.pdf) |
   | 我的 Django 笔记 | [Django Note](docs/Django%20Notes/Django%20Note.md) |

## 快速开始

1. 本项目使用的软件有：

   | 软件             | 版本   | 下载方式                                          |
   | ---------------- | ------ | ------------------------------------------------- |
   | MySQL            | 8.0    | [MySQL](https://www.mysql.com/cn/downloads/)      |
   | Python           | 3.11   | [Anaconda](https://www.anaconda.com/download)     |
   | Django           | 5.0    | [Django](https://www.djangoproject.com/download/) |
   | DataGrip         | 2024.1 | [DataGrip](https://www.jetbrains.com/datagrip/)   |
   | PyCharm          | 2024.1 | [Pycharm](https://www.jetbrains.com/pycharm/)     |
   | PDManer 元数建模 | 4.9    | [pdmaner](https://gitee.com/robergroup/pdmaner)   |

2. 简单配置流程
   - clone 本项目
     ```bash
     $ git clone https://github.com/Melmaphother/2024-USTC-Database-Lab2.git
     ```
   - 安装 MySQL，创建数据库 `bank_manage_system`，导入 `src/sql_src/init_database.sql` 文件
     ```bash
     $ mysql -u username -p password
     $ create database db_name default charset=UTF8MB4
     ```
   - 安装 Anaconda，搭建 Python 环境
     ```bash
     $ conda create -n django python=3.11
     $ conda activate django
     ```
   - 安装必要的包
     ```bash
     $ pip install -r requirements.txt
     ```
   - 进入目录 `src/BankManageSystem`，运行 Django 项目
     ```bash
     $ python manage.py runserver
     ```
   - 在浏览器中输入 `localhost:8000`，即可查看项目

## 项目细节

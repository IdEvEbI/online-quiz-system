# 项目初始化与本地环境准备

## 一、目标

1. 在 **GitHub** 上创建仓库，初始化结构。
2. 设置 **Git Flow** 分支策略。
3. 用 **Docker Desktop** 安装 **MySQL**。
4. 确认 **Python 3.9.6** 环境。

## 二、开发日志

### 2.1 初始化 GitHub 仓库

1. 登录 **GitHub**，创建仓库 `online-quiz-system`。
2. 添加 `.gitignore`（见下方示例）。

   ```gitignore
   # Python
   __pycache__/
   *.py[cod]
   *.so
   *.egg
   *.egg-info/
   dist/
   build/
   *.venv/
   venv/
   env/
   *.log
   
   # Docker
   *.dockerignore
   
   # Node.js (Vue)
   node_modules/
   dist/
   
   # macOS
   .DS_Store
   
   # MySQL
   mysql-data/
   ```

3. 检查文件：`.gitignore`、`README`、`LICENSE`。
4. 本地克隆并初始化 **Git Flow**：

   ```bash
   git clone https://github.com/<你的用户名>/online-quiz-system.git
   cd online-quiz-system
   # 初始化 Git Flow
   git flow init -d
   git push origin main
   git push origin develop
   ```

   > 提示：若未安装 `git-flow`，运行 `brew install git-flow`。

### 2.2 安装 MySQL

1. 启动 **Docker Desktop**（若未安装，从 [官网](https://www.docker.com/products/docker-desktop/) 下载）。
2. 拉取并运行 **MySQL**：

   ```bash
   # 拉取 MySQL 8.0 镜像
   docker pull mysql:8.0
   # 启动容器
   docker run -d -p 3306:3306 --name mysql-quiz -e MYSQL_ROOT_PASSWORD=root1234 -e MYSQL_DATABASE=quiz_db mysql:8.0
   ```

3. 验证：

   ```bash
   # 检查容器状态
   docker ps
   # 连接 MySQL（密码：root1234）
   mysql -h 127.0.0.1 -u root -p
   # 查看数据库
   SHOW DATABASES;
   ```

   > 提示：若无 MySQL 客户端，运行 `brew install mysql`。

### 2.3 配置 Python 虚拟环境

#### 2.3.1 关于虚拟环境

- **作用**：隔离项目依赖，避免冲突。
- **创建**：`python3 -m venv venv` 创建名为 `venv` 的虚拟环境。
- **激活**：`source venv/bin/activate`，提示符前出现 `(venv)`。
- **退出**：`deactivate`。
- **注意**：操作前确保虚拟环境激活。

#### 2.3.2 配置步骤

1. 检查版本并创建虚拟环境：

   ```bash
   # 检查 Python 版本
   python3 --version  # 预期：3.9.6
   # 创建并激活虚拟环境
   python3 -m venv venv
   source venv/bin/activate
   ```

2. 安装 **Flask**：

   ```bash
   pip install flask
   ```

3. （可选）升级 **Pip**：

   ```bash
   deactivate
   ./venv/bin/python3 -m pip install --upgrade pip
   source venv/bin/activate
   ```

## 三、验证结果与提交

### 3.1 验证结果

1. **本地代码仓库**：有 `main` 和 `develop` 分支，文件齐全。
2. **MySQL**：能连接并看到 `quiz_db`。
3. **Python**：在虚拟环境中运行：

   ```bash
   python -c "import flask; print(flask.__version__)"
   ```

   - 预期输出：类似 `3.1.0`。
   - 若出现 `DeprecationWarning`，属正常现象，无影响。

### 3.2 提交到 GitHub

```bash
git add docs/setup.md
git commit -m "完成项目初始化和环境准备，更新 setup.md"
git push origin develop
```

## 四、常见问题

- **安装错包**：若误装 `flash`，运行 `pip uninstall flash -y` 再装 `flask`。
- **虚拟环境未激活**：若无 `(venv)`，运行 `source venv/bin/activate`。
- **ModuleNotFoundError**：检查拼写或虚拟环境状态。

## 五、扩展阅读

- **VSCode 配置**：安装 Python 扩展，选择虚拟环境解释器（`/venv/bin/python3`）。
- **Docker 基础**：[Docker 官方文档](https://docs.docker.com/get-started/)。
- **MySQL 使用**：[MySQL 入门教程](https://dev.mysql.com/doc/refman/8.0/en/tutorial.html)。

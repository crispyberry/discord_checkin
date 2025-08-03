# Discord Check-in Bot

*Language / 语言: [English](#english) | [中文](#中文)*

---

## English

A Discord bot that allows users to perform daily check-ins using the `/blast` command and automatically saves check-in information to a database.

## 🎯 What can this bot do?

- **Check-in functionality**: Users can check in on Discord using `/blast` command
- **Auto recording**: Automatically saves username, ID, and check-in time to cloud database
- **Status checking**: Use `/credit` command to check your credits and consecutive days
- **Beautiful interface**: All responses use attractive Discord embed messages

## 📋 Prerequisites

Before getting started, you'll need:

1. **A computer** - Windows, Mac, or Linux
2. **Discord account** - To create the bot
3. **Internet connection** - To download files and connect to services

## 🚀 Installation Steps

### Step 1: Install Python

If Python isn't installed on your computer:

1. Visit [python.org](https://www.python.org/downloads/)
2. Download the latest Python version
3. During installation, **make sure to check** "Add Python to PATH"
4. After installation, open Command Prompt (Windows) or Terminal (Mac/Linux)
5. Type `python --version` to confirm successful installation

### Step 2: Download Bot Code

1. Download all project files to your computer
2. Extract to an easily accessible folder (e.g., Desktop)

### Step 3: Install Dependencies

1. Open Command Prompt or Terminal
2. Navigate to the bot folder (using `cd` command)
3. Run the following command to install required components:

```bash
pip install -r requirements.txt
```

This command automatically downloads all components needed for the bot.

### Step 4: Create Discord Bot

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give your bot a name, like "Check-in Bot"
4. Click "Bot" in the left sidebar
5. Click "Add Bot"
6. Copy the bot's Token - **This is important, don't share it with anyone!**
7. Under "Privileged Gateway Intents", enable all permissions
8. Click "OAuth2" > "URL Generator" in the left sidebar
9. In "Scopes", select "bot"
10. In "Bot Permissions", select:
    - Send Messages
    - Use Slash Commands
    - Read Message History
    - Embed Links
11. Copy the generated link, open it in your browser, and add the bot to your Discord server

### Step 5: Set up Database (Supabase)

1. Visit [supabase.com](https://supabase.com) and create a free account
2. Click "New Project"
3. Fill in project name and password
4. Wait for project creation (about 2 minutes)
5. On the project homepage, find and copy:
   - Project URL
   - anon public key
6. Click "SQL Editor" in the left sidebar
7. Copy and paste the following code, then click "Run":

```sql
-- Create check-in records table
CREATE TABLE user_check_ins (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    username TEXT NOT NULL,
    guild_id TEXT,
    check_in_time TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX user_id_idx ON user_check_ins(user_id);
CREATE INDEX check_in_time_idx ON user_check_ins(check_in_time);
CREATE INDEX guild_id_idx ON user_check_ins(guild_id);

-- Enable row level security
ALTER TABLE user_check_ins ENABLE ROW LEVEL SECURITY;

-- Create access policies
CREATE POLICY "Allow insert for authenticated users" ON user_check_ins
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select for authenticated users" ON user_check_ins
    FOR SELECT USING (true);
```

### Step 6: Configure Bot

1. In the bot folder, find the `config_example.py` file
2. Copy this file and rename it to `config.py`
3. Open `config.py` with a text editor (Notepad works)
4. Replace the following information with your actual data:

```python
# Discord bot configuration
DISCORD_TOKEN = "Your Discord bot Token here"
DISCORD_GUILD_ID = "Your Discord server ID here"

# Supabase database configuration
SUPABASE_URL = "Your Supabase project URL here"
SUPABASE_KEY = "Your Supabase public key here"
```

**How to get Discord Server ID:**
1. In Discord, right-click your server name
2. Click "Copy Server ID" (if you don't see this option, enable Developer Mode in Discord settings first)

### Step 7: Start the Bot

1. In Command Prompt or Terminal, make sure you're in the bot folder
2. Run the following command to start the bot:

```bash
python bot.py
```

If everything is working correctly, you'll see a message like "Bot connected".

## 🎮 How to Use the Bot

After the bot starts, you can use the following commands in your Discord server:

### Available Commands:

- **`/blast`** - Daily check-in, your information will be automatically recorded in the database
- **`/credit`** - Check your total credits and consecutive check-in days

### Usage Example:

1. Type `/blast` in any chat channel
2. The bot will reply with a beautiful check-in confirmation message
3. Your check-in information (username, time, etc.) will be automatically saved to the cloud database

## 📊 Database Information Recorded

Each time a user checks in, the system automatically records:

- **User ID**: Discord's unique user identifier
- **Username**: Your display name in Discord
- **Server ID**: The Discord server where the check-in occurred
- **Check-in time**: Exact moment of check-in (including date and time)
- **Record creation time**: When data was saved to the database

## ❓ Troubleshooting

### Bot won't start?

1. **Check Python installation**: Type `python --version` in command line
2. **Check component installation**: Confirm you've run `pip install -r requirements.txt`
3. **Check config file**: Confirm `config.py` exists and information is correct

### Bot not responding to commands?

1. **Check bot permissions**: Confirm bot has send message permissions in the server
2. **Check command format**: Use `/blast` not `$blast`
3. **Check console**: The command line window where the bot runs will show error messages

### Database connection failed?

1. **Check Supabase configuration**: Confirm URL and key are copied correctly
2. **Check internet connection**: Confirm your computer can access the internet
3. **Check database tables**: Confirm you've created the necessary tables in Supabase

## 🔒 Security Notes

- **Protect your Token**: Discord bot Token is like a password, never share it with others
- **Data security**: All check-in data is protected using Supabase's security system
- **Privacy protection**: Bot only records basic check-in information, no other personal data

## 💡 Technical Notes

- Developed using Python programming language
- Built on discord.py library
- Uses Supabase as cloud database
- Supports Slash Commands
- Includes comprehensive error handling

## 🆘 Need Help?

If you encounter any issues:

1. **Double-check**: Re-read the relevant steps, confirm each step is completed correctly
2. **Check error messages**: Red text in the command line window usually contains problem hints
3. **Try restarting**: Sometimes restarting the bot can solve temporary issues
4. **Seek help**: Ask experienced friends or post questions in relevant communities

## 📝 License

This project uses the MIT open source license, you can freely use, modify, and share it.

---

## 中文

这是一个 Discord 机器人，可以让用户使用 `/blast` 命令进行签到，并将签到信息自动保存到数据库中。

## 🎯 这个机器人能做什么？

- **签到功能**: 用户在 Discord 中输入 `/blast` 就能签到
- **自动记录**: 自动保存用户的姓名、ID 和签到时间到云端数据库
- **状态检查**: 使用 `/credit` 命令查看你的积分和连续签到天数
- **美观界面**: 所有回复都使用漂亮的 Discord 消息卡片

## 📋 安装前准备

在开始之前，您需要准备以下内容：

1. **一台电脑** - Windows、Mac 或 Linux 都可以
2. **Discord 账号** - 用于创建机器人
3. **网络连接** - 用于下载所需文件和连接服务

## 🚀 详细安装步骤

### 第一步：安装 Python（编程语言）

如果您的电脑还没有安装 Python：

1. 访问 [python.org](https://www.python.org/downloads/)
2. 下载最新版本的 Python
3. 安装时**一定要勾选** "Add Python to PATH" 选项
4. 安装完成后，打开命令提示符（Windows）或终端（Mac/Linux）
5. 输入 `python --version` 确认安装成功

### 第二步：下载机器人代码

1. 下载本项目的所有文件到您的电脑
2. 解压到一个容易找到的文件夹（例如桌面）

### 第三步：安装必要组件

1. 打开命令提示符或终端
2. 进入到机器人文件夹（使用 `cd` 命令）
3. 输入以下命令安装所需组件：

```bash
pip install -r requirements.txt
```

这个命令会自动下载机器人运行所需的所有组件。

### 第四步：创建 Discord 机器人

1. 访问 [Discord 开发者门户](https://discord.com/developers/applications)
2. 点击 "New Application"（新建应用）
3. 给您的机器人起个名字，比如 "签到机器人"
4. 点击左侧的 "Bot"（机器人）选项
5. 点击 "Add Bot"（添加机器人）
6. 复制机器人的 Token（令牌）- **这个很重要，不要分享给别人！**
7. 在 "Privileged Gateway Intents" 下面，开启所有权限
8. 点击左侧的 "OAuth2" > "URL Generator"
9. 在 "Scopes" 中选择 "bot"
10. 在 "Bot Permissions" 中选择：
    - Send Messages（发送消息）
    - Use Slash Commands（使用斜杠命令）
    - Read Message History（读取消息历史）
    - Embed Links（嵌入链接）
11. 复制生成的链接，在浏览器中打开，将机器人添加到您的 Discord 服务器

### 第五步：设置数据库（Supabase）

1. 访问 [supabase.com](https://supabase.com) 并创建免费账号
2. 点击 "New Project"（新建项目）
3. 填写项目名称和密码
4. 等待项目创建完成（大约 2 分钟）
5. 在项目首页找到并复制：
   - Project URL（项目网址）
   - anon public key（公开密钥）
6. 点击左侧的 "SQL Editor"（SQL 编辑器）
7. 复制并粘贴以下代码，然后点击 "Run"（运行）：

```sql
-- 创建签到记录表
CREATE TABLE user_check_ins (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    username TEXT NOT NULL,
    guild_id TEXT,
    check_in_time TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 创建索引以提升性能
CREATE INDEX user_id_idx ON user_check_ins(user_id);
CREATE INDEX check_in_time_idx ON user_check_ins(check_in_time);
CREATE INDEX guild_id_idx ON user_check_ins(guild_id);

-- 启用行级安全
ALTER TABLE user_check_ins ENABLE ROW LEVEL SECURITY;

-- 创建访问策略
CREATE POLICY "Allow insert for authenticated users" ON user_check_ins
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select for authenticated users" ON user_check_ins
    FOR SELECT USING (true);
```

### 第六步：配置机器人

1. 在机器人文件夹中，找到 `config_example.py` 文件
2. 复制这个文件并重命名为 `config.py`
3. 用文本编辑器（记事本也可以）打开 `config.py`
4. 将以下信息替换为您的实际信息：

```python
# Discord 机器人配置
DISCORD_TOKEN = "这里填写您的 Discord 机器人 Token"
DISCORD_GUILD_ID = "这里填写您的 Discord 服务器 ID"

# Supabase 数据库配置
SUPABASE_URL = "这里填写您的 Supabase 项目网址"
SUPABASE_KEY = "这里填写您的 Supabase 公开密钥"
```

**如何获取 Discord 服务器 ID：**
1. 在 Discord 中，右键点击您的服务器名称
2. 点击 "复制服务器 ID"（如果看不到这个选项，请先在 Discord 设置中开启开发者模式）

### 第七步：启动机器人

1. 在命令提示符或终端中，确保您在机器人文件夹内
2. 输入以下命令启动机器人：

```bash
python bot.py
```

如果一切正常，您会看到类似 "机器人已连接" 的消息。

## 🎮 如何使用机器人

机器人启动后，在您的 Discord 服务器中就可以使用以下命令：

### 可用命令：

- **`/blast`** - 进行签到，您的信息会被自动记录到数据库
- **`/credit`** - 检查您的总积分和连续签到天数

### 使用示例：

1. 在任意聊天频道输入 `/blast`
2. 机器人会回复一个漂亮的签到确认消息
3. 您的签到信息（用户名、时间等）会自动保存到云端数据库

## 📊 数据库记录的信息

每次用户签到时，系统会自动记录以下信息：

- **用户 ID**: Discord 的唯一用户标识
- **用户名**: 您在 Discord 中显示的名字
- **服务器 ID**: 签到所在的 Discord 服务器
- **签到时间**: 精确的签到时刻（包含日期和时间）
- **记录创建时间**: 数据保存到数据库的时间

## ❓ 常见问题解决

### 机器人无法启动？

1. **检查 Python 安装**: 在命令行输入 `python --version`
2. **检查组件安装**: 确认已运行 `pip install -r requirements.txt`
3. **检查配置文件**: 确认 `config.py` 文件存在且信息正确

### 机器人无法响应命令？

1. **检查机器人权限**: 确认机器人在服务器中有发送消息权限
2. **检查命令格式**: 使用 `/blast` 而不是 `$blast`
3. **查看控制台**: 运行机器人的命令行窗口会显示错误信息

### 数据库连接失败？

1. **检查 Supabase 配置**: 确认 URL 和密钥复制正确
2. **检查网络连接**: 确认您的电脑可以访问互联网
3. **检查数据库表**: 确认已在 Supabase 中创建了必要的表

## 🔒 安全说明

- **保护您的 Token**: Discord 机器人 Token 就像密码，绝不要分享给他人
- **数据安全**: 所有签到数据都使用 Supabase 的安全系统保护
- **隐私保护**: 机器人只记录基本的签到信息，不会收集其他个人数据

## 💡 技术说明（给有兴趣的用户）

- 使用 Python 编程语言开发
- 基于 discord.py 库构建
- 使用 Supabase 作为云数据库
- 支持斜杠命令（Slash Commands）
- 包含完整的错误处理机制

## 🆘 需要帮助？

如果您在使用过程中遇到任何问题：

1. **仔细检查**: 重新阅读相关步骤，确认每一步都正确完成
2. **查看错误信息**: 命令行窗口中的红色文字通常包含问题提示
3. **重启尝试**: 有时重启机器人可以解决临时问题
4. **寻求帮助**: 可以向有经验的朋友求助，或在相关社区提问

## 📝 许可证

本项目采用 MIT 开源许可证，您可以自由使用、修改和分享。
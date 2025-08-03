# Discord 签到机器人 (Discord Sign-in Bot)

这是一个 Discord 机器人，可以让用户使用 `/blast` 命令进行签到，并将签到信息自动保存到数据库中。

## 🎯 这个机器人能做什么？

- **签到功能**: 用户在 Discord 中输入 `/blast` 就能签到
- **自动记录**: 自动保存用户的姓名、ID 和签到时间到云端数据库
- **状态检查**: 使用 `/credit` 命令查看机器人是否正常工作
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
CREATE TABLE user_sign_ins (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    username TEXT NOT NULL,
    guild_id TEXT,
    sign_in_time TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 创建索引以提升性能
CREATE INDEX user_id_idx ON user_sign_ins(user_id);
CREATE INDEX sign_in_time_idx ON user_sign_ins(sign_in_time);
CREATE INDEX guild_id_idx ON user_sign_ins(guild_id);

-- 启用行级安全
ALTER TABLE user_sign_ins ENABLE ROW LEVEL SECURITY;

-- 创建访问策略
CREATE POLICY "Allow insert for authenticated users" ON user_sign_ins
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select for authenticated users" ON user_sign_ins
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
- **`/credit`** - 检查机器人状态，确认一切正常工作

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
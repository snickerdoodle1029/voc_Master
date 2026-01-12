# 🚀 Streamlit Cloud 部署指南

## ✅ 安全检查结果

经过代码扫描，**未发现任何硬编码的 API Key**。

当前项目：
- ✅ 不使用任何外部API服务（OpenAI、Anthropic等）
- ✅ 不包含任何API密钥
- ✅ 完全基于规则的分析引擎，无需API调用
- ✅ 所有依赖都是Python标准库和Streamlit

## 📦 依赖检查

项目的依赖库已在 `requirements.txt` 中列出：
- `streamlit>=1.28.0` - Web框架

其他使用的库（`re`, `typing`, `collections`）都是Python标准库，无需额外安装。

## 🔐 如需添加API密钥（未来扩展）

如果将来需要添加外部API服务（如OpenAI、Anthropic等），请按以下方式配置：

### 1. 修改代码使用 st.secrets

```python
# ❌ 错误：硬编码API Key
api_key = "sk-xxxxx"

# ✅ 正确：从secrets读取
api_key = st.secrets["API_KEY"]
# 或
api_key = st.secrets.get("API_KEY")
```

### 2. 在 Streamlit Cloud 配置 Secrets

1. **登录 Streamlit Cloud**
   - 访问 https://share.streamlit.io/
   - 登录你的账号

2. **进入应用设置**
   - 在应用列表中，点击你的应用
   - 点击右上角的 **"⋮"（三个点）** 菜单
   - 选择 **"Settings"** 或 **"Manage app"**

3. **配置 Secrets**
   - 找到 **"Secrets"** 或 **"App secrets"** 部分
   - 点击 **"Edit secrets"** 或 **"Add secrets"**

4. **添加密钥**
   - 使用TOML格式添加，例如：
   ```toml
   API_KEY = "sk-your-api-key-here"
   ANOTHER_KEY = "another-value"
   ```
   - 点击 **"Save"**

5. **重启应用**
   - 配置完成后，应用会自动重启
   - 密钥将在应用重启后生效

### 3. Secrets 格式示例

如果需要添加多个密钥，使用TOML格式：

```toml
# API Keys
OPENAI_API_KEY = "sk-xxxxx"
ANTHROPIC_API_KEY = "sk-ant-xxxxx"

# 配置项
MODEL_NAME = "gpt-4"
MAX_TOKENS = "1000"

# 嵌套配置
[database]
host = "localhost"
port = "5432"
```

### 4. 在代码中访问 Secrets

```python
import streamlit as st

# 访问简单密钥
api_key = st.secrets["OPENAI_API_KEY"]

# 访问嵌套配置
db_host = st.secrets["database"]["host"]
db_port = st.secrets["database"]["port"]

# 安全访问（带默认值）
api_key = st.secrets.get("OPENAI_API_KEY", "default-key")
```

## 📝 部署步骤

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "准备部署到Streamlit Cloud"
   git push origin main
   ```

2. **访问 Streamlit Cloud**
   - 打开 https://share.streamlit.io/
   - 使用 GitHub 账号登录

3. **创建新应用**
   - 点击 **"New app"**
   - 选择你的 GitHub 仓库
   - 选择分支（通常是 `main` 或 `master`）
   - 设置 Main file path: `app.py`

4. **部署**
   - 点击 **"Deploy"**
   - 等待部署完成（通常1-2分钟）

5. **获取链接**
   - 部署成功后，你会获得一个公开链接
   - 例如：`https://your-app-name.streamlit.app`
   - 可以直接分享给用户使用

## 🔍 验证清单

部署前请确认：
- ✅ `requirements.txt` 已包含所有依赖
- ✅ `app.py` 是主文件
- ✅ 代码中无硬编码的API Key
- ✅ 代码已推送到GitHub
- ✅ 所有必要的文件都在仓库中

## ⚠️ 注意事项

1. **不要提交 secrets 文件**
   - 不要将包含真实密钥的 `.streamlit/secrets.toml` 提交到GitHub
   - 如果创建了示例文件，使用 `.gitignore` 排除

2. **定期检查代码**
   - 定期扫描代码中是否有硬编码的密钥
   - 使用工具如 `git-secrets` 或 `truffleHog` 进行扫描

3. **保护 GitHub 仓库**
   - 如果是私有项目，确保仓库设置为 Private
   - 不要公开包含敏感信息的代码

## 📚 参考资源

- [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-community-cloud)
- [Secrets 管理文档](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Streamlit Cloud 最佳实践](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)

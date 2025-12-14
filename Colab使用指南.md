# 🌐 Google Colab 云端运行指南

## 🎯 为什么使用 Colab？

- ✅ **完全免费** - 无需付费服务器
- ✅ **零安装** - 不需要本地 Node.js
- ✅ **随时可用** - 浏览器打开即用
- ✅ **强大算力** - Google 提供的云端资源

---

## 🚀 快速开始

### 方法 1：直接使用 Notebook（推荐）

1. **打开 Colab Notebook**
   - 点击 [Academic_Homepage_Generator_Colab.ipynb](./Academic_Homepage_Generator_Colab.ipynb)
   - 或访问：https://colab.research.google.com/
   - 上传这个 notebook 文件

2. **上传项目文件**
   - 点击 Colab 左侧的文件图标
   - 创建 `/content/project` 文件夹
   - 上传整个项目到这个文件夹

3. **运行所有单元**
   - 菜单：Runtime → Run all
   - 或按 `Ctrl+F9`

4. **等待安装完成**
   - 约 2-3 分钟
   - 会自动安装 Node.js 和依赖

5. **点击生成的链接**
   - Notebook 会显示一个 ngrok 链接
   - 点击访问你的应用
   - 开始使用！

---

## 📝 详细步骤

### 步骤 1: 准备项目文件

**选项 A: 从 GitHub（如果你的项目在 GitHub）**
```python
!git clone https://github.com/your-username/your-repo.git /content/project
```

**选项 B: 手动上传**
1. 在 Colab 左侧文件浏览器
2. 创建 `/content/project` 文件夹
3. 上传所有项目文件

**选项 C: 从 Google Drive**
```python
from google.colab import drive
drive.mount('/content/drive')
!cp -r /content/drive/MyDrive/project /content/project
```

### 步骤 2: 运行 Notebook

打开 `Academic_Homepage_Generator_Colab.ipynb`，执行所有单元。

Notebook 会自动：
1. 安装 Node.js 20.x LTS
2. 安装项目依赖
3. 构建 Next.js 应用
4. 启动服务器
5. 创建公网访问链接（使用 ngrok）

### 步骤 3: 访问应用

运行完成后，会显示类似：
```
🎉 应用已启动！
🌐 访问链接: https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

点击链接即可访问！

---

## 🔑 获取 API Key

### Gemini（推荐-免费）

1. 访问：https://aistudio.google.com/app/apikey
2. 登录 Google 账号
3. 点击「Create API Key」
4. 复制密钥（格式：`AIzaSy...`）

### OpenAI

1. 访问：https://platform.openai.com/api-keys
2. 创建账号并添加付款方式
3. 创建新 API Key
4. 复制密钥（格式：`sk-proj-...`）

---

## ⚠️ 重要注意事项

### 会话限制

- Colab 免费版有**运行时限制**：
  - 空闲 90 分钟后断开
  - 连续运行最多 12 小时
- 断开后需要重新运行所有单元

### 数据持久化

- Colab 环境是**临时的**
- 会话结束后数据会丢失
- 建议：
  - 保存生成的结果到 Google Drive
  - 或下载到本地

### 网络访问

- ngrok 免费版的链接是**临时的**
- 每次运行会生成新链接
- 如需固定链接，考虑：
  - ngrok 付费版
  - 或部署到 Vercel/Netlify

---

## 💡 优化建议

### 1. 使用 Google Drive 持久化

```python
# 在 notebook 中添加
from google.colab import drive
drive.mount('/content/drive')

# 保存生成的网站到 Drive
!cp -r /content/project/.next /content/drive/MyDrive/
```

### 2. 使用 ngrok Authtoken

注册 ngrok 账号（免费）：
1. 访问：https://dashboard.ngrok.com/get-started/your-authtoken
2. 获取 authtoken
3. 在 notebook 中添加：
```python
ngrok.set_auth_token("your_token_here")
```

好处：
- 更长的会话时间
- 更稳定的连接
- 更多功能

### 3. 加速依赖安装

在 notebook 中使用国内镜像：
```bash
npm config set registry https://registry.npmmirror.com
```

---

## 🔧 故障排查

### Q: "npm: command not found"

**原因**：Node.js 安装失败  
**解决**：重新运行安装 Node.js 的单元

### Q: 链接打不开

**可能原因**：
1. 服务器还没启动完成 → 多等待几秒
2. ngrok 连接失败 → 重新运行创建链接的单元
3. Colab 会话断开 → 重新运行所有单元

### Q: 依赖安装很慢

**解决**：
1. 使用国内镜像（见优化建议）
2. 或等待完成（首次约 3-5 分钟）

### Q: 想要固定链接

**方案 A: 使用 ngrok 付费版**
- 费用：$8/月起
- 提供固定域名

**方案 B: 部署到真正的服务器**
- Vercel（推荐） - 免费
- Railway - 免费额度
- Render - 免费额度

---

## 🌟 生产部署（推荐）

如果你需要长期稳定运行，推荐部署到专业平台：

### Vercel（最简单）

```bash
# 在本地或 Colab 运行
npm i -g vercel
vercel --prod
```

- ✅ 免费
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ 自动部署

### Railway

```bash
npm i -g @railway/cli
railway login
railway up
```

### Render

直接在网页上连接 GitHub 仓库，自动部署。

---

## 📊 性能对比

| 方案 | 成本 | 稳定性 | 速度 | 适用场景 |
|------|------|--------|------|----------|
| **Colab** | 免费 | 中等 | 快 | 临时使用、测试 |
| **Vercel** | 免费 | 高 | 极快 | 生产环境 |
| **Railway** | 免费额度 | 高 | 快 | 小型项目 |
| **本地运行** | 免费 | 高 | 快 | 开发调试 |

---

## 🎯 最佳实践

### 开发阶段
→ 使用 Colab 或本地运行

### 测试阶段
→ 使用 Colab + ngrok

### 生产阶段
→ 部署到 Vercel/Railway

### 分享他人
→ 打包成桌面软件（Windows/Linux/macOS）

---

## 📚 相关文档

- 📖 [README.md](./README.md) - 完整项目说明
- 📖 [Linux使用指南.md](./Linux使用指南.md) - Linux 部署
- 📖 [打包指南.md](./打包指南.md) - 桌面应用打包

---

**祝你使用愉快！🎉**

有问题？查看 notebook 中的常见问题部分。

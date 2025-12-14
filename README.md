# 🎓 学术主页生成器 v2.0 Pro

> AI 驱动的下一代学术主页生成工具 - 支持 Gemini 2.5 Pro 和 GPT-4o Vision

## 🎉 现已支持桌面应用！

### 四种使用方式

#### 🌐 Google Colab（零安装-推荐新手）
- **完全免费**：使用 Google 云端资源
- **零安装**：无需本地 Node.js
- **一键运行**：打开 Notebook 即用
- **详细指南**：查看 [Colab使用指南.md](./Colab使用指南.md)

#### 💻 桌面应用（推荐）
- **独立窗口**：无需浏览器，独立运行
- **一键启动**：双击 `运行桌面版.bat` / `.sh`
- **可打包分享**：生成 .exe / .AppImage 安装程序

#### 🌐 网页版
- **浏览器访问**：双击 `启动.bat` / `启动.sh`
- **传统方式**：访问 http://localhost:3000

#### 📦 独立软件
- **打包分发**：双击 `打包成软件.bat` / `.sh`
- **生成安装程序**：分享给他人使用
- **无需环境**：对方无需安装 Node.js

---

## ✨ 新增功能（v2.0）

### 🚀 多 AI 提供商支持

- **✅ Google Gemini 2.0 Flash Exp**（推荐）
  - 免费额度更多
  - 响应速度更快
  - 支持多模态理解
  - [免费获取 API Key →](https://aistudio.google.com/app/apikey)

- **✅ OpenAI GPT-4o Vision**
  - 顶级准确性
  - 更强推理能力
  - [获取 API Key →](https://platform.openai.com/api-keys)

### 🎨 软件级 UI 体验

- 精美的渐变背景和玻璃态效果
- 流畅的 Framer Motion 动画
- 直观的 AI 提供商选择卡片
- 实时处理进度显示
- 友好的错误提示

## 🚀 快速开始

### 方法 1：双击启动（推荐）

直接双击 `启动.bat` 文件即可！

脚本会自动：
1. 检测并安装依赖（首次运行）
2. 启动开发服务器

### 方法 2：手动命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

然后打开浏览器访问 **http://localhost:3000**

## 📖 使用指南

### 1. 获取 API Key

**推荐使用 Gemini（免费额度充足）：**
1. 访问 https://aistudio.google.com/app/apikey
2. 登录 Google 账号
3. 点击「Create API Key」
4. 复制生成的 Key（格式：`AIzaSy...`）

**或使用 OpenAI：**
1. 访问 https://platform.openai.com/api-keys
2. 创建新密钥（需要付费账户）
3. 复制密钥（格式：`sk-proj-...`）

### 2. 上传简历

1. 选择 AI 提供商（Gemini / OpenAI）
2. 输入 API Key
3. 上传学术简历 PDF
4. 等待 10-30 秒
5. 查看生成的精美学术主页！

### 3. 支持的简历格式

✅ 单列传统学术 CV  
✅ 双列现代设计  
✅ 创意图形简历  
✅ 多页学术简历（建议 < 10 页）  
✅ 中英文混合  

## 🎯 核心功能

### AI 自动识别

系统会自动识别以下章节：
- 📚 教育背景
- 📝 学术出版物
- 💼 工作经历
- 🔬 研究项目
- 🏆 奖项荣誉
- 📜 专利
- 🎤 演讲/报告
- 👨‍🏫 教学经历
- 🛠️ 技能认证
- ...以及任意自定义章节

### 智能布局选择

AI 会根据内容自动选择最佳布局：
- **时间线**：教育、工作经历
- **卡片网格**：出版物、项目
- **文本块**：个人简介、研究兴趣
- **图库**：海报、照片

### 响应式设计

- 📱 完美适配移动端
- 💻 优化桌面体验
- 🎨 多主题支持（Bento、Minimal、Cyber、Academic）

## 💰 成本参考

### Gemini 2.0 Flash Exp（推荐）
- **免费额度**：每分钟 15 次请求
- **成本**：完全免费（当前）
- **速度**：非常快

### GPT-4o Vision
- **成本**：约 $0.01-0.03 / 页
- **10 页简历**：约 $0.10-0.30
- **速度**：较快

## 📁 项目结构

```
d:/project/
├── app/
│   ├── actions/parseResume.ts    # 多提供商 AI 解析
│   ├── page.tsx                  # 主界面
│   ├── layout.tsx                # 布局
│   └── globals.css               # 全局样式
├── components/builder/           # 渲染组件
│   ├── PageBuilder.tsx
│   ├── SectionRenderer.tsx
│   ├── TimelineSection.tsx
│   ├── GridListSection.tsx
│   ├── TextContentSection.tsx
│   └── GallerySection.tsx
├── hooks/usePdfToImage.ts        # PDF 转换
├── lib/schema.ts                 # 数据模型
├── 启动.bat                      # 一键启动脚本
└── package.json                  # 项目配置
```

## 🔧 技术栈

- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **动画**: Framer Motion
- **AI SDK**: Vercel AI SDK
  - `@ai-sdk/google` (Gemini)
  - `@ai-sdk/openai` (GPT-4o)
- **验证**: Zod
- **PDF**: pdfjs-dist

## 🔐 隐私与安全

- ✅ API Key 仅在运行时使用，**不存储**
- ✅ PDF 在浏览器端处理，**不上传服务器**
- ✅ 生成的数据仅在本地，**不外传**
- ⚠️ 生产环境请使用 HTTPS

## 🐛 常见问题

### Q: 依赖安装失败？
使用国内镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```

### Q: API 调用失败？
检查：
1. API Key 格式是否正确
2. 网络连接是否正常
3. API 账户是否有额度

### Q: PDF 解析不准确？
建议：
1. 确保 PDF 文本清晰可读
2. 避免纯图片扫描版
3. 尝试切换不同的 AI 提供商

## 📝 更新日志

### v2.0 (2025-12-14)
- ✨ 新增 Gemini 2.5 Pro 支持
- 🎨 全新软件级 UI 设计
- 🚀 优化处理流程和状态显示
- 📦 添加一键启动脚本

### v1.0 (2025-12-14)
- 🎉 首次发布
- 🤖 GPT-4o Vision 解析
- 📊 动态章节渲染
- 🎭 Framer Motion 动画

## 🤝 支持

如有问题，欢迎反馈！

---

**Made with ❤️ for Researchers**  
*Powered by Gemini 2.0 / GPT-4o Vision*

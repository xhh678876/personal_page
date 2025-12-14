# 🎓 學術主頁生成器

> AI 驅動的下一代學術主頁生成工具 - 支持 Gemini 2.5 Pro 和 GPT-4o Vision

[![v2 多模板版](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xhh678876/personal_page/blob/main/Homepage_Generator_v2_Colab.ipynb) **← 推薦！4種模板可選**

[![高級版](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xhh678876/personal_page/blob/main/Advanced_Homepage_Generator_Colab.ipynb)
[![簡化版](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xhh678876/personal_page/blob/main/Gradio_Academic_Homepage_Generator.ipynb)

---

## 🚀 快速開始

### 🎨 高級版（推薦 - 最炫酷）

**✨ 新！** 支持中英文切換、炫酷動畫、點擊特效、GitHub Pages 即用！

1. 點擊上方的「高級版」Colab 徽章
2. Runtime → Run all（僅需 30 秒安裝）
3. 點擊生成的公網鏈接
4. 在 Gradio 界面操作：
   - 選擇 AI 提供商（推薦 Gemini）
   - 輸入 API Key
   - 上傳 PDF
   - **查看 3 個標籤**：
     - 🎨 實時預覽
     - 📦 下載 GitHub Pages 項目 ZIP
     - 📋 查看 JSON 數據

**特性**：
- ✅ 中英文一鍵切換
- ✅ 粒子背景動畫
- ✅ 波紋點擊特效
- ✅ 打字機效果
- ✅ GitHub Pages 即用

### 📱 Gradio 簡化版（最簡單）

如果只需要基本功能：

1. 點擊「Gradio」徽章
2. Runtime → Run all
3. 上傳 PDF → 下載 HTML

### 🖥️ Next.js 版本（完整體驗）

如果你想要完整的 Next.js 應用體驗：

1. 打開 [Academic_Homepage_Generator_Colab.ipynb](./Academic_Homepage_Generator_Colab.ipynb)
2. Runtime → Run all（需要 2-3 分鐘）
3. 點擊 ngrok 鏈接訪問

✨ **所有版本都完全免費，零安裝！**

---

## ✨ 功能特性

### 🤖 雙 AI 提供商支持

- **Gemini 2.5 Pro**（推薦）
  - 完全免費
  - 每分鐘 15 次請求
  - 響應速度快（10-20秒）
  - [獲取 API Key →](https://aistudio.google.com/app/apikey)

- **GPT-4o Vision**
  - 頂級準確性
  - 約 $0.01-0.03/頁
  - [獲取 API Key →](https://platform.openai.com/api-keys)

### 🎨 炫酷界面

- 深色漸變背景 + 玻璃態效果
- Framer Motion 流暢動畫
- 實時處理進度顯示
- 完全響應式設計

### 📊 智能解析

- 支持任意 PDF 格式簡歷
- 自動識別章節類型
- 提取結構化數據
- 智能分類（教育/出版物/項目等）

### 🎭 動態渲染

- 4 種布局類型：Timeline / Grid / Text / Gallery
- 自動選擇最佳布局
- 多主題支持

---

## 💻 本地運行

### Gradio 版本（最簡單）

```bash
# 安裝依賴
pip install -r requirements_gradio.txt

# 運行
python gradio_app.py

# 瀏覽器自動打開，或訪問顯示的鏈接
```

**需要**: Python 3.8+

### Next.js 版本（完整功能）

**Windows**:
```bash
# 網頁版
雙擊 啟動.bat

# 桌面應用
雙擊 運行桌面版.bat

# 打包軟件
雙擊 打包成軟件.bat
```

**Linux/macOS**:
```bash
# 添加執行權限
chmod +x *.sh

# 網頁版
./啟動.sh

# 桌面應用
./運行桌面版.sh

# 打包軟件
./打包成軟件.sh
```

**需要**: Node.js 18+

---

## 📦 打包分發

### Windows
生成 `.exe` 安裝程序

### Linux
生成多種格式：
- `.AppImage` - 通用格式
- `.deb` - Ubuntu/Debian
- `.rpm` - Fedora/RedHat

---

## 🌐 生產部署

### Vercel（推薦-免費）

```bash
npm i -g vercel
vercel --prod
```

一鍵部署，獲得永久域名。

---

## 📚 項目結構

```
personal_page/
├──app/actions/ parseResume.ts          # Vision AI 解析
├── components/builder/                  # 動態渲染器
│   ├── PageBuilder.tsx                 # 主頁構建器
│   ├── TimelineSection.tsx             # 時間線布局
│   ├── GridListSection.tsx             # 網格布局
│   ├── TextContentSection.tsx          # 文本布局
│   └── GallerySection.tsx              # 畫廊布局
├── hooks/usePdfToImage.ts              # PDF 轉圖片
├── lib/schema.ts                        # 數據模型
├── Academic_Homepage_Generator_Colab.ipynb  # Colab Notebook
├── 啟動.bat / 啟動.sh                   # 啟動腳本
└── README.md                            # 本文件
```

---

## 🎯 使用流程

1. **選擇 AI 提供商**（Gemini / OpenAI）
2. **輸入 API Key**
3. **上傳簡歷 PDF**
4. **等待 AI 解析**（10-30秒）
5. **查看生成的精美主頁**！

---

## 📖 詳細文檔

- 📘 [Colab使用指南.md](./Colab使用指南.md) - Colab 詳細教程
- 📘 [安裝運行指南.md](./安裝運行指南.md) - Windows 指南
- 📘 [Linux使用指南.md](./Linux使用指南.md) - Linux 指南
- 📘 [打包指南.md](./打包指南.md) - 軟件打包教程
- 📘 [GitHub上傳指南.md](./GitHub上傳指南.md) - GitHub 操作指南

---

## 🔧 技術棧

- **框架**: Next.js 14 (App Router)
- **語言**: TypeScript
- **樣式**: Tailwind CSS
- **動畫**: Framer Motion
- **AI SDK**: Vercel AI SDK
  - `@ai-sdk/google` (Gemini)
  - `@ai-sdk/openai` (GPT-4o)
- **驗證**: Zod
- **PDF**: pdfjs-dist
- **桌面**: Electron

---

## 📊 部署對比

| 方案 | 成本 | 安裝難度 | 適用場景 |
|------|------|---------|---------|
| Google Colab | 🆓 | ⭐ 極簡 | 臨時使用、測試 |
| 本地網頁 | 🆓 | ⭐⭐ 簡單 | 開發、調試 |
| 桌面應用 | 🆓 | ⭐⭐ 簡單 | 日常使用 |
| 獨立軟件 | 🆓 | ⭐⭐⭐ 中等 | 分享他人 |
| Vercel | 🆓 | ⭐⭐ 簡單 | 生產環境 |

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License

---

**Made with ❤️ for Researchers**  
*Powered by Gemini 2.0 / GPT-4o Vision*

# 📤 上傳到 GitHub 指南

## 🎯 目標

將專案上傳到 `https://github.com/xhh678876/personal_page.git`，方便 Colab 直接克隆使用。

---

## 🚀 快速上傳步驟

### 方法 1：使用 Git 命令行（推薦）

```bash
# 1. 初始化 Git 倉庫
cd d:\project
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "feat: 初始提交 - AI 學術主頁生成器"

# 4. 添加遠程倉庫
git remote add origin https://github.com/xhh678876/personal_page.git

# 5. 推送到 GitHub
git branch -M main
git push -u origin main
```

---

### 方法 2：使用 GitHub Desktop（簡單）

1. **下載 GitHub Desktop**
   - 訪問：https://desktop.github.com/
   - 安裝後登錄你的 GitHub 賬號

2. **添加倉庫**
   - File → Add Local Repository
   - 選擇 `d:\project` 文件夾
   - 點擊 "Create a repository"

3. **提交更改**
   - 左下角輸入提交信息：`初始提交`
   - 點擊 "Commit to main"

4. **推送到 GitHub**
   - 點擊 "Publish repository"
   - Repository name: `personal_page`
   - 取消勾選 "Keep this code private"（如果想公開）
   - 點擊 "Publish repository"

---

### 方法 3：使用 VS Code（如果你在用）

1. **打開項目**
   - 在 VS Code 打開 `d:\project`

2. **初始化 Git**
   - 點擊左側源代碼管理圖標
   - 點擊 "Initialize Repository"

3. **提交更改**
   - 輸入提交信息
   - 點擊 ✓ 提交

4. **推送**
   - 點擊 "Publish Branch"
   - 選擇 GitHub
   - 輸入倉庫名稱：`personal_page`

---

## ⚠️ 上傳前檢查

### 1. 清理敏感信息

確保 `.gitignore` 已配置好：
```
node_modules/
.next/
.env*.local
dist/
```

### 2. 檢查文件大小

```bash
# 查找大文件
find . -type f -size +10M
```

如果有大文件，考慮：
- 添加到 `.gitignore`
- 或使用 Git LFS

### 3. 測試構建

上傳前確保項目可以正常構建：
```bash
npm install
npm run build
```

---

## 📋 完整 Git 工作流

```bash
# 首次設置
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 初始化
cd d:\project
git init

# 添加 .gitignore
echo "node_modules/" >> .gitignore
echo ".next/" >> .gitignore
echo "dist/" >> .gitignore
echo ".env*.local" >> .gitignore

# 提交
git add .
git commit -m "feat: 初始提交 - AI 學術主頁生成器

功能：
- Gemini 2.5 Pro 和 GPT-4o Vision 支持
- 動態 Schema 系統
- 4 種渲染布局
- Windows/Linux/macOS 跨平臺支持
- Electron 桌面應用
- Google Colab 集成"

# 連接 GitHub
git remote add origin https://github.com/xhh678876/personal_page.git

# 推送
git branch -M main
git push -u origin main
```

---

## 🔧 常見問題

### Q: 推送時提示需要身份驗證？

**解決方案 A：使用 Personal Access Token**
1. 訪問：https://github.com/settings/tokens
2. Generate new token (classic)
3. 勾選 `repo` 權限
4. 生成並複製 token
5. 推送時使用 token 作為密碼

**解決方案 B：使用 SSH**
```bash
# 生成 SSH 密鑰
ssh-keygen -t ed25519 -C "your.email@example.com"

# 添加到 ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 複製公鑰並添加到 GitHub
cat ~/.ssh/id_ed25519.pub
# 訪問 https://github.com/settings/keys 添加

# 修改遠程倉庫為 SSH
git remote set-url origin git@github.com:xhh678876/personal_page.git
```

### Q: 倉庫已存在怎麼辦？

如果倉庫已經有內容：
```bash
# 先拉取
git pull origin main --allow-unrelated-histories

# 解決衝突後推送
git push origin main
```

### Q: 想要強制覆蓋遠程倉庫？

```bash
git push -f origin main
```
⚠️ 注意：這會刪除遠程的所有歷史記錄！

---

## ✅ 驗證上傳

上傳成功後：

1. 訪問：https://github.com/xhh678876/personal_page
2. 檢查文件是否都在
3. 測試 Colab 克隆：
```bash
git clone https://github.com/xhh678876/personal_page.git
```

---

## 📝 後續維護

### 更新代碼

```bash
# 修改代碼後
git add .
git commit -m "描述你的更改"
git push
```

### 查看狀態

```bash
git status          # 查看更改
git log             # 查看歷史
git diff            # 查看差異
```

---

## 🌟 推薦的 README.md

上傳後，GitHub 會自動顯示 README.md。建議包含：

- ✅ 項目介紹
- ✅ Colab 一鍵運行鏈接
- ✅ 本地安裝指南
- ✅ 功能特性
- ✅ 截圖演示

---

**上傳完成後，Colab notebook 就可以直接從 GitHub 克隆了！** 🎉

# 🐧 Linux 使用指南

## 快速开始

### 方法 1：网页版

```bash
chmod +x 启动.sh
./启动.sh
```

然后浏览器访问 http://localhost:3000

### 方法 2：桌面版

```bash
chmod +x 运行桌面版.sh
./运行桌面版.sh
```

独立窗口打开

### 方法 3：打包分发

```bash
chmod +x 打包成软件.sh
./打包成软件.sh
```

生成多种格式：
- `*.AppImage` - 通用格式（推荐）
- `*.deb` - Debian/Ubuntu
- `*.rpm` - Fedora/RedHat

---

## 安装 Node.js

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install nodejs npm
```

### Fedora
```bash
sudo dnf install nodejs npm
```

### Arch Linux
```bash
sudo pacman -S nodejs npm
```

### 使用 nvm（推荐）
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
```

---

## 打包输出说明

### AppImage（推荐）
- **优点**：无需安装，通用
- **使用**：
  ```bash
  chmod +x 学术主页生成器-*.AppImage
  ./学术主页生成器-*.AppImage
  ```

### DEB 包
- **适用**：Ubuntu、Debian、Linux Mint
- **安装**：
  ```bash
  sudo dpkg -i 学术主页生成器-*.deb
  ```

### RPM 包
- **适用**：Fedora、RHEL、CentOS
- **安装**：
  ```bash
  sudo rpm -i 学术主页生成器-*.rpm
  ```

---

## 常见问题

### Q: 提示权限不足？
```bash
chmod +x *.sh
```

### Q: 端口 3000 被占用？
修改脚本中的端口号，或：
```bash
npm run dev -- -p 3001
```

### Q: Electron 打不开？
安装依赖：
```bash
# Ubuntu/Debian
sudo apt install libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils libatspi2.0-0 libdrm2 libgbm1

# Fedora
sudo dnf install gtk3 libnotify nss libXScrnSaver libXtst xdg-utils at-spi2-atk libdrm mesa-libgbm
```

---

## 跨平台打包

### 在 Linux 打包 Windows 版
```bash
npm run dist -- --win
```

需要安装 wine：
```bash
sudo apt install wine64
```

### 在 Linux 打包 macOS 版
需要 macOS 或使用 CI/CD（GitHub Actions）

---

**完整文档请查看 README.md**

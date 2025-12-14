const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let nextServer;

// 启动 Next.js 服务器
function startNextServer() {
    return new Promise((resolve) => {
        console.log('正在启动 Next.js 服务器...');

        // 使用 npx next start 启动生产服务器
        nextServer = spawn('npx', ['next', 'start', '-p', '3000'], {
            cwd: app.getAppPath(),
            shell: true,
            stdio: 'pipe'
        });

        nextServer.stdout.on('data', (data) => {
            console.log(`Next.js: ${data}`);
            if (data.toString().includes('Ready') || data.toString().includes('started')) {
                resolve();
            }
        });

        nextServer.stderr.on('data', (data) => {
            console.error(`Next.js Error: ${data}`);
        });

        // 等待 3 秒确保服务器启动
        setTimeout(resolve, 3000);
    });
}

// 创建主窗口
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 1000,
        minHeight: 700,
        title: '学术主页生成器',
        icon: path.join(__dirname, '../build/icon.ico'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: true,
        },
        backgroundColor: '#0f172a',
        show: false, // 初始不显示，等加载完成
    });

    // 隐藏默认菜单栏
    Menu.setApplicationMenu(null);

    // 加载 Next.js 应用
    mainWindow.loadURL('http://localhost:3000');

    // 窗口准备好后显示
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        mainWindow.focus();
    });

    // 开发模式下打开 DevTools（可选）
    // mainWindow.webContents.openDevTools();

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// 应用启动
app.whenReady().then(async () => {
    console.log('Electron 应用启动中...');

    // 启动 Next.js 服务器
    await startNextServer();

    // 创建窗口
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// 所有窗口关闭时退出
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        // 关闭 Next.js 服务器
        if (nextServer) {
            nextServer.kill();
        }
        app.quit();
    }
});

// 应用退出前清理
app.on('before-quit', () => {
    if (nextServer) {
        console.log('关闭 Next.js 服务器...');
        nextServer.kill();
    }
});

// 处理未捕获的异常
process.on('uncaughtException', (error) => {
    console.error('未捕获的异常:', error);
});

# MCP_Start 项目文档

> Seeed Studio 智慧仓管 MCP 系统 | 基于 Python + MCP 协议 | 支持 Windows / Linux

---

## 项目概述

本项目是 Seeed Studio 智慧仓管（StoreClerk）系统的 MCP（Model Context Protocol）启动器，通过 MCP 协议远程管理仓储设备，支持浏览器控制、仓库管理 UI/API 访问、以及可选的全屏 Kiosk 模式。

**跨平台支持：** Windows / Linux（Raspberry Pi OS、reComputer 等 ARM/Linux 设备）

---

## 目录结构

```
MCP_Start/
├── main.py                    # 入口：启动 MCP 服务 + 可选 Kiosk 浏览器
├── server/
│   └── mcp_server.py         # MCP 工具函数（open_warehouse_ui/api）
├── browser_kiosk/             # 全屏浏览器启动器（--kiosk 模式）
│   ├── __init__.py
│   └── kiosk_browser.py
├── MCPConfig/
│   ├── mcp_pipe.py           # MCP WebSocket 代理（stdio ↔ WebSocket）
│   ├── mcp_config_Win.json   # MCP 服务器配置（Windows）
│   └── mcp_config_Linux.json # MCP 服务器配置（Linux）
├── globalData/
│   ├── GData.py               # 全局配置（MCP endpoint + Kiosk 配置）
│   ├── GObj.py                # 全局对象（BrowserTool）
│   └── path.py                # 路径配置
├── SysManger/
│   ├── Sys_env.py             # 环境变量/系统命令工具（跨平台）
│   ├── Sys_JsonFile.py        # JSON 文件读写
│   └── debugOut.py            # 日志系统（彩色输出 + 文件轮转）
└── tools/
    └── browser.py             # 浏览器控制工具（跨平台，支持 kiosk 全屏）
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行

```bash
python main.py
```

---

## 全局配置（globalData/GData.py）

### MCP 配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `MCP_ENDPOINT_Name` | 环境变量名 | `"MCP_ENDPOINT"` |
| `mcp_point` | WebSocket MCP 端点 URL | `wss://...` |

### Kiosk 全屏浏览器配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `KIOSK_ENABLED` | 是否启用 Kiosk 全屏模式 | `False` |
| `KIOSK_URL` | 启动时打开的页面地址 | `"http://192.168.2.181:2125"` |
| `KIOSK_BROWSER` | 使用的浏览器 | `"firefox"` |

**启用 Kiosk 模式：**
```python
# globalData/GData.py
KIOSK_ENABLED = True
KIOSK_URL = "http://192.168.2.181:2125"
KIOSK_BROWSER = "firefox"
```

---

## 硬件设备信息

### reComputer-R100x 智慧仓管

| 项目 | 信息 |
|------|------|
| 设备名称 | reComputer-R100x 智慧仓管 |
| MAC 地址 | 2C-CF-67-E8-E6-79 |
| 有线 IP | 192.168.2.177 |
| WiFi IP | 192.168.2.181 |
| 登录用户 | recomputer / 12345678 |

### 服务端口

| 服务 | 地址 | 说明 |
|------|------|------|
| 仓库管理系统 UI | `http://192.168.2.181:2125` | Web 管理界面 |
| 仓库管理系统 API | `http://192.168.2.181:2124/docs` | Swagger API 文档 |
| API 有线版本 | `http://192.168.2.177:2125` / `:2124/docs` | 有线接入 |

---

## MCP 工具函数（server/mcp_server.py）

### 仓库管理系统

| 函数 | 功能 | 默认地址 |
|------|------|---------|
| `open_warehouse_ui()` | 打开仓库管理系统 Web UI | `http://192.168.2.181:2125` |
| `open_warehouse_api()` | 打开仓库管理系统 API 文档 | `http://192.168.2.181:2124/docs` |

**参数：**
- `device_ip` - `"192.168.2.181"`（WiFi）或 `"192.168.2.177"`（有线），默认 WiFi
- `browser` - `edge`/`chrome`/`firefox`/`chromium`，默认自动选择

### 浏览器控制

| 函数 | 功能 |
|------|------|
| `open_webpage()` | 在浏览器中打开指定网页，支持 `kiosk=True` 全屏模式 |
| `list_opened_webpages()` | 列出所有已打开的网页 |
| `close_webpage()` | 关闭指定网页 |
| `close_all_webpages()` | 关闭所有已打开的网页 |
| `close_browser()` | 关闭指定浏览器的所有实例 |
| `search_web()` | 使用搜索引擎搜索内容 |

### 全屏控制

| 函数 | 功能 |
|------|------|
| `toggle_browser_fullscreen()` | 切换浏览器全屏模式 |
| `enter_fullscreen()` | 进入全屏 |
| `exit_fullscreen()` | 退出全屏 |

---

## Kiosk 全屏浏览器（browser_kiosk/）

### 功能说明

`start_kiosk_browser()` 在 `main.py` 启动时被调用。
- 若 `KIOSK_ENABLED=True`，则以 `--kiosk`（全屏）模式打开 `KIOSK_URL` 指定的页面
- 直接复用 `BrowserTool.open_webpage(kiosk=True)`，无需重复逻辑
- 支持 Windows 和 Linux 桌面环境检测

### 调用流程

```
main.py
  └── start_kiosk_browser()
        ├── GDat.KIOSK_ENABLED? → False 直接返回
        ├── GDat.KIOSK_URL
        ├── GDat.KIOSK_BROWSER
        └── GObj.browser.open_webpage(url, browser, kiosk=True)
              ├── Windows → <browser> --kiosk <url>
              └── Linux   → sudo -u <user> <browser> --kiosk <url>
```

### 浏览器 --kiosk 支持情况

| 浏览器 | Linux | Windows |
|--------|-------|---------|
| Firefox | ✅ | ✅ |
| Chrome | ✅ | ✅ |
| Edge | ❌ | ✅ |
| Chromium | ✅ | ✅ |

---

## 跨平台说明

### Windows

- 浏览器直接通过 `subprocess.Popen` 启动，无需额外配置
- 浏览器检测顺序：msedge → chrome → firefox
- Kiosk 模式直接启动，不涉及桌面会话检测

### Linux

- 依赖 `loginctl` 和 `/run/user/` 检测当前登录用户的桌面会话
- 使用 `sudo -u <user>` 以登录用户身份启动浏览器（避免 root 启动 GUI）
- 浏览器检测顺序（自动选择首个可用）：firefox / firefox-esr / chromium / chromium-browser
- 无头模式（headless，无图形桌面）下会跳过 Kiosk 浏览器启动，不影响 MCP 主程序运行

---

## 日志系统

- 日志保存路径：`.logs/`
- 文件命名：`YYYY-MM-DD-all.log` / `YYYY-MM-DD-error.log`
- 单文件最大：1MB，超出自动轮转，保留 3 个备份
- 控制台彩色输出（DEBUG/INFO/WARNING/ERROR/CRITICAL 五级）

---

## 修改记录

### 2026-03-27

**新增功能：**

1. **MCP 工具函数**（`server/mcp_server.py`）
   - `open_warehouse_ui(device_ip, browser)` - 打开仓库管理系统 Web UI
   - `open_warehouse_api(device_ip, browser)` - 打开仓库管理系统 API 文档

2. **Kiosk 全屏浏览器**（`browser_kiosk/`）
   - 新增文件夹，包含 `kiosk_browser.py`
   - 新增配置项：`KIOSK_ENABLED`、`KIOSK_URL`、`KIOSK_BROWSER`
   - 直接复用 `BrowserTool.open_webpage(kiosk=True)`

3. **BrowserTool 增强**（`tools/browser.py`）
   - `open_webpage()` 新增 `kiosk` 参数
   - `_open_on_linux()` / `_open_on_windows()` / `_open_on_macos()` 均支持 `kiosk` 参数
   - 新增 `_detect_desktop_env_for_kiosk()` 方法处理 Linux 桌面会话

4. **main.py 更新**
   - 启动时打印 Kiosk 配置信息
   - 调用 `start_kiosk_browser()` 启动可选全屏浏览器

**修复问题：**

- **tools/browser.py — Linux Kiosk 参数缺失**
  - 问题：`_open_on_linux()` 未添加 `kiosk` 参数，导致 `takes 4 positional arguments but 5 were given`
  - 修复：三个 `_open_on_*` 方法均添加 `kiosk: bool = False` 参数
  - Pi 端已通过 SSH 同步修复

- **kiosk_browser.py**
  - `import pwd` 移至 `_detect_desktop_env_for_kiosk()` 函数内部，解决 Windows `ModuleNotFoundError`

- **mcp_server.py — WebSocket 1009 错误**
  - 问题：工具 docstring 过长（单个最长 ~5938 字符），超出 WebSocket 缓冲区
  - 修复：`@mcp.tool(description="简短描述")` 显式指定短描述

- **requirements.txt**
  - 补充缺失依赖：`colorlog`, `websockets`, `python-dotenv`

---

## 注意事项

1. **WiFi vs 有线**：默认使用 WiFi IP `192.168.2.181`，有线接入请使用 `192.168.2.177`
2. **Kiosk 模式**：需要桌面环境支持，Linux 无头模式下会跳过
3. **sudo 权限**：Linux 上启动 Kiosk 浏览器需要 sudo 权限

# MCP_Start 项目文档

> Seeed Studio 智慧仓管 MCP 系统 | 基于 Python + MCP 协议 | 支持 Windows / Linux

---

## 项目概述

本项目是 Seeed Studio 智慧仓管（StoreClerk）系统的 MCP（Model Context Protocol）启动器，通过 MCP 协议远程管理仓储设备，支持浏览器控制、仓库管�?UI/API 访问、以及可选的全屏 Kiosk 模式�?
**跨平台支持：Windows / Linux**（Raspberry Pi OS、reComputer �?ARM/Linux 设备�?
---

## 目录结构

```
MCP_Start/
├── main.py                    # �?入口：启�?MCP 服务 + 可�?Kiosk 浏览�?├── server/
�?  └── mcp_server.py         # �?MCP 工具函数（open_warehouse_ui/api�?├── browser_kiosk/             # �?全屏浏览器启动器�?-kiosk 模式�?�?  ├── __init__.py
�?  └── kiosk_browser.py
├── MCPConfig/
�?  ├── mcp_pipe.py           # MCP WebSocket 代理（stdio �?WebSocket�?�?  ├── mcp_config_Win.json   # MCP 服务器配置（Windows�?�?  └── mcp_config_Linux.json # MCP 服务器配置（Linux�?├── globalData/
�?  ├── GData.py               # �?全局配置（MCP endpoint + Kiosk 配置�?�?  ├── GObj.py                # 全局对象（BrowserTool�?�?  └── path.py                # 路径配置
├── SysManger/
�?  ├── Sys_env.py             # 环境变量/系统命令工具（跨平台�?�?  ├── Sys_JsonFile.py        # JSON 文件读写
�?  └── debugOut.py            # 日志系统（彩色输�?+ 文件轮转�?└── tools/
    └── browser.py             # 浏览器控制工具（跨平台）
```

> **标注 �?的文�?文件夹为本次新增或频繁修改的内容�?*

---

## 快速开�?
### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 MCP Endpoint

MCP Endpoint 已配置在 `globalData/GData.py` 中的 `GDat.mcp_point`，首次运行会自动加载�?
### 3. 运行

```bash
python main.py
```

---

## 全局配置（globalData/GData.py�?
### MCP 配置

| 配置�?| 说明 | 默认�?|
|--------|------|--------|
| `MCP_ENDPOINT_Name` | 环境变量�?| `"MCP_ENDPOINT"` |
| `mcp_point` | WebSocket MCP 端点 URL | `wss://...` |

### Kiosk 全屏浏览器配�?
| 配置�?| 说明 | 默认�?|
|--------|------|--------|
| `KIOSK_ENABLED` | 是否启用 Kiosk 全屏模式 | `False` |
| `KIOSK_URL` | 启动时打开的页面地址 | `"http://192.168.2.181:2125"` |
| `KIOSK_BROWSER` | 使用的浏览器 | `"firefox"` |

**启用 Kiosk 模式�?*
```python
# globalData/GData.py
KIOSK_ENABLED = True
KIOSK_URL = "http://192.168.2.181:2125"   # 仓库管理系统 UI
KIOSK_BROWSER = "firefox"                  # Linux: firefox/chromium
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

## MCP 工具函数（server/mcp_server.py�?
### 仓库管理系统

| 函数 | 功能 | 默认地址 |
|------|------|---------|
| `open_warehouse_ui()` | 打开仓库管理系统 Web UI | `http://192.168.2.181:2125` |
| `open_warehouse_api()` | 打开仓库管理系统 API 文档 | `http://192.168.2.181:2124/docs` |

**参数�?*
- `device_ip` - `"192.168.2.181"`（WiFi）或 `"192.168.2.177"`（有线），默�?WiFi
- `browser` - `edge`/`chrome`/`firefox`/`chromium`，默认自动选择

**使用示例�?*
```
打开仓库管理系统           # �?192.168.2.181:2125
打开仓库管理API文档         # �?192.168.2.181:2124/docs
打开192.168.2.177仓库UI   # �?有线接入
用chrome打开仓库系统        # �?指定浏览�?```

### 浏览器控�?
| 函数 | 功能 |
|------|------|
| `open_webpage()` | 在浏览器中打开指定网页 |
| `list_opened_webpages()` | 列出所有已打开的网�?|
| `close_webpage()` | 关闭指定网页 |
| `close_all_webpages()` | 关闭所有已打开的网�?|
| `close_browser()` | 关闭指定浏览器的所有实�?|
| `search_web()` | 使用搜索引擎搜索内容 |
| `open_youtube()` / `open_bilibili()` | 打开视频网站 |

### 全屏控制

| 函数 | 功能 |
|------|------|
| `toggle_browser_fullscreen()` | 切换浏览器全屏模�?|
| `enter_fullscreen()` | 进入全屏 |
| `exit_fullscreen()` | 退出全�?|

---

## Kiosk 全屏浏览器（browser_kiosk/�?
### 功能说明

`start_kiosk_browser()` �?`main.py` 启动时被调用�?- �?`KIOSK_ENABLED=True`，则�?`--kiosk`（全屏）模式打开 `KIOSK_URL` 指定的页�?- 支持 Linux 桌面环境检�?+ `sudo -u` 以登录用户身份启动浏览器
- 支持 Windows 直接启动

### 调用流程

```
main.py
  └── start_kiosk_browser()       # Kiosk 启动�?        ├── GDat.KIOSK_ENABLED?   # 检查开�?        �?    ├── False �?直接返回（跳过）
        �?    └── True �?继续
        ├── GDat.KIOSK_URL        # 获取目标地址
        ├── GDat.KIOSK_BROWSER    # 获取浏览器类�?        └── platform.system()     # 判断系统
              ├── Windows �?_start_on_windows()
              └── Linux   �?_start_on_linux()
                    ├── _detect_desktop_env_linux()  # 检测桌面会�?                    └── sudo -u <user> <browser> --kiosk <url>
```

### 浏览�?--kiosk 支持情况

| 浏览�?| Linux | Windows |
|--------|--------|---------|
| Firefox | �?| �?|
| Chrome | �?| �?|
| Edge | �?| �?|
| Chromium | �?| �?|

---

## 日志系统

- 日志保存路径：`.logs/`
- 文件命名：`YYYY-MM-DD-all.log` / `YYYY-MM-DD-error.log`
- 单文件最大：1MB，超出自动轮转，保留 3 个备�?- 控制台彩色输出（DEBUG/INFO/WARNING/ERROR/CRITICAL 五级�?
```python
from SysManger.debugOut import log

log.info("信息")
log.error("错误")
```

---

## 修改记录

### 2026-03-27

**新增功能�?*

1. **MCP 工具函数**（`server/mcp_server.py`�?   - `open_warehouse_ui(device_ip, browser)` - 打开仓库管理系统 Web UI
   - `open_warehouse_api(device_ip, browser)` - 打开仓库管理系统 API 文档

2. **Kiosk 全屏浏览�?*（`browser_kiosk/`�?   - 新增文件夹，包含 `kiosk_browser.py`
   - 新增配置项：`KIOSK_ENABLED`、`KIOSK_URL`、`KIOSK_BROWSER`
   - 支持 Windows �?Linux（桌面环境检测）

3. **main.py 更新**
   - 启动时打�?Kiosk 配置信息
   - 调用 `start_kiosk_browser()` 启动可选全屏浏览器

4. **README.md**
   - 新增项目文档，每次修改同步更�?
### 2026-03-27（重构）

**重构 Kiosk 浏览器逻辑�?*

- **tools/browser.py �?BrowserTool.open_webpage()**
  - 新增 `kiosk` 参数：`open_webpage(url, browser, kiosk=False)`
  - `kiosk=True` 时自动添�?`--kiosk` 参数，支�?Windows / Linux / macOS
  - 新增 `_detect_desktop_env_for_kiosk()` 方法处理 Linux 桌面会话检�?+ sudo 用户切换
  - Linux Kiosk 模式自动以登录用户身份启动浏览器（复�?BrowserTool，不再重复逻辑�?
- **browser_kiosk/kiosk_browser.py**
  - 大幅精简：不再重复浏览器启动逻辑
  - 直接调用 `GObj.browser.open_webpage(url, browser, kiosk=True)`
  - 代码量从 ~200 行缩减至 ~70 �?
- **kiosk_browser.py**
  - `import pwd` 移至 `_detect_desktop_env_linux()` 函数内部，解�?Windows �?`ModuleNotFoundError: No module named 'pwd'` 的问�?
- **mcp_server.py �?WebSocket 1009 错误修复**
  - 问题原因：MCP 工具�?docstring 过长（单个最�?~5938 字符），JSON-RPC 响应超出 WebSocket 默认缓冲区限�?  - 修复方式：将 `@mcp.tool()` 改为 `@mcp.tool(description="简短描�?)`，显式指定短描述，覆盖冗�?docstring
  - 影响工具：`open_homeassistant`、`open_sensecraft_voice`、`open_rerouter_voice_service`、`open_warehouse_ui`、`open_warehouse_api`、`toggle_browser_fullscreen`、`enter_fullscreen`、`exit_fullscreen`
  - 工具描述统一精简�?30 字以�?
---

## 跨平台说�?
### Windows

- 浏览器直接通过 `subprocess.Popen` 启动，无需额外配置
- 浏览器检测顺序：msedge �?chrome �?firefox
- Kiosk 模式直接启动，不涉及桌面会话检�?
### Linux

- 依赖 `loginctl` �?`/run/user/` 检测当前登录用户的桌面会话
- 使用 `sudo -u <user>` 以登录用户身份启动浏览器（避�?root 启动 GUI�?- 浏览器检测顺序（自动选择首个可用）：
  - **firefox** �?firefox-esr �?firefox
  - **chromium** �?chromium-browser �?chromium
- 无头模式（headless，无图形桌面）下会跳�?Kiosk 浏览器启动，不影�?MCP 主程序运�?
## 注意事项

1. **WiFi vs 有线**：默认使�?WiFi IP `192.168.2.181`，有线接入请使用 `192.168.2.177`
2. **Kiosk 模式**：需要桌面环境支持，Linux 无头模式（headless）下会跳�?3. **浏览器权�?*：Kiosk 模式可能需要浏览器权限配置，参考各平台文档
4. **sudo 权限**：Linux 上启动浏览器需�?sudo 权限用于 `sudo -u` 切换用户

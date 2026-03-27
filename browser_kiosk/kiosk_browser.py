"""
全屏浏览器启动模块 (Kiosk Browser)

功能：
    - 启动全屏浏览器并打开指定页面（--kiosk 模式）
    - 通过全局变量 GDat.KIOSK_ENABLED 控制开关
    - 直接复用 BrowserTool.open_webpage(kiosk=True)，无需重复逻辑

使用方法：
    from browser_kiosk import start_kiosk_browser
    start_kiosk_browser()  # 在 main.py 中调用

全局配置（globalData/GData.py）：
    GDat.KIOSK_ENABLED  - True/False，启用/禁用此功能
    GDat.KIOSK_URL      - 启动时打开的页面地址
    GDat.KIOSK_BROWSER  - 浏览器类型：firefox / chrome / edge（仅 Windows）
"""

import sys
import os

# 路径：项目根目录
_CURRENT_FILE = os.path.abspath(__file__)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_CURRENT_FILE))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from globalData.GData import GDat
from globalData.GObj import GObj
from SysManger.debugOut import log


def start_kiosk_browser() -> bool:
    """
    启动全屏浏览器（Kiosk 模式）

    读取 GDat.KIOSK_ENABLED 和 GDat.KIOSK_URL 配置，
    以全屏模式（--kiosk）打开指定页面。

    直接调用 GObj.browser.open_webpage(kiosk=True)，由 BrowserTool
    处理 Windows/Linux/macOS 的差异。

    Returns:
        bool: 启动成功返回 True，未启用或失败返回 False
    """
    # 检查是否启用
    enabled = getattr(GDat, "KIOSK_ENABLED", False)
    if not enabled:
        log.debug("Kiosk 浏览器功能未启用（KIOSK_ENABLED=False），跳过")
        return False

    # 获取 URL
    url = getattr(GDat, "KIOSK_URL", None)
    if not url:
        log.warning("KIOSK_URL 未配置，跳过启动 Kiosk 浏览器")
        return False

    # 获取浏览器类型
    browser = getattr(GDat, "KIOSK_BROWSER", None)

    log.info(f"[Kiosk] 准备启动全屏浏览器: url={url}, browser={browser}")

    # 直接复用 BrowserTool，kiosk=True 开启全屏模式
    result = GObj.browser.open_webpage(url, browser=browser, kiosk=True)

    if result.get("success"):
        log.info(f"✅ Kiosk 浏览器已启动: {url}（{result.get('browser_used')}）")
    else:
        log.error(f"❌ Kiosk 浏览器启动失败: {result.get('message')}")

    return result.get("success", False)

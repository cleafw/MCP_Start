import os
import sys

current_file = os.path.abspath(__file__)
server_dir = os.path.dirname(current_file)
project_root = os.path.dirname(server_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"[mcp_server] 已添加项目根目录到路径: {project_root}", file=sys.stderr)

from mcp.server.fastmcp import FastMCP
from globalData.GData import GStr
from globalData.GObj import GObj

# 创建 MCP 实例
mcp = FastMCP(GStr.mcp_server_name)

"""
MCP 工具函数集合 - 带详细注释版本
提供浏览器控制、网页管理等功能
每个函数都有清晰的中文功能说明
"""

'''浏览器控制工具'''

# 在浏览器中打开指定的网页，支持自动选择或指定浏览器类型
@mcp.tool()
def open_webpage(url: str, browser: str = None) -> dict:
    """
    在浏览器中打开网页

    支持在Firefox、Chrome、Edge、Safari等浏览器中打开指定的URL。
    如果不指定浏览器（browser=None），会自动选择系统最佳浏览器。
    自动补全URL协议（http://或https://）。

    Args:
        url (str): 要打开的网页地址
            示例: "www.bilibili.com" 或 "https://www.youtube.com"
        browser (str, optional): 浏览器类型，默认为None（自动选择系统最佳浏览器）
            可选值:
                - None: 自动选择（Windows用Edge，Linux用Firefox，macOS用Safari）
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

    Returns:
        dict: 执行结果
            {
                "success": bool,              # 是否成功打开
                "message": str,               # 执行消息
                "browser_used": str,          # 实际使用的浏览器
                "system": str,                # 操作系统
                "webpage_index": int          # 网页索引（用于后续关闭）
            }

    Examples:
        - "打开百度网页"
        - "用Chrome打开github.com"
        - "在浏览器中访问example.com"
        - "打开 www.youtube.com"
    """
    print(f"[MCP] open_webpage called: url={url}, browser={browser}")
    return GObj.browser.open_webpage(url, browser)

# 列出所有通过此工具打开的网页，显示详细信息
# @mcp.tool()
def list_opened_webpages() -> list:
    """
    列出所有已打开的网页

    显示通过此工具打开的所有网页的详细信息，包括URL、使用的浏览器、
    打开时间和索引编号。

    Returns:
        list: 已打开的网页列表
            [
                {
                    "index": int,           # 网页索引
                    "url": str,             # 网页地址
                    "browser": str,         # 使用的浏览器
                    "opened_at": str,       # 打开时间（格式：2026-01-09 21:30:00）
                    "pid": int              # 进程ID（如果可用）
                },
                ...
            ]

    Examples:
        - "查看已打开的网页"
        - "列出所有网页"
        - "显示打开了哪些网站"
    """
    print("[MCP] list_opened_webpages called")
    return GObj.browser.list_opened_webpages()

# 关闭指定的网页，可通过索引或URL指定
@mcp.tool()
def close_webpage(index: int = None, url: str = None) -> dict:
    """
    关闭指定的网页

    可以通过网页索引或URL来关闭已打开的网页。
    索引可以从 list_opened_webpages() 或 open_webpage() 的返回值中获取。

    Args:
        index (int, optional): 网页索引（从0开始）
            示例: 0, 1, 2
        url (str, optional): 网页地址（精确匹配）
            示例: "https://www.bilibili.com"

    注意：
        - index 和 url 至少需要提供一个
        - 如果两个都提供，优先使用 index

    Returns:
        dict: 执行结果
            {
                "success": bool,        # 是否成功
                "message": str,         # 执行消息
                "closed_index": int     # 关闭的网页索引
            }

    Examples:
        - "关闭第一个网页"
        - "关闭索引为0的网页"
        - "关闭bilibili网页"
        - "关闭 https://www.youtube.com"
    """
    print(f"[MCP] close_webpage called: index={index}, url={url}")
    return GObj.browser.close_webpage(index=index, url=url)

# 一键关闭所有通过此工具打开的网页
@mcp.tool()
def close_all_webpages() -> dict:
    """
    关闭所有已打开的网页

    一键关闭通过此工具打开的所有网页。

    Returns:
        dict: 执行结果
            {
                "success": bool,        # 是否成功
                "message": str,         # 执行消息
                "closed_count": int     # 关闭的网页数量
            }

    Examples:
        - "关闭所有网页"
        - "关掉全部网站"
        - "清空所有打开的网页"
    """
    print("[MCP] close_all_webpages called")
    return GObj.browser.close_all_webpages()


# 强制关闭指定浏览器的所有窗口和实例
@mcp.tool()
def close_browser(browser: str) -> dict:
    """
    关闭指定浏览器的所有实例

    强制关闭指定浏览器的所有窗口和标签页。
    这将关闭该浏览器的所有窗口，不仅限于通过此工具打开的网页。

    Args:
        browser (str): 浏览器类型
            可选值:
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

    Returns:
        dict: 执行结果
            {
                "success": bool,    # 是否成功
                "message": str      # 执行消息
            }

    警告：
        - 这会关闭指定浏览器的所有窗口和标签页
        - 包括不是通过此工具打开的窗口

    Examples:
        - "关闭Chrome浏览器"
        - "关掉Firefox"
        - "结束Edge浏览器"
    """
    print(f"[MCP] close_browser called: browser={browser}")
    return GObj.browser.close_browser(browser)

'''系统信息工具'''

# 获取当前系统信息、支持的浏览器列表和优先级
# @mcp.tool()
def get_system_info() -> dict:
    """
    获取系统和浏览器信息

    返回当前操作系统信息、支持的浏览器列表、浏览器优先级等。

    Returns:
        dict: 系统信息
            {
                "system": str,                      # 操作系统（Windows/Linux/Darwin）
                "supported_browsers": list,         # 支持的浏览器列表
                "browser_priority": list,           # 浏览器优先级顺序
                "opened_webpages_count": int        # 当前打开的网页数量
            }

    Examples:
        - "查看系统信息"
        - "支持哪些浏览器"
        - "显示浏览器优先级"
    """
    print("[MCP] get_system_info called")
    return GObj.browser.get_system_info()

# 获取当前系统支持的所有浏览器及其命令映射
# @mcp.tool()
def get_supported_browsers() -> dict:
    """
    获取支持的浏览器列表

    返回当前系统支持的所有浏览器及其命令映射。

    Returns:
        dict: 浏览器映射
            {
                "firefox": "firefox",
                "chrome": "google-chrome",
                "edge": "msedge",
                ...
            }

    Examples:
        - "查看支持的浏览器"
        - "有哪些浏览器可用"
    """
    print("[MCP] get_supported_browsers called")
    return GObj.browser.get_supported_browsers()


'''网页搜索工具'''
# 使用指定搜索引擎搜索内容（Google / Baidu）
@mcp.tool()
def search_web(query: str, engine: str = "google", browser: str = None) -> dict:
    """
    在浏览器中使用指定搜索引擎搜索内容（Google / Baidu）

    Args:
        query (str): 搜索关键词
            示例: "Python教程", "如何学习编程"
        engine (str, optional): 搜索引擎，可选 "google" 或 "baidu"，默认 "google"
        browser (str, optional): 浏览器类型，默认为None（自动选择）

    Returns:
        dict: 执行结果
            {
                "success": bool,
                "message": str,
                "search_url": str,
                "browser_used": str,
                "webpage_index": int
            }

    Examples:
        - "用google搜索Python教程"
        - "用baidu搜索人工智能"
        - "在Chrome中搜索机器学习"
    """
    print(f"[MCP] search_web called: query={query}, engine={engine}, browser={browser}")
    import urllib.parse

    engine = engine.lower()
    encoded_query = urllib.parse.quote(query)

    # 搜索引擎URL映射
    if engine == "baidu":
        search_url = f"https://www.baidu.com/s?wd={encoded_query}&ie=utf-8"
    else:  # 默认 google
        search_url = f"https://www.google.com/search?q={encoded_query}"

    # 打开搜索页面
    result = GObj.browser.open_webpage(search_url, browser)

    if result.get("success"):
        result["search_url"] = search_url
        result["query"] = query
        result["engine"] = engine

    return result


# 打开YouTube视频网站，可选择搜索特定内容
# @mcp.tool()
def open_youtube(search_query: str = None, browser: str = None) -> dict:
    """
    打开 YouTube

    可以直接打开 YouTube 首页，或搜索指定内容。

    Args:
        search_query (str, optional): 搜索关键词，为None时打开首页
        browser (str, optional): 浏览器类型

    Returns:
        dict: 执行结果

    Examples:
        - "打开YouTube"
        - "在YouTube上搜索音乐"
    """
    print(f"[MCP] open_youtube called: query={search_query}, browser={browser}")

    if search_query:
        import urllib.parse
        encoded_query = urllib.parse.quote(search_query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
    else:
        url = "https://www.youtube.com"

    return GObj.browser.open_webpage(url, browser)


# 打开Bilibili视频网站（B站），可选择搜索特定内容
@mcp.tool()
def open_bilibili(search_query: str = None, browser: str = None) -> dict:
    """
    打开 Bilibili（B站）

    可以直接打开 B站 首页，或搜索指定内容。

    Args:
        search_query (str, optional): 搜索关键词，为None时打开首页
        browser (str, optional): 浏览器类型

    Returns:
        dict: 执行结果

    Examples:
        - "打开B站"
        - "在B站搜索编程教程"
    """
    print(f"[MCP] open_bilibili called: query={search_query}, browser={browser}")

    if search_query:
        import urllib.parse
        encoded_query = urllib.parse.quote(search_query)
        url = f"https://search.bilibili.com/all?keyword={encoded_query}"
    else:
        url = "https://www.bilibili.com"

    return GObj.browser.open_webpage(url, browser)


'''批量操作工具'''

# 批量打开多个网页，可使用相同或不同浏览器
# @mcp.tool()
def open_multiple_webpages(urls: list, browser: str = None) -> dict:
    """
    批量打开多个网页

    同时打开多个网页，可以指定使用相同的浏览器或让系统自动选择。

    Args:
        urls (list): 网页地址列表
            示例: ["www.bilibili.com", "www.youtube.com", "github.com"]
        browser (str, optional): 浏览器类型，默认为None（自动选择）

    Returns:
        dict: 执行结果
            {
                "success": bool,
                "message": str,
                "opened_count": int,        # 成功打开的数量
                "failed_count": int,        # 失败的数量
                "results": list,            # 每个网页的详细结果
                "indices": list             # 所有网页的索引列表
            }

    Examples:
        - "打开bilibili、youtube和github"
        - "批量打开多个网站"
    """
    print(f"[MCP] open_multiple_webpages called: urls={urls}, browser={browser}")

    results = []
    indices = []
    success_count = 0
    failed_count = 0

    for url in urls:
        result = GObj.browser.open_webpage(url, browser)
        results.append(result)

        if result.get('success'):
            success_count += 1
            if 'webpage_index' in result:
                indices.append(result['webpage_index'])
        else:
            failed_count += 1

    return {
        "success": success_count > 0,
        "message": f"✅ 成功打开 {success_count} 个网页，失败 {failed_count} 个",
        "opened_count": success_count,
        "failed_count": failed_count,
        "results": results,
        "indices": indices
    }


'''便捷操作工具'''

# 获取当前已打开网页的总数量
@mcp.tool()
def get_webpage_count() -> dict:
    """
    获取已打开的网页数量

    返回当前通过此工具打开的网页总数。

    Returns:
        dict: 结果
            {
                "count": int,           # 网页数量
                "message": str
            }

    Examples:
        - "有多少个打开的网页"
        - "查看网页数量"
    """
    print("[MCP] get_webpage_count called")
    webpages = GObj.browser.list_opened_webpages()
    count = len(webpages)

    return {
        "count": count,
        "message": f"当前有 {count} 个已打开的网页"
    }


# 关闭最近（最后）打开的网页
@mcp.tool()
def close_latest_webpage() -> dict:
    """
    关闭最近打开的网页

    关闭最后一个打开的网页（索引最大的）。

    Returns:
        dict: 执行结果

    Examples:
        - "关闭最新的网页"
        - "关掉刚才打开的页面"
    """
    print("[MCP] close_latest_webpage called")
    webpages = GObj.browser.list_opened_webpages()

    if not webpages:
        return {
            "success": False,
            "message": "❌ 没有已打开的网页"
        }

    # 找到索引最大的网页
    latest = max(webpages, key=lambda x: x['index'])

    return GObj.browser.close_webpage(index=latest['index'])


# 关闭最早（第一个）打开的网页
@mcp.tool()
def close_oldest_webpage() -> dict:
    """
    关闭最早打开的网页

    关闭第一个打开的网页（索引最小的）。

    Returns:
        dict: 执行结果

    Examples:
        - "关闭最早的网页"
        - "关掉第一个打开的页面"
    """
    print("[MCP] close_oldest_webpage called")
    webpages = GObj.browser.list_opened_webpages()

    if not webpages:
        return {
            "success": False,
            "message": "❌ 没有已打开的网页"
        }

    # 找到索引最小的网页
    oldest = min(webpages, key=lambda x: x['index'])

    return GObj.browser.close_webpage(index=oldest['index'])


"""
工具函数功能概览：

【浏览器控制】
1. open_webpage           - 在浏览器中打开指定的网页，支持自动选择或指定浏览器类型
2. list_opened_webpages   - 列出所有通过此工具打开的网页，显示详细信息
3. close_webpage          - 关闭指定的网页，可通过索引或URL指定
4. close_all_webpages     - 一键关闭所有通过此工具打开的网页
5. close_browser          - 强制关闭指定浏览器的所有窗口和实例

【系统信息】
6. get_system_info        - 获取当前系统信息、支持的浏览器列表和优先级
7. get_supported_browsers - 获取当前系统支持的所有浏览器及其命令映射

【搜索工具】
8. search_web             - 使用Google搜索引擎搜索指定内容
9. open_youtube           - 打开YouTube视频网站，可选择搜索特定内容
10. open_github           - 打开GitHub代码托管平台，可选择搜索仓库或用户
11. open_bilibili         - 打开Bilibili视频网站（B站），可选择搜索特定内容

【批量操作】
12. open_multiple_webpages - 批量打开多个网页，可使用相同或不同浏览器

【便捷操作】
13. get_webpage_count     - 获取当前已打开网页的总数量
14. close_latest_webpage  - 关闭最近（最后）打开的网页
15. close_oldest_webpage  - 关闭最早（第一个）打开的网页

使用示例：

1. 基本操作：
   - open_webpage("www.bilibili.com")                    # 自动选择浏览器
   - open_webpage("www.youtube.com", "chrome")           # 指定Chrome
   - list_opened_webpages()                              # 查看所有网页
   - close_webpage(index=0)                              # 关闭第一个
   - close_all_webpages()                                # 关闭所有

2. 搜索功能：
   - search_web("Python教程")                            # 搜索内容
   - open_youtube("music")                               # YouTube搜索
   - open_github("python project")                       # GitHub搜索
   - open_bilibili("编程")                               # B站搜索

3. 批量操作：
   - open_multiple_webpages(["url1", "url2", "url3"])   # 批量打开
   - close_all_webpages()                                # 批量关闭

4. 系统信息：
   - get_system_info()                                   # 系统信息
   - get_supported_browsers()                            # 支持的浏览器
   - get_webpage_count()                                 # 网页数量

5. 便捷操作：
   - close_latest_webpage()                              # 关闭最新
   - close_oldest_webpage()                              # 关闭最早
"""


'''智能家居'''
# 打开 Home Assistant 智能家居控制页面
@mcp.tool(description="打开 Home Assistant 智能家居控制面板")
def open_homeassistant(browser: str = None) -> dict:
    """
    打开 Home Assistant 智能家居控制系统

    自动打开 Home Assistant 的主控制面板，用于管理和控制智能家居设备。
    首先会打开主页(http://homeassistant.local:8123/)，
    然后自动跳转到配置好的 MIOT 控制页面(http://homeassistant.local:8123/dashboard-unknown/miot)。

    Home Assistant 是一个开源的智能家居平台，支持管理灯光、开关、传感器、
    摄像头等各类智能设备。该控制面板可以实现设备状态查看、远程控制、
    自动化场景设置等功能。

    Args:
        browser (str, optional): 浏览器类型，默认为None（自动选择系统最佳浏览器）
            可选值:
                - None: 自动选择（Windows用Edge，Linux用Firefox，macOS用Safari）
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

    Returns:
        dict: 执行结果
            {
                "success": bool,              # 是否成功打开
                "message": str,               # 执行消息
                "browser_used": str,          # 实际使用的浏览器
                "system": str,                # 操作系统
                "webpage_index": int,         # 网页索引
                "url": str                    # 打开的URL地址
            }

    Examples:
        - "打开Home Assistant"
        - "打开智能家居控制面板"
        - "打开家庭助手"
        - "用Chrome打开Home Assistant控制页面"
        - "打开HA控制面板"

    Note:
        - 需要确保 Home Assistant 服务正在运行
        - 需要能够访问 http://homeassistant.local:8123
        - 如果无法通过 homeassistant.local 访问，可能需要使用IP地址
    """
    print(f"[MCP] open_homeassistant called: browser={browser}")

    # 打开配置好的MIOT控制页面
    url = "http://homeassistant.local:8123/dashboard-unknown/miot"
    result = GObj.browser.open_webpage(url, browser)

    if result.get("success"):
        result["url"] = url
        result["message"] = "✅ 成功打开 Home Assistant 智能家居控制面板"

    return result


'''语音识别系统'''
# 打开 SenseCraft Voice 语音识别系统
@mcp.tool(description="打开 SenseCraft Voice 语音识别系统云端管理平台")
def open_sensecraft_voice(browser: str = None) -> dict:
    """
    打开 SenseCraft Voice 语音识别系统（别名：语音识别管理平台、会议纪要管理平台）

    打开由 Seeed Studio 开发的 SenseCraft Voice 语音识别系统的Web管理平台。
    该系统运行在云端，使用 reRouter 设备搭配 reSpeaker XVF3800 麦克风阵列
    进行高质量的语音采集和识别。

    SenseCraft Voice 是一个专业的语音识别和对话系统，提供完整的管理功能：

    1. 【仪表盘 Dashboard】- 系统总览
       - 总记录数：显示累计语音记录数量和今日增量（例如：124,575条，今日+973）
       - 点位数量：显示已配置的门店/设备数量（例如：5个门店下所有点位）
       - 今日完成数据：显示当天数据采集完成进度（例如：23%，已完成3/13个设备）
       - 关键词触发：显示今日触发关键词次数（例如：2次）
       - 今日采集趋势图：按时间展示24小时内的语音采集量分布
       - 今日活跃设备：显示活跃话筒设备数量和设备生产记录
       - 最近记录：展示最新的语音交互记录列表
       - 关键词热度分析：统计关键词出现频率（全部/传播量/舆后/投诉）

    2. 【AI分析】- AI智能分析与录音管理
       - 与AI助手对话分析语音内容
       - 获取数据洞察和业务建议
       - 支持优化询问策略
       - 录音记录查询和管理
       - 按门店/点位/时间筛选数据
       - 实时语音对话功能

    3. 【录音管理】- 全部设备录音
       - 搜索录音（支持MAC地址搜索）
       - 按录音状态筛选（全部/已录音/未录音）
       - 查看设备列表和录音详情
       - 支持按开始日期和结束日期范围筛选
       - 导出和重置功能

    4. 【门店管理】- 店铺与设备管理
       - 门店管理：创建和管理门店信息
       - 点位管理：配置具体的设备部署位置
       - 设备管理：管理麦克风阵列等硬件设备
       - 查看门店名称、门店代码、地址、联系人信息
       - 实时监控设备状态（正常/未分配）
       - 编辑、定位、复制、删除操作

    5. 【后台配置】- 系统设置
       - 关键词配置：设置需要监控的关键词和近义词
       - 用户管理：管理系统用户权限
       - 系统维护接口：配置API和系统参数
       - 标记颜色设置：自定义关键词标记颜色

    硬件配置：
    - 主控设备：reRouter（Seeed Studio网关设备）
    - 麦克风阵列：reSpeaker XVF3800（4麦远场语音采集模组）
    - 部署方式：云端管理平台 + 本地设备采集

    Args:
        browser (str, optional): 浏览器类型，默认为None（自动选择系统最佳浏览器）
            可选值:
                - None: 自动选择（Windows用Edge，Linux用Firefox，macOS用Safari）
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

    Returns:
        dict: 执行结果
            {
                "success": bool,              # 是否成功打开
                "message": str,               # 执行消息
                "browser_used": str,          # 实际使用的浏览器
                "system": str,                # 操作系统
                "webpage_index": int,         # 网页索引
                "url": str                    # 打开的URL地址
            }

    Examples:
        - "打开SenseCraft Voice"
        - "打开语音识别系统"
        - "打开SenseCraft语音管理平台"
        - "用Firefox打开Seeed语音系统"
        - "打开录音管理系统"
        - "查看语音数据统计"
        - "打开语音识别系统仪表盘"

    Note:
        - 需要网络连接访问云端平台
        - 建议使用现代浏览器（Chrome/Firefox/Edge）以获得最佳体验
        - 首次访问可能需要登录账号
        - 部分功能可能需要管理员权限
        - 实时语音对话功能需要授权浏览器使用麦克风权限
    """
    print(f"[MCP] open_sensecraft_voice called: browser={browser}")

    # SenseCraft Voice 云端管理平台地址
    url = "https://test-voice-web.seeed.cn/"

    result = GObj.browser.open_webpage(url, browser)

    if result.get("success"):
        result["url"] = url
        result["message"] = "✅ 成功打开 SenseCraft Voice 语音识别系统"

    return result


# 打开 reRouter 本地语音识别服务
@mcp.tool(description="打开 reRouter 本地语音识别服务页面")
def open_rerouter_voice_service(device_ip: str = "192.168.2.142", browser: str = None) -> dict:
    """
    打开 reRouter 本地语音识别服务（别名：会议纪要系统）

    打开运行在 reRouter 设备上的本地语音识别服务页面。
    该服务提供实时语音采集、处理和基础的设备控制功能。

    这是与 SenseCraft Voice 云端平台配套使用的本地设备服务，
    负责实际的语音采集和初步处理，然后将数据上传到云端平台进行分析。

    本地服务功能：
    - 实时语音采集：使用 reSpeaker XVF3800 麦克风阵列采集音频
    - 设备状态监控：查看麦克风、网络等硬件状态
    - 基础配置：网络设置、音量调节等
    - 录音控制：启动/停止录音
    - 日志查看：查看本地运行日志

    硬件配置：
    - 主控设备：reRouter（网关设备）
    - 麦克风阵列：reSpeaker XVF3800（4麦远场拾音）
    - 默认网络地址：192.168.2.142（可通过参数覆盖）
    - 访问端口：8090（本地服务端口）

    Args:
        device_ip (str, optional): reRouter 设备的 IP 地址，默认为 "192.168.2.142"
            当网络环境变化导致 IP 改变时，可手动指定新的 IP 地址
            示例："192.168.1.100"、"10.0.0.50"
        browser (str, optional): 浏览器类型，默认为None（自动选择系统最佳浏览器）
            可选值:
                - None: 自动选择（Windows用Edge，Linux用Firefox，macOS用Safari）
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

    Returns:
        dict: 执行结果
            {
                "success": bool,              # 是否成功打开
                "message": str,               # 执行消息
                "browser_used": str,          # 实际使用的浏览器
                "system": str,                # 操作系统
                "webpage_index": int,         # 网页索引
                "url": str,                   # 打开的URL地址
                "device_ip": str              # 设备IP地址
            }

    Examples:
        - "打开reRouter语音服务"
        - "打开本地语音识别服务"
        - "打开192.168.2.142语音服务"
        - "用192.168.1.100打开reRouter语音服务"
        - "查看reRouter设备状态"
        - "打开麦克风控制页面"

    Note:
        - 需要确保设备在同一局域网内
        - 需要能够访问 http://{device_ip}:8090
        - 确保 reRouter 设备已启动
        - 确保 reSpeaker XVF3800 麦克风阵列已连接
        - 建议使用支持WebRTC的现代浏览器
        - 实时语音功能需要授权浏览器使用麦克风权限
    """
    print(f"[MCP] open_rerouter_voice_service called: device_ip={device_ip}, browser={browser}")

    port = "8090"
    url = f"http://{device_ip}:{port}"

    result = GObj.browser.open_webpage(url, browser)

    if result.get("success"):
        result["url"] = url
        result["device_ip"] = device_ip
        result["message"] = f"✅ 成功打开 reRouter 本地语音识别服务（{device_ip}）"

    return result

'''智慧仓管系统'''
# 打开仓库管理系统 UI
@mcp.tool(description="打开仓库管理系统 Web UI（端口 2125）")
def open_warehouse_ui(device_ip: str = "192.168.2.181", browser: str = None) -> dict:
    """
    打开仓库管理系统 Web UI（别名：智慧仓管、WMS系统）

    打开部署在 reComputer-R100x 设备上的仓库管理系统用户界面。
    该系统提供仓储业务的可视化Web管理功能。

    硬件配置：
    - 设备名称：reComputer-R100x 智慧仓管
    - MAC地址：2C-CF-67-E8-E6-79
    - 有线IP：192.168.2.177
    - WiFi IP：192.168.2.181
    - 默认登录用户：recomputer / 12345678

    功能入口：
    - UI管理界面：端口 2125
    - API接口文档：端口 2124/docs

    Args:
        device_ip (str, optional): 设备 IP 地址，默认为 "192.168.2.181"
            可选值：
                - "192.168.2.181"（WiFi接入）
                - "192.168.2.177"（有线接入）
        browser (str, optional): 浏览器类型，默认为None（自动选择系统最佳浏览器）
            可选值：
                - None: 自动选择（Windows用Edge，Linux用Firefox，macOS用Safari）
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

    Returns:
        dict: 执行结果
            {
                "success": bool,              # 是否成功打开
                "message": str,               # 执行消息
                "browser_used": str,          # 实际使用的浏览器
                "system": str,                # 操作系统
                "webpage_index": int,         # 网页索引
                "url": str,                   # 打开的URL地址
                "device_ip": str             # 设备IP地址
            }

    Examples:
        - "打开仓库管理系统"
        - "打开智慧仓管UI"
        - "打开仓储管理系统"
        - "用Chrome打开仓库管理"
        - "打开192.168.2.181仓库系统"
        - "打开192.168.2.177仓库UI"

    Note:
        - 需要确保设备在同一局域网内
        - 需要能够访问 http://{device_ip}:2125
        - 默认用户名：recomputer，密码：12345678
        - 建议使用现代浏览器（Chrome/Firefox/Edge）
    """
    print(f"[MCP] open_warehouse_ui called: device_ip={device_ip}, browser={browser}")

    port = "2125"
    url = f"http://{device_ip}:{port}"

    result = GObj.browser.open_webpage(url, browser)

    if result.get("success"):
        result["url"] = url
        result["device_ip"] = device_ip
        result["message"] = f"✅ 成功打开仓库管理系统 UI（{device_ip}:{port}）"

    return result


# 打开仓库管理系统 API 文档
# @mcp.tool(description="打开仓库管理系统 API 文档（端口 2124/docs）")
def open_warehouse_api(device_ip: str = "192.168.2.181", browser: str = None) -> dict:
    """
    打开仓库管理系统 API 接口文档（别名：WMS API）

    打开部署在 reComputer-R100x 设备上的仓库管理系统 API 接口文档页面。
    使用 Swagger UI 展示所有可用的 API 接口，支持在线调试。

    硬件配置：
    - 设备名称：reComputer-R100x 智慧仓管
    - MAC地址：2C-CF-67-E8-E6-79
    - 有线IP：192.168.2.177
    - WiFi IP：192.168.2.181

    API 文档：
    - 地址：端口 2124/docs
    - 格式：Swagger UI / OpenAPI

    Args:
        device_ip (str, optional): 设备 IP 地址，默认为 "192.168.2.181"
            可选值：
                - "192.168.2.181"（WiFi接入）
                - "192.168.2.177"（有线接入）
        browser (str, optional): 浏览器类型，默认为None（自动选择系统最佳浏览器）
            可选值：
                - None: 自动选择
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

    Returns:
        dict: 执行结果
            {
                "success": bool,              # 是否成功打开
                "message": str,               # 执行消息
                "browser_used": str,          # 实际使用的浏览器
                "system": str,                # 操作系统
                "webpage_index": int,         # 网页索引
                "url": str,                   # 打开的URL地址
                "device_ip": str             # 设备IP地址
            }

    Examples:
        - "打开仓库管理系统API文档"
        - "打开WMS API"
        - "查看仓储接口文档"
        - "打开192.168.2.181的API文档"
        - "打开192.168.2.177的API"

    Note:
        - 需要确保设备在同一局域网内
        - 需要能够访问 http://{device_ip}:2124/docs
        - API采用 OpenAPI/Swagger 规范
        - 支持在线调试 API 接口
    """
    print(f"[MCP] open_warehouse_api called: device_ip={device_ip}, browser={browser}")

    port = "2124"
    url = f"http://{device_ip}:{port}/docs"

    result = GObj.browser.open_webpage(url, browser)

    if result.get("success"):
        result["url"] = url
        result["device_ip"] = device_ip
        result["message"] = f"✅ 成功打开仓库管理系统 API 文档（{device_ip}:{port}/docs）"

    return result


'''浏览器显示控制工具
需要安装插件：
sudo apt update
sudo apt install -y xdotool
或：
sudo apt install -y wmctrl
'''


# 将浏览器窗口切换为全屏模式
@mcp.tool(description="切换浏览器全屏模式（F11），enable=True 进入全屏，False 退出全屏")
def toggle_browser_fullscreen(browser: str = None, enable: bool = True) -> dict:
    """
    切换浏览器全屏显示模式

    将指定的浏览器窗口切换为全屏模式（F11）或退出全屏模式。
    全屏模式会隐藏浏览器的标签栏、地址栏和工具栏，让网页内容占据整个屏幕。

    适用场景：
    - 演示和展示：全屏显示仪表盘、数据可视化界面
    - 专注模式：观看视频、阅读文档时减少干扰
    - 信息展示：将网页作为信息屏或监控大屏使用
    - 沉浸体验：游戏、互动应用等需要全屏的场景

    实现方式：
    - Windows/Linux: 发送 F11 按键（标准全屏快捷键）
    - macOS: 发送 Ctrl+Cmd+F（macOS全屏快捷键）

    Args:
        browser (str, optional): 浏览器类型，默认为None（对所有浏览器生效）
            可选值:
                - None: 对当前活动的浏览器窗口生效
                - "firefox": Mozilla Firefox
                - "chrome": Google Chrome
                - "chromium": Chromium 浏览器
                - "edge": Microsoft Edge（仅 Windows）
                - "safari": Safari（仅 macOS）

        enable (bool, optional): 是否启用全屏，默认为True
            - True: 进入全屏模式
            - False: 退出全屏模式
            注意: 对于大多数浏览器，F11 是切换键，所以无论 enable 值如何都会切换状态

    Returns:
        dict: 执行结果
            {
                "success": bool,              # 是否成功执行
                "message": str,               # 执行消息
                "action": str,                # 执行的动作（"enter_fullscreen" 或 "exit_fullscreen"）
                "browser": str,               # 目标浏览器
                "system": str,                # 操作系统
                "method": str                 # 使用的方法（"F11" 或 "Ctrl+Cmd+F"）
            }

    Examples:
        - "浏览器全屏"
        - "进入全屏模式"
        - "全屏显示网页"
        - "退出全屏"
        - "取消全屏模式"
        - "让Chrome全屏显示"
        - "把浏览器切换到全屏"
        - "退出浏览器全屏"

    Note:
        - F11 是切换键，连续按两次会回到原始状态
        - 某些网页可能有自己的全屏控制，与浏览器全屏不同
        - 退出全屏也可以按 ESC 键
        - macOS 上的全屏模式会创建新的工作区
        - 需要浏览器窗口处于活动状态才能生效

    提示：
        如果要确保进入全屏状态，建议先检查当前是否已经全屏，
        或者调用两次以确保状态切换正确。
    """
    print(f"[MCP] toggle_browser_fullscreen called: browser={browser}, enable={enable}")

    import platform
    import subprocess

    system = platform.system()
    action = "enter_fullscreen" if enable else "exit_fullscreen"

    try:
        if system == "Darwin":  # macOS
            # macOS 使用 Ctrl+Cmd+F 进入全屏
            # 使用 AppleScript 发送快捷键
            script = '''
            tell application "System Events"
                keystroke "f" using {control down, command down}
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True)
            method = "Ctrl+Cmd+F"

        elif system == "Linux":
            # Linux 使用 xdotool 发送 F11
            try:
                # 首先尝试获取活动窗口
                result = subprocess.run(['xdotool', 'getactivewindow'],
                                        capture_output=True, text=True, check=True)
                window_id = result.stdout.strip()

                # 发送 F11 键
                subprocess.run(['xdotool', 'key', '--window', window_id, 'F11'], check=True)
                method = "F11 (xdotool)"

            except (subprocess.CalledProcessError, FileNotFoundError):
                # 如果 xdotool 不可用，尝试使用 wmctrl
                try:
                    if enable:
                        subprocess.run(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,fullscreen'], check=True)
                    else:
                        subprocess.run(['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,fullscreen'], check=True)
                    method = "wmctrl"
                except (subprocess.CalledProcessError, FileNotFoundError):
                    return {
                        "success": False,
                        "message": "❌ Linux 系统需要安装 xdotool 或 wmctrl 工具",
                        "action": action,
                        "browser": browser,
                        "system": system,
                        "method": "none"
                    }

        elif system == "Windows":
            # Windows 使用 F11
            # 可以使用 pyautogui 或者直接通过 win32api
            try:
                import pyautogui
                pyautogui.press('f11')
                method = "F11 (pyautogui)"
            except ImportError:
                # 如果没有 pyautogui，尝试使用 win32api
                try:
                    import win32api
                    import win32con
                    # VK_F11 = 0x7A
                    win32api.keybd_event(0x7A, 0, 0, 0)  # 按下
                    win32api.keybd_event(0x7A, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放
                    method = "F11 (win32api)"
                except ImportError:
                    return {
                        "success": False,
                        "message": "❌ Windows 系统需要安装 pyautogui 或 pywin32 库",
                        "action": action,
                        "browser": browser,
                        "system": system,
                        "method": "none"
                    }
        else:
            return {
                "success": False,
                "message": f"❌ 不支持的操作系统: {system}",
                "action": action,
                "browser": browser,
                "system": system,
                "method": "none"
            }

        # 成功执行
        action_text = "进入" if enable else "退出"
        return {
            "success": True,
            "message": f"✅ 已发送{action_text}全屏指令（{method}）",
            "action": action,
            "browser": browser or "active_window",
            "system": system,
            "method": method
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"❌ 切换全屏失败: {str(e)}",
            "action": action,
            "browser": browser,
            "system": system,
            "error": str(e)
        }

# 便捷函数：进入全屏
@mcp.tool(description="将浏览器窗口设为全屏显示")
def enter_fullscreen(browser: str = None) -> dict:
    """
    进入浏览器全屏模式

    快捷函数，将浏览器窗口切换为全屏显示。
    这是 toggle_browser_fullscreen(enable=True) 的便捷版本。

    Args:
        browser (str, optional): 浏览器类型，默认为None（对当前活动窗口生效）

    Returns:
        dict: 执行结果

    Examples:
        - "进入全屏"
        - "全屏显示"
        - "浏览器全屏"
    """
    print(f"[MCP] enter_fullscreen called: browser={browser}")
    return toggle_browser_fullscreen(browser=browser, enable=True)

# 便捷函数：退出全屏
@mcp.tool(description="退出浏览器全屏模式")
def exit_fullscreen(browser: str = None) -> dict:
    """
    退出浏览器全屏模式

    快捷函数，退出浏览器的全屏显示。
    这是 toggle_browser_fullscreen(enable=False) 的便捷版本。

    Args:
        browser (str, optional): 浏览器类型，默认为None（对当前活动窗口生效）

    Returns:
        dict: 执行结果

    Examples:
        - "退出全屏"
        - "取消全屏"
        - "关闭全屏模式"
    """
    print(f"[MCP] exit_fullscreen called: browser={browser}")
    return toggle_browser_fullscreen(browser=browser, enable=False)


# ===========================
# 使用示例和说明
# ===========================

"""
新增工具函数使用示例：

1. Home Assistant 智能家居控制：
   - open_homeassistant()                                    # 自动选择浏览器打开
   - open_homeassistant("chrome")                            # 用Chrome打开

2. SenseCraft Voice 云端管理平台：
   - open_sensecraft_voice()                                 # 打开云端管理平台
   - open_sensecraft_voice("firefox")                        # 用Firefox打开

3. reRouter 本地语音服务：
   - open_rerouter_voice_service()                           # 打开本地设备服务
   - open_rerouter_voice_service("edge")                     # 用Edge打开

4. 浏览器全屏控制：
   - toggle_browser_fullscreen(enable=True)                  # 进入全屏
   - toggle_browser_fullscreen(enable=False)                 # 退出全屏
   - enter_fullscreen()                                      # 进入全屏（便捷函数）
   - exit_fullscreen()                                       # 退出全屏（便捷函数）
   - enter_fullscreen("chrome")                              # 让Chrome进入全屏

典型使用场景：

场景1：查看智能家居状态
"打开Home Assistant控制面板，我想看看家里的灯光状态"

场景2：语音系统管理
"打开SenseCraft Voice，我要查看今天的语音数据"

场景3：本地设备控制
"打开reRouter本地服务，检查麦克风状态"

场景4：全屏展示
"打开SenseCraft Voice仪表盘并全屏显示"
→ open_sensecraft_voice()
→ enter_fullscreen()

场景5：退出全屏
"退出全屏模式"
→ exit_fullscreen()

场景6：批量操作
"同时打开Home Assistant和SenseCraft Voice，并将浏览器设为全屏"
→ open_homeassistant()
→ open_sensecraft_voice()  
→ enter_fullscreen()

注意事项：
1. SenseCraft Voice 使用云端平台（https://test-voice-web.seeed.cn/）
2. reRouter 本地服务需要在同一局域网访问（192.168.2.142:8090）
3. 全屏功能依赖系统工具（Linux需要xdotool或wmctrl，Windows需要pyautogui）
4. Home Assistant 需要确保服务正常运行
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")
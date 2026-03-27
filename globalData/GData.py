

# 智能仓管
mcp_point_IWMS = ("wss://watcher-agent-api.seeed.cc/watcher/mcp/ws?token=eyJhbGciOiJFUzI1NiIsInR5cCI6Ik"
                  "pXVCJ9.eyJ1c2VySWQiOjExNDkyMiwiYWdlbnRJZCI6Njg0MzU4LCJlbmRwb2ludElkIjoiYWdlbnRfNjg0Mz"
                  "U4IiwicHVycG9zZSI6Im1jcC1lbmRwb2ludCIsImlhdCI6MTc3NDU3ODI5NSwiZXhwIjoxODA2MTM1ODk1fQ."
                  "EcQpOtO6H5yuBWLmLDmLPX8GieExE2xa-pF4DJ7LZ3CISmeqO6NY2SGXaGS_FbcKBL9FWGanPtx1ab__yQb7MQ")
URL_IWMS: str = "http://192.168.2.181:2125"     # 仓库管理系统 UI页面


# 桌面DM助手
mcp_point_DM = ("wss://api.xiaozhi.me/mcp/?token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ5MT"
                "U1NCwiYWdlbnRJZCI6MTMxODYyMSwiZW5kcG9pbnRJZCI6ImFnZW50XzEzMTg2MjEiLCJwdXJwb3NlIjoibWNwL"
                "WVuZHBvaW50IiwiaWF0IjoxNzc0NjA0Mzg3LCJleHAiOjE4MDYxNjE5ODd9.WUz-SMr2ZD-genVIY4xxXa1hjlN"
                "ls41Uj2wwbva0f5BGQce5hLUEblopRFUAKE-RAxOWWULYpL0LFtG5Fzpmpg")
URL_DM: str = "http://192.168.2.2:8123/dashboard-unknown/miot"  # HA页面



from typing import Optional

class GStr:
    mcp_server_name = "net_server"


class GDat:
    MCP_json_path = "./MCPConfig/"                  # MCP配置文件路径
    MCP_json_name_win = "mcp_config_Win.json"       # MCP配置文件名 (win)
    MCP_json_name_linux = "mcp_config_Linux.json"   # MCP配置文件名 (linux)

    python_env: Optional[str] = None

    MCP_ENDPOINT_Name = "MCP_ENDPOINT"

    mcp_point = mcp_point_DM    # MCP点

    # ========== Kiosk 全屏浏览器配置 ==========
    KIOSK_ENABLED: bool = True                    # True = 启动时打开全屏浏览器，False = 禁用
    KIOSK_URL: str = URL_DM                       # Kiosk 模式打开的页面地址
    KIOSK_BROWSER: str = "firefox"               # 使用的浏览器（Linux: firefox/chromium，Windows: edge/chrome/firefox）
import sys
from globalData.GData import GDat

print(f"=== 主进程信息 ===")
print(f"当前 Python 解释器: {sys.executable}")
print(f"GDat.python_env: {getattr(GDat, 'python_env', 'NOT SET')}")
print(f"==================\n")

from MCPConfig.mcp_pipe import start_RunMCP
from SysManger.Sys_env import set_env
from globalData.GData import GDat

if __name__ == "__main__":

    set_env(GDat.MCP_ENDPOINT_Name, GDat.mcp_point)     # 设置环境变量 MCP端点名称

    start_RunMCP()                                      # 启动MCP主程序
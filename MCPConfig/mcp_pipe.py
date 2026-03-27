#!/usr/bin/env python3
"""
MCP stdio <-> WebSocket 代理服务器
版本: 0.2.0

功能说明:
    这个程序作为一个桥接代理，将本地的 MCP (Model Context Protocol) 服务器
    通过 stdio (标准输入输出) 与远程 WebSocket 服务器连接起来。

使用方法:
    1. 设置环境变量:
       export MCP_ENDPOINT=<ws_endpoint>
       # Windows (PowerShell): $env:MCP_ENDPOINT = "<ws_endpoint>"

    2. 运行所有配置的服务器 (默认):
       python main.py

    3. 运行单个本地服务器脚本 (向后兼容):
       python main.py path/to/server.py

配置文件:
    配置文件查找顺序:
    1. 环境变量 $MCP_CONFIG 指定的路径
    2. 当前目录下的 ./mcp_config_Win.json

    配置文件示例:
    {
        "mcpServers": {
            "server1": {
                "command": "python",
                "args": ["server.py"],
                "env": {"KEY": "value"},
                "disabled": false
            },
            "server2": {
                "type": "sse",
                "url": "http://example.com/sse",
                "headers": {"Authorization": "Bearer token"}
            }
        }
    }

作者: [Your Name]
"""

import asyncio
import json
import logging
import os
import signal
import ssl
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

import websockets
from dotenv import load_dotenv

from SysManger.Sys_JsonFile import json_file_read
from SysManger.Sys_env import is_windows
from SysManger.debugOut import log
from globalData.GData import GDat

# 配置日志系统
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# log = logging.getLogger('MCP_PIPE')

"""要运行json配置的服务器，就不要配置环境变量。"""
# MCP 配置相关路径
MCP_CONFIG_NAME = GDat.MCP_json_name_win if is_windows() else GDat.MCP_json_name_linux  # MCP配置文件名
MCP_CONFIG_DIR = GDat.MCP_json_path                                       # MCP配置目录
MCP_CONFIG_FILE_PATH = os.path.join(MCP_CONFIG_DIR, MCP_CONFIG_NAME)    # MCP配置文件完整路径

# MCP环境变量名
MCP_ENDPOINT_Name = GDat.MCP_ENDPOINT_Name

# 自动加载 .env 文件中的环境变量
load_dotenv()

# WebSocket 重连配置
INITIAL_BACKOFF = 1      # 初始重连等待时间（秒）
MAX_BACKOFF = 600        # 最大重连等待时间（秒）

# SSL 上下文配置（禁用证书验证，用于测试环境）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 数据管道: WebSocket -> 进程标准输入
async def pipe_websocket_to_process(websocket: websockets.WebSocketClientProtocol, process: subprocess.Popen, target: str) -> None:
    """
    数据管道: WebSocket -> 进程标准输入

    从 WebSocket 读取消息并写入到进程的 stdin
    每条消息自动添加换行符

    Args:
        websocket: WebSocket 连接对象
        process: 子进程对象
        target: 服务器标识（用于日志）

    Raises:
        Exception: 当管道发生错误时
    """
    try:
        while True:
            # 从 WebSocket 接收消息
            message = await websocket.recv()
            log.debug(f"[{target}] << {message[:120]}...")

            # 确保消息是字符串格式
            if isinstance(message, bytes):
                message = message.decode('utf-8')

            # 写入进程 stdin（文本模式，自动添加换行符）
            process.stdin.write(message + '\n')
            process.stdin.flush()

    except Exception as e:
        log.error(f"[{target}] WebSocket -> 进程管道错误: {e}")
        raise  # 重新抛出以触发重连

    finally:
        # 关闭进程 stdin
        if not process.stdin.closed:
            process.stdin.close()

# 数据管道: 进程标准输出 -> WebSocket
async def pipe_process_to_websocket(process: subprocess.Popen, websocket: websockets.WebSocketClientProtocol, target: str) -> None:
    """
    数据管道: 进程标准输出 -> WebSocket

    从进程的 stdout 读取数据并发送到 WebSocket

    Args:
        process: 子进程对象
        websocket: WebSocket 连接对象
        target: 服务器标识（用于日志）

    Raises:
        Exception: 当管道发生错误时
    """
    try:
        while True:
            # 从进程 stdout 读取一行数据（在线程池中执行以避免阻塞）
            data = await asyncio.to_thread(process.stdout.readline)

            if '"method":"tools/list"' in data or '"result":{"tools":' in data:
                log.info(f"[{target}] 完整工具列表响应:")
                log.info(data)  # 输出完整的JSON

            # 如果没有数据，说明进程可能已结束
            if not data:
                log.info(f"[{target}] 进程已结束输出")
                break

            # 发送数据到 WebSocket
            log.debug(f"[{target}] >> {data[:120]}...")
            await websocket.send(data)

    except Exception as e:
        log.error(f"[{target}] 进程 -> WebSocket 管道错误: {e}")
        raise  # 重新抛出以触发重连

# 数据管道: 进程标准错误 -> 终端
async def pipe_process_stderr_to_terminal(process: subprocess.Popen, target: str) -> None:
    """
    数据管道: 进程标准错误 -> 终端

    从进程的 stderr 读取数据并输出到终端的标准错误流
    用于实时查看服务器进程的错误日志

    Args:
        process: 子进程对象
        target: 服务器标识（用于日志）

    Raises:
        Exception: 当管道发生错误时
    """
    try:
        while True:
            # 从进程 stderr 读取一行数据（在线程池中执行以避免阻塞）
            data = await asyncio.to_thread(process.stderr.readline)

            # 如果没有数据，说明进程可能已结束
            if not data:
                log.info(f"[{target}] 进程已结束错误输出")
                break

            # 输出到终端标准错误流
            sys.stderr.write(data)
            sys.stderr.flush()

    except Exception as e:
        log.error(f"[{target}] 进程 stderr 管道错误: {e}")
        raise  # 重新抛出以触发重连

# 构建服务器进程的启动命令和环境变量
def build_server_command(target: Optional[str] = None) -> Tuple[List[str], Dict[str, str]]:
    """
    构建服务器进程的启动命令和环境变量

    优先级:
        1. 如果 target 匹配配置文件中的服务器名: 使用配置定义
        2. 否则: 将 target 视为 Python 脚本路径 (向后兼容模式)

    Args:
        target: 服务器名称或脚本路径。如果为 None，则从 sys.argv[1] 读取

    Returns:
        Tuple[List[str], Dict[str, str]]: (命令列表, 环境变量字典)

    Raises:
        RuntimeError: 当配置错误或文件不存在时
        AssertionError: 当缺少必要参数时

    支持的服务器类型:
        - stdio: 标准输入输出模式（默认）
        - sse: Server-Sent Events 模式
        - http/streamablehttp: HTTP 流式传输模式
    """
    # 获取目标服务器名称
    if target is None:
        assert len(sys.argv) >= 2, "缺少服务器名称或脚本路径参数"
        target = sys.argv[1]

    # 加载配置文件
    config = json_file_read(full_path=MCP_CONFIG_FILE_PATH)
    servers = config.get("mcpServers", {}) if isinstance(config, dict) else {}

    # 检查是否为配置的服务器
    if target in servers:
        entry = servers[target] or {}

        # 检查服务器是否被禁用
        if entry.get("disabled"):
            raise RuntimeError(f"服务器 '{target}' 在配置中被禁用")

        # 获取传输类型（默认为 stdio）
        transport_type = (entry.get("type") or entry.get("transportType") or "stdio").lower()

        # 构建子进程环境变量（继承父进程环境变量并添加配置的环境变量）
        child_env = os.environ.copy()
        for key, value in (entry.get("env") or {}).items():
            child_env[str(key)] = str(value)

        # 处理 stdio 类型
        if transport_type == "stdio":
            command = entry.get("command")
            args = entry.get("args") or []

            if not command:
                raise RuntimeError(f"服务器 '{target}' 缺少 'command' 配置项")

            return [command, *args], child_env

        # 处理 SSE/HTTP 类型
        if transport_type in ("sse", "http", "streamablehttp"):
            url = entry.get("url")

            if not url:
                raise RuntimeError(f"服务器 '{target}' (类型 {transport_type}) 缺少 'url' 配置项")

            # 使用当前 Python 解释器运行 mcp-proxy 模块
            cmd = [sys.executable, "-m", "mcp_proxy"]

            # 添加传输类型参数
            if transport_type in ("http", "streamablehttp"):
                cmd += ["--transport", "streamablehttp"]

            # 添加 HTTP 头部（如认证信息）
            headers = entry.get("headers") or {}
            for header_key, header_value in headers.items():
                cmd += ["-H", header_key, str(header_value)]

            cmd.append(url)
            return cmd, child_env

        # 不支持的服务器类型
        raise RuntimeError(f"不支持的服务器类型: {transport_type}")

    # 回退到脚本路径模式（向后兼容）
    script_path = target
    if not os.path.exists(script_path):
        raise RuntimeError(
            f"'{target}' 既不是配置的服务器名称，也不是存在的脚本文件"
        )

    return [sys.executable, script_path], os.environ.copy()

# 连接到 WebSocket 服务器并启动数据管道
async def connect_to_server(uri: str, target: str) -> None:
    """
    连接到 WebSocket 服务器并启动数据管道

    这个函数会:
        1. 建立 WebSocket 连接
        2. 启动本地 MCP 服务器进程
        3. 创建三个异步任务进行双向数据传输:
           - WebSocket -> 进程 stdin
           - 进程 stdout -> WebSocket
           - 进程 stderr -> 终端

    Args:
        uri: WebSocket 服务器地址
        target: 服务器标识

    Raises:
        websockets.exceptions.ConnectionClosed: 当 WebSocket 连接关闭时
        Exception: 其他连接错误
    """
    process = None

    try:
        log.info(f"[{target}] 正在连接到 WebSocket 服务器...")

        # 建立 WebSocket 连接（使用自定义 SSL 上下文）
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            log.info(f"[{target}] 成功连接到 WebSocket 服务器")

            # 构建并启动服务器进程
            cmd, env = build_server_command(target)
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                text=True,
                env=env
            )
            log.info(f"[{target}] 已启动服务器进程: {' '.join(cmd)}")

            # 并行运行三个数据管道任务
            await asyncio.gather(
                pipe_websocket_to_process(websocket, process, target),
                pipe_process_to_websocket(process, websocket, target),
                pipe_process_stderr_to_terminal(process, target)
            )

    except websockets.exceptions.ConnectionClosed as e:
        log.error(f"[{target}] WebSocket 连接已关闭: {e}")
        raise  # 重新抛出异常以触发重连

    except Exception as e:
        log.error(f"[{target}] 连接错误: {e}")
        raise  # 重新抛出异常

    finally:
        # 确保子进程被正确终止
        if process is not None:
            log.info(f"[{target}] 正在终止服务器进程")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                log.warning(f"[{target}] 进程未响应终止信号，强制结束")
                process.kill()
            log.info(f"[{target}] 服务器进程已终止")

# WebSocket 连接管理
async def connect_with_retry(uri: str, target: str) -> None:
    """
    带重连机制的 WebSocket 连接函数

    使用指数退避算法进行自动重连，永不放弃连接尝试

    Args:
        uri: WebSocket 服务器地址
        target: 服务器标识（用于日志记录）

    重连策略:
        - 初始等待时间: INITIAL_BACKOFF 秒
        - 每次失败后等待时间翻倍
        - 最大等待时间: MAX_BACKOFF 秒
        - 无限重试直到连接成功
    """
    reconnect_attempt = 0
    backoff = INITIAL_BACKOFF

    while True:  # 无限重连循环
        try:
            # 非首次连接需要等待一段时间
            if reconnect_attempt > 0:
                log.info(
                    f"[{target}] 等待 {backoff}秒 后进行第 {reconnect_attempt} 次重连尝试..."
                )
                await asyncio.sleep(backoff)

            # 尝试建立连接
            await connect_to_server(uri, target)

        except Exception as e:
            reconnect_attempt += 1
            log.warning(f"[{target}] 连接断开 (尝试 {reconnect_attempt}): {e}")

            # 使用指数退避算法计算下次等待时间
            backoff = min(backoff * 2, MAX_BACKOFF)

# 信号处理
def signal_handler(sig: int, frame) -> None:
    """
    处理中断信号（如 Ctrl+C）

    当接收到 SIGINT 信号时，优雅地关闭程序

    Args:
        sig: 信号编号
        frame: 当前堆栈帧
    """
    log.info("接收到中断信号，正在关闭程序...")
    sys.exit(0)

# 创建连接 异步运行函数
async def run_connect_async() -> None:
    """
    异步主函数

    根据命令行参数决定运行模式:
        - 无参数: 运行配置文件中所有启用的服务器
        - 有参数: 运行指定的单个服务器（脚本路径模式）

    Raises:
        RuntimeError: 当配置错误或没有可用服务器时
    """
    # 获取目标服务器参数
    target_arg = sys.argv[1] if len(sys.argv) >= 2 else None

    # 从环境变量获取 WebSocket 端点
    endpoint_url = os.environ.get(MCP_ENDPOINT_Name)
    if not endpoint_url:
        log.error("请设置 MCP_ENDPOINT 环境变量")
        sys.exit(1)

    # 模式 1: 无参数 - 运行所有配置的服务器
    if not target_arg:
        config = json_file_read(full_path=MCP_CONFIG_FILE_PATH)
        servers_config = config.get("mcpServers") or {}

        # 获取所有服务器名称
        all_servers = list(servers_config.keys())

        # 筛选启用的服务器
        enabled = [
            name for name, entry in servers_config.items()
            if not (entry or {}).get("disabled")
        ]

        # 显示被跳过的服务器
        skipped = [name for name in all_servers if name not in enabled]
        if skipped:
            log.info(f"跳过已禁用的服务器: {', '.join(skipped)}")

        # 检查是否有启用的服务器
        if not enabled:
            raise RuntimeError("配置文件中没有找到启用的服务器")

        log.info(f"正在启动服务器: {', '.join(enabled)}")

        # 为每个服务器创建独立的连接任务
        tasks = [
            asyncio.create_task(connect_with_retry(endpoint_url, server_name))
            for server_name in enabled
        ]

        # 并行运行所有任务（每个任务内部有自动重连机制）
        await asyncio.gather(*tasks)

    # 模式 2: 有参数 - 运行单个服务器（仅支持脚本路径）
    else:
        if os.path.exists(target_arg):
            await connect_with_retry(endpoint_url, target_arg)
        else:
            log.error("参数必须是本地 Python 脚本路径。要运行配置的服务器，请不带参数运行。")
            sys.exit(1)

# 程序入口
def start_RunMCP():
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # 运行异步主函数
        asyncio.run(run_connect_async())

    except KeyboardInterrupt:
        log.info("程序被用户中断")

    except Exception as e:
        log.error(f"程序执行错误: {e}")
        sys.exit(1)

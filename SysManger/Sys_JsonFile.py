"""
JSON 文件读写通用函数模块
提供统一的 JSON 数据序列化和反序列化功能
"""
import json
import os
import traceback
from typing import Any, Optional, Union, Dict, List
from SysManger.debugOut import log

# 深度合并两个字典（内部辅助函数）
def _deep_merge_dict(base_dict: Dict, update_dict: Dict) -> Dict:
    """
    深度合并两个字典（内部辅助函数）

    Args:
        base_dict: 基础字典
        update_dict: 更新字典

    Returns:
        Dict: 合并后的字典
    """
    result = base_dict.copy()

    for key, value in update_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # 递归合并嵌套字典
            result[key] = _deep_merge_dict(result[key], value)
        else:
            # 直接更新值
            result[key] = value

    return result

# 检查 JSON 文件是否存在
def json_file_exists(file_path: Optional[str] = None, file_name: Optional[str] = None, full_path: Optional[str] = None) -> bool:
    """
    检查 JSON 文件是否存在

    Args:
        file_path: 文件所在目录路径
        file_name: 文件名
        full_path: 完整文件路径

    Returns:
        bool: 存在返回 True，不存在返回 False

    示例:
        >>> if json_file_exists("/data", "config.json"):
        ...     print("配置文件存在")
    """
    try:
        # 确定完整文件路径
        if full_path:
            target_path = full_path
        elif file_path and file_name:
            target_path = os.path.join(file_path, file_name)
        elif file_path:
            target_path = file_path
        else:
            return False

        return os.path.isfile(target_path)

    except Exception as e:
        log.error(f"json_file_exists() error: {e}")
        return False

# 保存对象到 JSON 文件
def json_file_save(file_path: Optional[str] = None, file_name: Optional[str] = None, file_obj: Any = None, full_path: Optional[str] = None, ensure_ascii: bool = False, indent: int = 2) -> bool:
    """
    保存对象到 JSON 文件

    使用方式1: 提供 file_path 和 file_name
        json_file_save(file_path="/path/to", file_name="config.json", file_obj=data)

    使用方式2: 提供完整路径 full_path
        json_file_save(full_path="/path/to/config.json", file_obj=data)

    Args:
        file_path: 文件所在目录路径
        file_name: 文件名（带 .json 后缀）
        file_obj: 要保存的对象（必须是可 JSON 序列化的类型）
        full_path: 完整文件路径（包含文件名），优先级高于 file_path + file_name
        ensure_ascii: 是否将非 ASCII 字符转义（False 表示保留中文等字符）
        indent: 缩进空格数，None 表示紧凑格式

    Returns:
        bool: 成功返回 True，失败返回 False

    Raises:
        ValueError: 当参数组合不正确时

    示例:
        >>> data = {"name": "张三", "age": 25}
        >>> json_file_save("/data", "user.json", data)
        True

        >>> json_file_save(full_path="/data/user.json", file_obj=data)
        True
    """
    try:
        # 参数验证
        if file_obj is None:
            raise ValueError("file_obj 参数不能为 None")

        # 确定完整文件路径
        if full_path:
            # 优先使用 full_path
            target_path = full_path
        elif file_path and file_name:
            # 组合 file_path 和 file_name
            target_path = os.path.join(file_path, file_name)
        elif file_path and not file_name:
            # 只提供了 file_path，假设它就是完整路径
            target_path = file_path
        else:
            raise ValueError("必须提供 full_path 或 (file_path + file_name) 或 file_path")

        # 确保目录存在
        directory = os.path.dirname(target_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            log.debug(f"已创建目录: {directory}")

        # 写入 JSON 文件
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(
                file_obj,
                f,
                ensure_ascii=ensure_ascii,  # 保留中文字符
                indent=indent,  # 美化格式
                sort_keys=False  # 保持原始键顺序
            )

        log.debug(f"JSON 文件已成功保存到: {target_path}")
        return True

    except (TypeError, ValueError) as e:
        log.error(f"json_file_save() 序列化错误: {e}")
        log.error(f"无法序列化的对象类型: {type(file_obj)}")
        return False

    except IOError as e:
        log.error(f"json_file_save() 文件写入错误: {e}")
        return False

    except Exception as e:
        log.error(f"json_file_save() error: {e}")
        log.error(traceback.format_exc())
        return False

# 从 JSON 文件读取对象
def json_file_read(file_path: Optional[str] = None, file_name: Optional[str] = None, full_path: Optional[str] = None, create_if_missing: bool = False, default_value: Any = None) -> Dict | List | Any:
    """
    从 JSON 文件读取对象

    使用方式1: 提供 file_path 和 file_name
        data = json_file_read(file_path="/path/to", file_name="config.json")

    使用方式2: 提供完整路径 full_path
        data = json_file_read(full_path="/path/to/config.json")

    Args:
        file_path: 文件所在目录路径
        file_name: 文件名（带 .json 后缀）
        full_path: 完整文件路径（包含文件名），优先级高于 file_path + file_name
        create_if_missing: 如果文件不存在，是否创建默认文件
        default_value: 文件不存在时的默认值（当 create_if_missing=True 时使用）

    Returns:
        Union[Dict, List, Any]: 反序列化后的 JSON 对象
        None: 读取失败或文件不存在时返回 None

    Raises:
        ValueError: 当参数组合不正确时

    示例:
        >>> data = json_file_read("/data", "user.json")
        >>> print(data)
        {"name": "张三", "age": 25}

        >>> data = json_file_read(full_path="/data/user.json")
        >>> print(data)
        {"name": "张三", "age": 25}

        >>> # 文件不存在时返回默认值
        >>> data = json_file_read(
        ...     full_path="/data/config.json",
        ...     create_if_missing=True,
        ...     default_value={"key": "value"}
        ... )
    """
    try:
        # 确定完整文件路径
        if full_path:
            # 优先使用 full_path
            target_path = full_path
        elif file_path and file_name:
            # 组合 file_path 和 file_name
            target_path = os.path.join(file_path, file_name)
        elif file_path and not file_name:
            # 只提供了 file_path，假设它就是完整路径
            target_path = file_path
        else:
            raise ValueError("必须提供 full_path 或 (file_path + file_name) 或 file_path")

        # 检查文件是否存在
        if not os.path.isfile(target_path):
            if create_if_missing:
                # 创建默认文件
                log.info(f"文件不存在，创建默认文件: {target_path}")
                if default_value is None:
                    default_value = {}  # 默认为空字典

                success = json_file_save(full_path=target_path, file_obj=default_value)
                if success:
                    return default_value
                else:
                    log.error(f"创建默认文件失败: {target_path}")
                    return None
            else:
                log.warning(f"文件不存在: {target_path}")
                return None

        # 确保目录存在（防御性编程）
        directory = os.path.dirname(target_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            log.debug(f"已创建目录: {directory}")

        # 读取 JSON 文件
        with open(target_path, 'r', encoding='utf-8') as f:
            obj = json.load(f)
            log.debug(f"JSON 文件读取成功: {target_path}")
            return obj
    except json.JSONDecodeError as e:
        log.error(f"json_file_read() JSON 解析错误: {e}")
        log.error(f"错误位置: 第 {e.lineno} 行, 第 {e.colno} 列")
        log.error(f"文件路径: {target_path}")
        return None
    except IOError as e:
        log.error(f"json_file_read() 文件读取错误: {e}")
        return None
    except Exception as e:
        log.error(f"json_file_read() error: {e}")
        log.error(traceback.format_exc())
        return None

# 更新 JSON 文件
def json_file_update(file_path: Optional[str] = None, file_name: Optional[str] = None, full_path: Optional[str] = None, update_dict: Optional[Dict] = None, merge_mode: str = "update") -> bool:
    """
    更新 JSON 文件的内容（仅支持字典类型）

    Args:
        file_path: 文件所在目录路径
        file_name: 文件名
        full_path: 完整文件路径
        update_dict: 要更新的字典数据
        merge_mode: 合并模式
            - "update": 更新已有键，保留其他键（默认）
            - "replace": 完全替换为新内容
            - "merge": 深度合并（递归合并嵌套字典）

    Returns:
        bool: 成功返回 True，失败返回 False

    示例:
        >>> # 原始文件: {"name": "张三", "age": 25}
        >>> json_file_update("/data", "user.json", {"age": 26, "city": "北京"})
        >>> # 结果: {"name": "张三", "age": 26, "city": "北京"}
    """
    try:
        if update_dict is None:
            raise ValueError("update_dict 参数不能为 None")

        # 读取现有数据
        existing_data = json_file_read(
            file_path=file_path,
            file_name=file_name,
            full_path=full_path,
            create_if_missing=True,
            default_value={}
        )

        if not isinstance(existing_data, dict):
            log.error("json_file_update() 仅支持字典类型的 JSON 文件")
            return False

        # 根据合并模式处理数据
        if merge_mode == "replace":
            # 完全替换
            new_data = update_dict
        elif merge_mode == "merge":
            # 深度合并
            new_data = _deep_merge_dict(existing_data, update_dict)
        else:  # "update"
            # 浅合并（更新）
            new_data = existing_data.copy()
            new_data.update(update_dict)

        # 保存更新后的数据
        return json_file_save(
            file_path=file_path,
            file_name=file_name,
            full_path=full_path,
            file_obj=new_data
        )

    except Exception as e:
        log.error(f"json_file_update() error: {e}")
        log.error(traceback.format_exc())
        return False
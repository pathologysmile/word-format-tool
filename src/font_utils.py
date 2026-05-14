"""字体工具模块 - 提供字体检测、分离等功能"""

import os
import platform
from typing import List, Tuple


class FontUtils:
    """字体工具类"""
    
    @staticmethod
    def check_font_installed(font_name: str) -> bool:
        """
        检查系统是否安装指定字体
        
        Args:
            font_name: 字体名称
            
        Returns:
            bool: 字体是否存在
        """
        system = platform.system()
        
        if system == "Windows":
            return FontUtils._check_windows_font(font_name)
        elif system == "Darwin":  # macOS
            return FontUtils._check_macos_font(font_name)
        else:  # Linux
            return FontUtils._check_linux_font(font_name)
    
    @staticmethod
    def _check_windows_font(font_name: str) -> bool:
        """Windows 系统字体检测"""
        font_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
        
        # 常见字体文件名映射
        font_mapping = {
            "宋体": ["simsun.ttc", "simsun.ttf"],
            "黑体": ["simhei.ttf"],
            "楷体": ["simkai.ttf"],
            "仿宋": ["simfang.ttf"],
            "微软雅黑": ["msyh.ttc", "msyh.ttf"],
            "方正小标宋简体": ["fzxbsjt.ttf"],
            "仿宋_GB2312": ["fs_gb2312.ttf"],
            "楷体_GB2312": ["kt_gb2312.ttf"],
        }
        
        possible_files = font_mapping.get(font_name, [f"{font_name}.ttf"])
        
        for filename in possible_files:
            if os.path.exists(os.path.join(font_dir, filename)):
                return True
        
        return False
    
    @staticmethod
    def _check_macos_font(font_name: str) -> bool:
        """macOS 系统字体检测"""
        font_dirs = [
            "/Library/Fonts",
            "/System/Library/Fonts",
            os.path.expanduser("~/Library/Fonts")
        ]
        
        for font_dir in font_dirs:
            if not os.path.exists(font_dir):
                continue
            for filename in os.listdir(font_dir):
                if font_name.lower() in filename.lower():
                    return True
        
        return False
    
    @staticmethod
    def _check_linux_font(font_name: str) -> bool:
        """Linux 系统字体检测"""
        try:
            import subprocess
            result = subprocess.run(
                ["fc-list", ":family"],
                capture_output=True,
                text=True
            )
            return font_name in result.stdout
        except:
            return False
    
    @staticmethod
    def get_available_chinese_fonts() -> List[str]:
        """
        获取系统可用的中文字体列表
        
        Returns:
            List[str]: 字体名称列表
        """
        common_chinese_fonts = [
            "宋体", "黑体", "楷体", "仿宋", "微软雅黑",
            "方正小标宋简体", "仿宋_GB2312", "楷体_GB2312",
            "华文细黑", "华文中宋", "华文楷体", "华文仿宋",
            "思源黑体", "思源宋体"
        ]
        
        available = []
        for font in common_chinese_fonts:
            if FontUtils.check_font_installed(font):
                available.append(font)
        
        return available
    
    @staticmethod
    def get_fallback_font(font_name: str) -> str:
        """
        获取替代字体(当原字体不存在时)
        
        Args:
            font_name: 原始字体名称
            
        Returns:
            str: 替代字体名称
        """
        fallback_map = {
            "方正小标宋简体": "黑体",
            "仿宋_GB2312": "仿宋",
            "楷体_GB2312": "楷体",
            "华文细黑": "黑体",
            "华文中宋": "宋体",
        }
        
        return fallback_map.get(font_name, "宋体")
    
    @staticmethod
    def separate_text_parts(text: str) -> List[Tuple[str, str]]:
        """
        分离文本中的中文和数字/英文部分
        
        Args:
            text: 输入文本
            
        Returns:
            List[Tuple[str, str]]: [(文本片段, 类型), ...]
            类型: 'chinese', 'number', 'english', 'other'
        """
        if not text:
            return []
        
        parts = []
        current_part = ""
        current_type = None
        
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # 中文字符
                char_type = 'chinese'
            elif char.isdigit():  # 数字
                char_type = 'number'
            elif char.isalpha() and char.isascii():  # 英文字母
                char_type = 'english'
            else:  # 其他(标点、空格等)
                char_type = 'other'
            
            if current_type is None:
                current_type = char_type
                current_part = char
            elif char_type == current_type:
                current_part += char
            else:
                parts.append((current_part, current_type))
                current_part = char
                current_type = char_type
        
        if current_part:
            parts.append((current_part, current_type))
        
        return parts

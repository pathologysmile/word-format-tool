"""字体工具模块 - 提供字体检测、分离等功能"""

import os
import platform
from typing import List, Tuple


class FontUtils:
    """字体工具类"""
    
    @staticmethod
    def is_cloud_environment() -> bool:
        """
        检测是否运行在云环境(Streamlit Cloud/Heroku等)
        
        Returns:
            bool: 是否为云环境
        """
        # Streamlit Cloud 环境变量
        if os.environ.get('STREAMLIT_CLOUD') or os.environ.get('IS_HEROKU'):
            return True
        
        # Linux 系统且没有 Windows 字体目录通常是云环境
        system = platform.system()
        if system == "Linux":
            windir = os.environ.get("WINDIR", "")
            if not windir or not os.path.exists(windir):
                return True
        
        return False
    
    @staticmethod
    def check_font_installed(font_name: str) -> bool:
        """
        检查系统是否安装指定字体
        
        Args:
            font_name: 字体名称
            
        Returns:
            bool: 字体是否存在
        """
        # 云环境直接返回 False,使用降级策略
        if FontUtils.is_cloud_environment():
            return False
        
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
    def get_system_fonts() -> List[str]:
        """
        获取系统中所有可用的字体名称（尝试扫描系统目录）
        
        Returns:
            List[str]: 字体名称列表
        """
        system = platform.system()
        fonts = set()
        
        if system == "Windows":
            font_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
            if os.path.exists(font_dir):
                for f in os.listdir(font_dir):
                    if f.lower().endswith(('.ttf', '.ttc', '.otf')):
                        # 简单提取文件名作为字体名（去除扩展名）
                        name = os.path.splitext(f)[0]
                        fonts.add(name)
        elif system == "Darwin":  # macOS
            font_dirs = ["/Library/Fonts", "/System/Library/Fonts", os.path.expanduser("~/Library/Fonts")]
            for font_dir in font_dirs:
                if os.path.exists(font_dir):
                    for f in os.listdir(font_dir):
                        if f.lower().endswith(('.ttf', '.ttc', '.otf')):
                            name = os.path.splitext(f)[0]
                            fonts.add(name)
        
        # 合并常用中文字体以确保关键字体不丢失
        common_fonts = FontUtils.get_available_chinese_fonts()
        fonts.update(common_fonts)
        
        return sorted(list(fonts))

    @staticmethod
    def get_available_chinese_fonts() -> List[str]:
        """
        获取系统可用的中文字体列表
        
        Returns:
            List[str]: 字体名称列表
        """
        # 云环境返回空列表,使用通用字体
        if FontUtils.is_cloud_environment():
            return []
        
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
            "方正小标宋简体": "SimHei",  # 黑体
            "仿宋_GB2312": "FangSong",   # 仿宋
            "楷体_GB2312": "KaiTi",      # 楷体
            "华文细黑": "SimHei",
            "华文中宋": "SimSun",
            "黑体": "SimHei",
            "宋体": "SimSun",
            "楷体": "KaiTi",
            "仿宋": "FangSong",
            "微软雅黑": "Microsoft YaHei",
        }
        
        # 云环境直接使用英文字体名
        if FontUtils.is_cloud_environment():
            return fallback_map.get(font_name, "SimSun")
        
        return fallback_map.get(font_name, "SimSun")
    
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

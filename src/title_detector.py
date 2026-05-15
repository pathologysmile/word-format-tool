"""标题识别引擎 - 智能识别文档段落层级"""

import re
from typing import List, Dict


class TitleDetector:
    """标题识别器"""
    
    # 中文序号正则模式
    PATTERNS = {
        'heading_1': r'^[一二三四五六七八九十百千]+、',  # 一、二、三、
        'heading_2': r'^[(（][一二三四五六七八九十百千]+[)）]',  # (一)、(二)
        'heading_3': r'^\d+\.\s*',  # 1. 2. 3. (允许有无空格)
        'heading_4': r'^[(（]\d+[)）]',  # (1)、(2)
    }
    
    # 样式名称映射
    STYLE_MAP = {
        'Title': 'title',
        '标题': 'title',
        'Heading 1': 'heading_1',
        '标题 1': 'heading_1',
        'Heading 2': 'heading_2',
        '标题 2': 'heading_2',
        'Heading 3': 'heading_3',
        '标题 3': 'heading_3',
        'Heading 4': 'heading_4',
        '标题 4': 'heading_4',
        'Normal': 'body',
        '正文': 'body',
    }
    
    def __init__(self, paragraphs: List[Dict]):
        """
        初始化标题识别器
        
        Args:
            paragraphs: 段落列表(来自 DocumentParser)
        """
        self.paragraphs = paragraphs
    
    def detect_by_style(self) -> List[Dict]:
        """
        基于样式识别标题层级
        
        Returns:
            List[Dict]: 带层级标注的段落列表
        """
        result = []
        
        for para in self.paragraphs:
            style_name = para.get('style', 'Normal')
            level = self.STYLE_MAP.get(style_name, 'body')
            
            # 样式识别置信度高
            confidence = 0.95 if level != 'body' else 0.90
            
            result.append({
                'index': para['index'],
                'text': para['text'],
                'level': level,
                'confidence': confidence,
                'method': 'style'
            })
        
        return result
    
    def detect_by_pattern(self) -> List[Dict]:
        """
        基于正则模式识别标题层级
        
        Returns:
            List[Dict]: 带层级标注的段落列表
        """
        result = []
        
        for para in self.paragraphs:
            text = para['text'].strip()
            level = 'body'
            matched_pattern = None
            
            # 按优先级匹配正则模式
            for level_name, pattern in self.PATTERNS.items():
                if re.match(pattern, text):
                    level = level_name
                    matched_pattern = pattern
                    break
            
            # 计算置信度
            if level != 'body':
                confidence = 0.80
            else:
                confidence = 0.90  # 正文也有较高置信度
            
            result.append({
                'index': para['index'],
                'text': text,
                'level': level,
                'confidence': confidence,
                'method': 'pattern',
                'matched_pattern': matched_pattern
            })
        
        return result
    
    def hybrid_detect(self) -> List[Dict]:
        """
        混合识别(样式优先,模式补充,首段特殊处理)
        
        Returns:
            List[Dict]: 带层级标注的段落列表
        """
        result = []
        
        for i, para in enumerate(self.paragraphs):
            style_name = para.get('style', 'Normal')
            text = para['text'].strip()
            
            # 第一层:尝试样式识别
            level = self.STYLE_MAP.get(style_name, None)
            method = 'style'
            confidence = 0.95
            
            # 特殊处理：如果第一段没有明确样式，但文本较短且非空，倾向于认为是总标题
            if i == 0 and (level is None or level == 'body') and text and len(text) < 50:
                level = 'title'
                method = 'first_line_heuristic'
                confidence = 0.85

            # 如果样式是 Normal 或未识别,使用正则模式
            if level is None or level == 'body':
                # 第二层:尝试正则模式
                pattern_level = None
                for level_name, pattern in self.PATTERNS.items():
                    if re.match(pattern, text):
                        pattern_level = level_name
                        break
                
                if pattern_level:
                    level = pattern_level
                    method = 'pattern'
                    confidence = 0.80
                else:
                    level = 'body'
                    method = 'default'
                    confidence = 0.90
            
            result.append({
                'index': para['index'],
                'text': text,
                'level': level,
                'confidence': confidence,
                'method': method
            })
        
        return result
    
    def calculate_confidence(self, method: str) -> float:
        """
        计算识别置信度
        
        Args:
            method: 识别方法 ('style', 'pattern', 'default')
            
        Returns:
            float: 置信度 (0-1)
        """
        confidence_map = {
            'style': 0.95,
            'pattern': 0.80,
            'default': 0.90
        }
        return confidence_map.get(method, 0.50)

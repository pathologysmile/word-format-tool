"""文档清理器 - 清理文档中的冗余内容"""

from typing import List, Dict


class DocumentCleaner:
    """文档清理器"""
    
    def __init__(self, paragraphs: List[Dict]):
        """
        初始化清理器
        
        Args:
            paragraphs: 段落列表(来自 DocumentParser)
        """
        self.paragraphs = [p.copy() for p in paragraphs]
        self.stats = {
            'removed_empty': 0,
            'merged_blanks': 0,
            'removed_duplicates': 0
        }
    
    def remove_empty_paragraphs(self) -> List[Dict]:
        """
        清除所有空白段落
        
        Returns:
            List[Dict]: 清理后的段落列表
        """
        original_count = len(self.paragraphs)
        self.paragraphs = [p for p in self.paragraphs if p['text'].strip() != ""]
        self.stats['removed_empty'] = original_count - len(self.paragraphs)
        return self.paragraphs
    
    def merge_consecutive_blanks(self) -> List[Dict]:
        """
        合并连续空段落(保留1个)
        
        Returns:
            List[Dict]: 清理后的段落列表
        """
        result = []
        prev_empty = False
        merged_count = 0
        
        for para in self.paragraphs:
            is_empty = para['text'].strip() == ""
            
            if is_empty:
                if not prev_empty:
                    result.append(para)
                else:
                    merged_count += 1
                prev_empty = True
            else:
                result.append(para)
                prev_empty = False
        
        self.stats['merged_blanks'] = merged_count
        self.paragraphs = result
        return self.paragraphs
    
    def remove_consecutive_duplicates(self) -> List[Dict]:
        """
        清除连续重复段落(只保留第一个)
        
        Returns:
            List[Dict]: 清理后的段落列表
        """
        result = []
        prev_text = None
        removed_count = 0
        
        for para in self.paragraphs:
            current_text = para['text'].strip()
            
            if current_text != prev_text:
                result.append(para)
                prev_text = current_text
            else:
                removed_count += 1
        
        self.stats['removed_duplicates'] = removed_count
        self.paragraphs = result
        return self.paragraphs
    
    def clean_all(self, options: Dict[str, bool] = None) -> Dict:
        """
        执行全部清理操作
        
        Args:
            options: 清理选项
                - remove_empty: 清除空白段落
                - merge_blanks: 合并连续空行
                - remove_duplicates: 清除重复段落
        
        Returns:
            Dict: 清理后的段落列表和统计信息
        """
        if options is None:
            options = {
                'remove_empty': True,
                'merge_blanks': True,
                'remove_duplicates': True
            }
        
        if options.get('remove_empty', False):
            self.remove_empty_paragraphs()
        
        if options.get('merge_blanks', False):
            self.merge_consecutive_blanks()
        
        if options.get('remove_duplicates', False):
            self.remove_consecutive_duplicates()
        
        # 重新编号索引
        for i, para in enumerate(self.paragraphs):
            para['index'] = i
        
        return {
            'paragraphs': self.paragraphs,
            'stats': self.stats,
            'original_count': sum(self.stats.values()) + len(self.paragraphs),
            'cleaned_count': len(self.paragraphs)
        }

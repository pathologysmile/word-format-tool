"""测试文档清理功能"""

from src.document_cleaner import DocumentCleaner


def test_merge_consecutive_blanks():
    """测试合并连续空行"""
    paragraphs = [
        {'index': 0, 'text': '段落1', 'style': 'Normal'},
        {'index': 1, 'text': '', 'style': 'Normal'},
        {'index': 2, 'text': '', 'style': 'Normal'},
        {'index': 3, 'text': '', 'style': 'Normal'},
        {'index': 4, 'text': '段落2', 'style': 'Normal'},
    ]
    
    cleaner = DocumentCleaner(paragraphs)
    result = cleaner.merge_consecutive_blanks()
    
    assert len(result) == 3
    assert result[1]['text'] == ''
    assert cleaner.stats['merged_blanks'] == 2
    print("✅ 测试通过: 合并连续空行")


def test_remove_empty_paragraphs():
    """测试清除空白段落"""
    paragraphs = [
        {'index': 0, 'text': '段落1', 'style': 'Normal'},
        {'index': 1, 'text': '   ', 'style': 'Normal'},
        {'index': 2, 'text': '', 'style': 'Normal'},
        {'index': 3, 'text': '段落2', 'style': 'Normal'},
    ]
    
    cleaner = DocumentCleaner(paragraphs)
    result = cleaner.remove_empty_paragraphs()
    
    assert len(result) == 2
    assert cleaner.stats['removed_empty'] == 2
    print("✅ 测试通过: 清除空白段落")


def test_remove_consecutive_duplicates():
    """测试清除连续重复段落"""
    paragraphs = [
        {'index': 0, 'text': '特此报告。', 'style': 'Normal'},
        {'index': 1, 'text': '特此报告。', 'style': 'Normal'},
        {'index': 2, 'text': '特此报告。', 'style': 'Normal'},
        {'index': 3, 'text': '谢谢。', 'style': 'Normal'},
    ]
    
    cleaner = DocumentCleaner(paragraphs)
    result = cleaner.remove_consecutive_duplicates()
    
    assert len(result) == 2
    assert cleaner.stats['removed_duplicates'] == 2
    print("✅ 测试通过: 清除连续重复段落")


def test_clean_all():
    """测试完整清理流程"""
    paragraphs = [
        {'index': 0, 'text': '标题', 'style': 'Title'},
        {'index': 1, 'text': '', 'style': 'Normal'},
        {'index': 2, 'text': '', 'style': 'Normal'},
        {'index': 3, 'text': '段落1', 'style': 'Normal'},
        {'index': 4, 'text': '段落1', 'style': 'Normal'},
        {'index': 5, 'text': '', 'style': 'Normal'},
        {'index': 6, 'text': '段落2', 'style': 'Normal'},
    ]
    
    cleaner = DocumentCleaner(paragraphs)
    result = cleaner.clean_all({
        'remove_empty': True,
        'merge_blanks': True,
        'remove_duplicates': True
    })
    
    # remove_empty 会删除所有空段落(3个)
    # remove_duplicates 会删除1个重复的"段落1"
    assert result['cleaned_count'] == 3
    assert result['stats']['removed_empty'] == 3
    assert result['stats']['removed_duplicates'] == 1
    assert result['paragraphs'][0]['text'] == '标题'
    assert result['paragraphs'][1]['text'] == '段落1'
    assert result['paragraphs'][2]['text'] == '段落2'
    print("✅ 测试通过: 完整清理流程")


if __name__ == '__main__':
    test_merge_consecutive_blanks()
    test_remove_empty_paragraphs()
    test_remove_consecutive_duplicates()
    test_clean_all()
    print("\n🎉 所有测试通过！")

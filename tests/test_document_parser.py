"""文档解析器测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from document_parser import DocumentParser


def test_parse_paragraphs():
    """测试段落解析"""
    parser = DocumentParser('tests/sample_docs/sample_official.docx')
    paragraphs = parser.extract_paragraphs()
    
    print(f"解析到 {len(paragraphs)} 个段落")
    
    assert len(paragraphs) > 0
    assert 'index' in paragraphs[0]
    assert 'text' in paragraphs[0]
    assert 'style' in paragraphs[0]
    assert 'preview' in paragraphs[0]
    assert 'runs_count' in paragraphs[0]
    assert 'is_empty' in paragraphs[0]
    
    # 打印前几个段落信息
    for i, para in enumerate(paragraphs[:3]):
        print(f"段落 {i}: {para['preview']} (样式: {para['style']})")


def test_get_metadata():
    """测试元数据提取"""
    parser = DocumentParser('tests/sample_docs/sample_official.docx')
    metadata = parser.get_metadata()
    
    print(f"文档元数据: {metadata}")
    
    assert 'paragraph_count' in metadata
    assert metadata['paragraph_count'] > 0
    assert 'table_count' in metadata
    assert 'section_count' in metadata
    assert 'file_path' in metadata
    assert 'file_size_kb' in metadata


def test_get_page_setup():
    """测试页面设置提取"""
    parser = DocumentParser('tests/sample_docs/sample_official.docx')
    page_setup = parser.get_page_setup()
    
    print(f"页面设置: {page_setup}")
    
    assert 'top_margin' in page_setup
    assert 'bottom_margin' in page_setup
    assert 'left_margin' in page_setup
    assert 'right_margin' in page_setup
    assert 'page_width' in page_setup
    assert 'page_height' in page_setup


if __name__ == '__main__':
    print("运行文档解析器测试...\n")
    
    print("测试 1: 段落解析")
    test_parse_paragraphs()
    print("✅ 测试通过\n")
    
    print("测试 2: 元数据提取")
    test_get_metadata()
    print("✅ 测试通过\n")
    
    print("测试 3: 页面设置提取")
    test_get_page_setup()
    print("✅ 测试通过\n")
    
    print("所有测试通过! ✅")

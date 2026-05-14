"""标题识别引擎测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from title_detector import TitleDetector


def test_detect_by_style():
    """测试基于样式的识别"""
    paragraphs = [
        {'index': 0, 'text': '标题', 'style': 'Title'},
        {'index': 1, 'text': '一、目标', 'style': 'Heading 1'},
        {'index': 2, 'text': '正文', 'style': 'Normal'}
    ]
    
    detector = TitleDetector(paragraphs)
    result = detector.detect_by_style()
    
    print(f"样式识别结果:")
    for item in result:
        print(f"  {item['text']} -> {item['level']} (置信度: {item['confidence']})")
    
    assert result[0]['level'] == 'title'
    assert result[1]['level'] == 'heading_1'
    assert result[2]['level'] == 'body'
    assert result[0]['confidence'] == 0.95


def test_detect_by_pattern():
    """测试基于正则模式的识别"""
    paragraphs = [
        {'index': 0, 'text': '一、工作目标', 'style': 'Normal'},
        {'index': 1, 'text': '(二)具体措施', 'style': 'Normal'},
        {'index': 2, 'text': '3.实施步骤', 'style': 'Normal'},
        {'index': 3, 'text': '(4)注意事项', 'style': 'Normal'},
        {'index': 4, 'text': '这是正文内容', 'style': 'Normal'}
    ]
    
    detector = TitleDetector(paragraphs)
    result = detector.detect_by_pattern()
    
    print(f"\n正则模式识别结果:")
    for item in result:
        print(f"  {item['text']} -> {item['level']} (置信度: {item['confidence']})")
    
    assert result[0]['level'] == 'heading_1'
    assert result[1]['level'] == 'heading_2'
    assert result[2]['level'] == 'heading_3'
    assert result[3]['level'] == 'heading_4'
    assert result[4]['level'] == 'body'
    assert result[0]['confidence'] == 0.80


def test_hybrid_detect():
    """测试混合识别(样式优先+模式补充)"""
    paragraphs = [
        {'index': 0, 'text': '标题', 'style': 'Title'},
        {'index': 1, 'text': '一、目标', 'style': 'Normal'},  # 无样式,用正则
        {'index': 2, 'text': '正文', 'style': 'Normal'}
    ]
    
    detector = TitleDetector(paragraphs)
    result = detector.hybrid_detect()
    
    print(f"\n混合识别结果:")
    for item in result:
        print(f"  {item['text']} -> {item['level']} (方法: {item['method']}, 置信度: {item['confidence']})")
    
    assert result[0]['level'] == 'title'
    assert result[1]['level'] == 'heading_1'
    assert result[2]['level'] == 'body'


if __name__ == '__main__':
    print("运行标题识别引擎测试...\n")
    
    print("测试 1: 基于样式的识别")
    test_detect_by_style()
    print("✅ 测试通过\n")
    
    print("测试 2: 基于正则模式的识别")
    test_detect_by_pattern()
    print("✅ 测试通过\n")
    
    print("测试 3: 混合识别")
    test_hybrid_detect()
    print("✅ 测试通过\n")
    
    print("所有测试通过! ✅")

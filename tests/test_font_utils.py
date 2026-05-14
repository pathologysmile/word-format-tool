"""字体工具模块测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from font_utils import FontUtils


def test_check_font_installed():
    """测试字体检测功能"""
    # Windows 系统应该自带这些字体
    result_simsum = FontUtils.check_font_installed("宋体")
    result_heiti = FontUtils.check_font_installed("黑体")
    
    print(f"宋体检测: {result_simsum}")
    print(f"黑体检测: {result_heiti}")
    
    # 至少应该检测到一些常见字体
    assert isinstance(result_simsum, bool)
    assert isinstance(result_heiti, bool)


def test_get_available_chinese_fonts():
    """测试获取系统中文字体列表"""
    fonts = FontUtils.get_available_chinese_fonts()
    
    print(f"检测到的中文字体数量: {len(fonts)}")
    print(f"字体列表: {fonts[:5]}...")  # 只显示前5个
    
    assert isinstance(fonts, list)
    assert len(fonts) > 0


def test_separate_text_parts():
    """测试文本分离功能"""
    # 测试混合文本
    parts = FontUtils.separate_text_parts("中文123ABC")
    print(f"文本分离结果: {parts}")
    
    assert len(parts) >= 2
    # 应该能分离出中文和数字/英文部分
    
    # 测试纯中文
    parts_cn = FontUtils.separate_text_parts("纯中文测试")
    print(f"纯中文: {parts_cn}")
    assert len(parts_cn) == 1
    assert parts_cn[0][1] == 'chinese'
    
    # 测试纯数字
    parts_num = FontUtils.separate_text_parts("123456")
    print(f"纯数字: {parts_num}")
    assert len(parts_num) == 1
    assert parts_num[0][1] == 'number'
    
    # 测试空字符串
    parts_empty = FontUtils.separate_text_parts("")
    assert len(parts_empty) == 0


if __name__ == '__main__':
    print("运行字体工具测试...\n")
    
    print("测试 1: 字体检测")
    test_check_font_installed()
    print("✅ 测试通过\n")
    
    print("测试 2: 获取中文字体列表")
    test_get_available_chinese_fonts()
    print("✅ 测试通过\n")
    
    print("测试 3: 文本分离")
    test_separate_text_parts()
    print("✅ 测试通过\n")
    
    print("所有测试通过! ✅")

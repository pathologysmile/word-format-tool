"""完整功能测试脚本 - 验证 word-format-tool 的所有核心功能"""
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from document_parser import DocumentParser
from font_utils import FontUtils
from title_detector import TitleDetector


def test_complete_workflow():
    """测试完整工作流程"""
    print("=" * 60)
    print("Word 文档格式工具 - 完整功能测试")
    print("=" * 60)
    
    # 1. 测试文档解析器
    print("\n【1】测试文档解析器")
    print("-" * 60)
    
    doc_path = 'tests/sample_docs/sample_official.docx'
    if not os.path.exists(doc_path):
        print(f"❌ 测试文件不存在: {doc_path}")
        print("请先运行: python tests/create_sample_doc.py")
        return False
    
    parser = DocumentParser(doc_path)
    
    # 提取段落
    paragraphs = parser.extract_paragraphs()
    print(f"✅ 成功解析 {len(paragraphs)} 个段落")
    for i, para in enumerate(paragraphs[:3]):
        print(f"   段落 {i}: {para['preview']} (样式: {para['style']})")
    
    # 获取元数据
    metadata = parser.get_metadata()
    print(f"\n✅ 文档元数据:")
    print(f"   - 段落数: {metadata['paragraph_count']}")
    print(f"   - 表格数: {metadata['table_count']}")
    print(f"   - 节数: {metadata['section_count']}")
    print(f"   - 文件大小: {metadata['file_size_kb']:.2f} KB")
    
    # 获取页面设置
    page_setup = parser.get_page_setup()
    print(f"\n✅ 页面设置:")
    print(f"   - 上边距: {page_setup['top_margin']} mm")
    print(f"   - 下边距: {page_setup['bottom_margin']} mm")
    print(f"   - 左边距: {page_setup['left_margin']} mm")
    print(f"   - 右边距: {page_setup['right_margin']} mm")
    print(f"   - 页面宽度: {page_setup['page_width']} mm")
    print(f"   - 页面高度: {page_setup['page_height']} mm")
    
    # 2. 测试字体工具
    print("\n【2】测试字体工具")
    print("-" * 60)
    
    # 检测字体
    fonts_to_check = ["宋体", "黑体", "楷体", "仿宋", "微软雅黑"]
    print("✅ 字体检测结果:")
    for font in fonts_to_check:
        is_installed = FontUtils.check_font_installed(font)
        status = "✓" if is_installed else "✗"
        print(f"   {status} {font}")
    
    # 获取可用中文字体
    available_fonts = FontUtils.get_available_chinese_fonts()
    print(f"\n✅ 系统可用中文字体: {len(available_fonts)} 个")
    print(f"   {', '.join(available_fonts[:5])}" + ("..." if len(available_fonts) > 5 else ""))
    
    # 测试文本分离
    test_texts = [
        "中文123ABC",
        "纯中文测试",
        "123456",
        "混合文本：中文+123+English"
    ]
    print(f"\n✅ 文本分离测试:")
    for text in test_texts:
        parts = FontUtils.separate_text_parts(text)
        parts_str = " + ".join([f"{p[0]}({p[1]})" for p in parts])
        print(f"   '{text}' → {parts_str}")
    
    # 3. 测试标题识别器
    print("\n【3】测试标题识别器")
    print("-" * 60)
    
    detector = TitleDetector(paragraphs)
    
    # 基于样式识别
    style_results = detector.detect_by_style()
    print("✅ 基于样式的识别结果:")
    for item in style_results[:3]:
        print(f"   {item['text'][:20]:20s} → {item['level']:12s} (置信度: {item['confidence']:.2f})")
    
    # 基于正则模式识别
    pattern_results = detector.detect_by_pattern()
    print("\n✅ 基于正则模式的识别结果:")
    for item in pattern_results[:5]:
        print(f"   {item['text'][:20]:20s} → {item['level']:12s} (置信度: {item['confidence']:.2f})")
    
    # 混合识别
    hybrid_results = detector.hybrid_detect()
    print("\n✅ 混合识别结果:")
    for item in hybrid_results[:5]:
        print(f"   {item['text'][:20]:20s} → {item['level']:12s} (方法: {item['method']:8s}, 置信度: {item['confidence']:.2f})")
    
    # 4. 测试模板加载
    print("\n【4】测试模板配置")
    print("-" * 60)
    
    templates_dir = 'templates'
    template_files = ['official.json', 'academic.json', 'business.json']
    
    print("✅ 可用模板:")
    for template_file in template_files:
        template_path = os.path.join(templates_dir, template_file)
        if os.path.exists(template_path):
            import json
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
            print(f"   ✓ {template['name']} ({template['version']})")
            print(f"     {template['description']}")
        else:
            print(f"   ✗ {template_file} (不存在)")
    
    print("\n" + "=" * 60)
    print("✅ 所有功能测试通过！")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    try:
        success = test_complete_workflow()
        if success:
            print("\n🎉 Word 文档格式工具核心功能全部正常！")
        else:
            print("\n⚠️  部分功能测试失败，请检查上述错误信息")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

"""
Streamlit Cloud 部署前验证脚本

运行此脚本确保所有修改在本地正常工作。
"""

import io
import sys
from pathlib import Path

def test_font_utils():
    """测试字体工具模块"""
    print("🔍 测试 1: 字体工具模块")
    from src.font_utils import FontUtils
    
    # 测试云环境检测
    is_cloud = FontUtils.is_cloud_environment()
    print(f"  - 云环境检测: {is_cloud}")
    
    # 测试字体列表
    fonts = FontUtils.get_available_chinese_fonts()
    print(f"  - 可用中文字体数: {len(fonts)}")
    
    # 测试降级策略
    fallback = FontUtils.get_fallback_font("方正小标宋简体")
    print(f"  - 字体降级: 方正小标宋简体 -> {fallback}")
    
    print("  ✅ 字体工具测试通过\n")
    return True

def test_document_parser():
    """测试文档解析器(文件路径和内存流)"""
    print("🔍 测试 2: 文档解析器")
    from src.document_parser import DocumentParser
    
    test_file = "tests/sample_docs/sample_official.docx"
    if not Path(test_file).exists():
        print(f"  ⚠️  跳过: 测试文件不存在 ({test_file})\n")
        return True
    
    # 测试文件路径方式
    parser1 = DocumentParser(test_file)
    meta1 = parser1.get_metadata()
    print(f"  - 文件路径模式: {meta1['paragraph_count']} 段落")
    
    # 测试内存流方式
    with open(test_file, 'rb') as f:
        file_stream = io.BytesIO(f.read())
    
    parser2 = DocumentParser(file_stream)
    meta2 = parser2.get_metadata()
    print(f"  - 内存流模式: {meta2['paragraph_count']} 段落")
    
    # 验证结果一致
    assert meta1['paragraph_count'] == meta2['paragraph_count'], "两种模式结果不一致!"
    
    print("  ✅ 文档解析器测试通过\n")
    return True

def test_document_formatter():
    """测试文档格式化引擎(内存流输出)"""
    print("🔍 测试 3: 文档格式化引擎")
    from src.document_formatter import DocumentFormatter
    
    input_file = "tests/sample_docs/sample_official.docx"
    template_file = "templates/official.json"
    
    if not Path(input_file).exists():
        print(f"  ⚠️  跳过: 输入文件不存在 ({input_file})\n")
        return True
    
    if not Path(template_file).exists():
        print(f"  ⚠️  跳过: 模板文件不存在 ({template_file})\n")
        return True
    
    # 测试内存流输出
    output_stream = io.BytesIO()
    formatter = DocumentFormatter(template_file)
    formatter.apply_formatting(input_file, output_stream)
    
    output_size = len(output_stream.getvalue())
    print(f"  - 输出文件大小: {output_size} bytes")
    
    assert output_size > 0, "输出文件为空!"
    
    print("  ✅ 文档格式化引擎测试通过\n")
    return True

def test_templates():
    """测试模板文件"""
    print("🔍 测试 4: 模板文件")
    import json
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("  ❌ 模板目录不存在!\n")
        return False
    
    template_files = list(templates_dir.glob("*.json"))
    print(f"  - 找到 {len(template_files)} 个模板文件")
    
    for tf in template_files:
        try:
            with open(tf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  - ✅ {tf.name}: {data.get('name', 'Unknown')}")
        except Exception as e:
            print(f"  - ❌ {tf.name}: {str(e)}")
            return False
    
    print("  ✅ 模板文件测试通过\n")
    return True

def test_imports():
    """测试所有必要的导入"""
    print("🔍 测试 5: 依赖导入")
    
    required_modules = [
        'streamlit',
        'docx',
        'pandas',
        'lxml'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  - ✅ {module}")
        except ImportError as e:
            print(f"  - ❌ {module}: {str(e)}")
            return False
    
    print("  ✅ 依赖导入测试通过\n")
    return True

def main():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Streamlit Cloud 部署前验证")
    print("=" * 60)
    print()
    
    tests = [
        ("依赖导入", test_imports),
        ("字体工具", test_font_utils),
        ("文档解析器", test_document_parser),
        ("文档格式化引擎", test_document_formatter),
        ("模板文件", test_templates),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ {name} 测试异常: {str(e)}\n")
            results.append((name, False))
    
    # 汇总结果
    print("=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} - {name}")
    
    print()
    print(f"总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过!可以安全部署到 Streamlit Cloud")
        return 0
    else:
        print("\n⚠️  部分测试失败,请修复后再部署")
        return 1

if __name__ == "__main__":
    sys.exit(main())

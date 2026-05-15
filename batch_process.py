"""批量处理脚本 - 命令行模式下格式化多个文档"""

import os
import sys
import argparse
from src.document_formatter import DocumentFormatter


def batch_process(input_dir, template_path, output_dir):
    """
    批量处理目录下的所有 .docx 文件
    
    Args:
        input_dir: 输入目录路径
        template_path: 模板 JSON 路径
        output_dir: 输出目录路径
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    formatter = DocumentFormatter(template_path)
    files = [f for f in os.listdir(input_dir) if f.endswith('.docx')]
    
    print(f"📂 正在处理目录: {input_dir}")
    print(f"📄 找到 {len(files)} 个 Word 文档")
    print(f"🎨 使用模板: {template_path}")
    print("-" * 40)
    
    success_count = 0
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"formatted_{filename}")
        
        try:
            print(f"⏳ 正在处理: {filename} ...")
            formatter.apply_formatting(input_path, output_path)
            print(f"✅ 成功: {filename}")
            success_count += 1
        except Exception as e:
            print(f"❌ 失败: {filename} - {str(e)}")
            
    print("-" * 40)
    print(f"🎉 处理完成！成功: {success_count}/{len(files)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Word 文档批量格式化工具")
    parser.add_argument("--input", "-i", required=True, help="输入文件夹路径")
    parser.add_argument("--template", "-t", required=True, help="模板 JSON 文件路径")
    parser.add_argument("--output", "-o", default="./output", help="输出文件夹路径 (默认: ./output)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ 错误: 输入目录不存在 - {args.input}")
        sys.exit(1)
        
    if not os.path.exists(args.template):
        print(f"❌ 错误: 模板文件不存在 - {args.template}")
        sys.exit(1)
        
    batch_process(args.input, args.template, args.output)

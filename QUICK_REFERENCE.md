# Word 文档格式工具 - 快速参考指南

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行测试
```bash
# 创建测试文档
python tests/create_sample_doc.py

# 运行所有测试
python test_all_features.py

# 或单独运行各模块测试
python tests/test_document_parser.py
python tests/test_font_utils.py
python tests/test_title_detector.py
```

---

## 📚 核心 API 使用示例

### 1. 文档解析器

```python
from src.document_parser import DocumentParser

# 加载文档
parser = DocumentParser('path/to/document.docx')

# 提取段落
paragraphs = parser.extract_paragraphs()
for para in paragraphs:
    print(f"段落 {para['index']}: {para['text']}")
    print(f"  样式: {para['style']}")
    print(f"  Run数量: {para['runs_count']}")

# 获取元数据
metadata = parser.get_metadata()
print(f"段落数: {metadata['paragraph_count']}")
print(f"表格数: {metadata['table_count']}")

# 获取页面设置
page_setup = parser.get_page_setup()
print(f"上边距: {page_setup['top_margin']} mm")
print(f"页面大小: {page_setup['page_width']} x {page_setup['page_height']} mm")
```

### 2. 字体工具

```python
from src.font_utils import FontUtils

# 检测字体是否安装
if FontUtils.check_font_installed("宋体"):
    print("宋体已安装")

# 获取系统可用中文字体
fonts = FontUtils.get_available_chinese_fonts()
print(f"可用字体: {fonts}")

# 文本分离（用于差异化格式化）
parts = FontUtils.separate_text_parts("中文123ABC")
for text, type_ in parts:
    print(f"{text} ({type_})")
# 输出: 中文 (chinese), 123 (number), ABC (english)

# 获取替代字体
fallback = FontUtils.get_fallback_font("方正小标宋简体")
print(f"替代字体: {fallback}")  # 输出: 黑体
```

### 3. 标题识别器

```python
from src.document_parser import DocumentParser
from src.title_detector import TitleDetector

# 先解析文档
parser = DocumentParser('document.docx')
paragraphs = parser.extract_paragraphs()

# 创建识别器
detector = TitleDetector(paragraphs)

# 方法1: 基于样式识别
style_results = detector.detect_by_style()

# 方法2: 基于正则模式识别
pattern_results = detector.detect_by_pattern()

# 方法3: 混合识别（推荐）
hybrid_results = detector.hybrid_detect()
for item in hybrid_results:
    print(f"{item['text']} → {item['level']}")
    print(f"  方法: {item['method']}, 置信度: {item['confidence']}")
```

### 4. 加载模板

```python
import json

# 加载公文模板
with open('templates/official.json', 'r', encoding='utf-8') as f:
    template = json.load(f)

print(f"模板名称: {template['name']}")
print(f"标题字体: {template['levels']['title']['font_main']}")
print(f"正文字号: {template['levels']['body']['font_size_pt']} pt")
```

---

## 🎯 标题识别规则

### 样式识别优先级
1. **Title / 标题** → `title` (置信度 0.95)
2. **Heading 1 / 标题 1** → `heading_1` (置信度 0.95)
3. **Heading 2 / 标题 2** → `heading_2` (置信度 0.95)
4. **Heading 3 / 标题 3** → `heading_3` (置信度 0.95)
5. **Heading 4 / 标题 4** → `heading_4` (置信度 0.95)
6. **Normal / 正文** → `body` (置信度 0.90)

### 正则模式识别
| 层级 | 模式示例 | 正则表达式 |
|------|---------|-----------|
| heading_1 | 一、二、三、 | `^[一二三四五六七八九十百千]+、` |
| heading_2 | (一)、(二) | `^[(（][一二三四五六七八九十百千]+[)）]` |
| heading_3 | 1. 2. 3. | `^\d+\.\s*` |
| heading_4 | (1)、(2) | `^[(（]\d+[)）]` |

### 混合识别策略
```
IF 段落有明确样式 (非 Normal) THEN
    使用样式识别 (置信度 0.95)
ELSE IF 段落匹配正则模式 THEN
    使用正则识别 (置信度 0.80)
ELSE
    标记为正文 (置信度 0.90)
END IF
```

---

## 📋 预设模板对比

| 特性 | 公文标准 | 学术论文 | 商务文档 |
|------|---------|---------|---------|
| **适用场景** | 党政机关公文 | 学位论文、期刊 | 商业报告、方案 |
| **标题字体** | 方正小标宋简体 | 黑体 | 微软雅黑 |
| **正文字体** | 仿宋_GB2312 | 宋体 | 微软雅黑 |
| **字号** | 三号 (16pt) | 小四 (12pt) | 五号 (10.5pt) |
| **行距** | 固定 28.9pt | 1.5倍 | 固定 20pt |
| **首行缩进** | 2字符 | 2字符 | 无 |
| **对齐方式** | 两端对齐 | 两端对齐 | 左对齐 |
| **页边距** | 上37 下35 左28 右26 | 四边25 | 四边25 |

---

## 🔧 常见问题

### Q1: 如何添加新的字体支持？
在 `src/font_utils.py` 的 `_check_windows_font` 方法中添加字体映射：
```python
font_mapping = {
    "新字体名称": ["font_file.ttf"],
    # ...
}
```

### Q2: 如何自定义标题识别规则？
在 `src/title_detector.py` 的 `PATTERNS` 字典中添加新模式：
```python
PATTERNS = {
    'heading_5': r'^【\d+】',  # 【1】【2】
    # ...
}
```

### Q3: 如何创建新模板？
复制现有模板 JSON 文件，修改以下字段：
- `name`: 模板名称
- `description`: 描述
- `page`: 页面设置
- `levels`: 各层级格式配置

### Q4: 文本分离有什么用？
用于对同一段落中的中文、数字、英文应用不同字体：
```python
parts = FontUtils.separate_text_parts("第123章 Introduction")
# 可以分别设置：
# - 中文部分 → 宋体
# - 数字部分 → Times New Roman
# - 英文部分 → Arial
```

---

## 📁 项目结构

```
word-format-tool/
├── src/                      # 源代码
│   ├── document_parser.py    # 文档解析器
│   ├── font_utils.py         # 字体工具
│   └── title_detector.py     # 标题识别器
├── templates/                # 预设模板
│   ├── official.json         # 公文标准
│   ├── academic.json         # 学术论文
│   └── business.json         # 商务文档
├── tests/                    # 测试文件
│   ├── create_sample_doc.py  # 创建测试文档
│   ├── test_document_parser.py
│   ├── test_font_utils.py
│   └── test_title_detector.py
├── requirements.txt          # 依赖包
├── README.md                 # 项目说明
├── FUNCTION_TEST_REPORT.md   # 功能测试报告
└── QUICK_REFERENCE.md        # 本文件
```

---

## ✅ 当前状态

**已完成**:
- ✅ 文档解析（段落、表格、元数据、页面设置）
- ✅ 字体工具（检测、列表、回退、文本分离）
- ✅ 标题识别（样式、正则、混合策略）
- ✅ 模板系统（3种预设模板）
- ✅ 单元测试（10/10 通过）

**待开发**:
- 🔲 Streamlit Web 界面
- 🔲 文档格式化引擎
- 🔲 批量处理功能
- 🔲 模板管理 UI

---

## 📞 技术支持

如遇问题，请检查：
1. Python 版本 >= 3.8
2. 依赖包是否正确安装
3. 测试文档是否存在
4. 查看 `FUNCTION_TEST_REPORT.md` 了解详细测试结果

---

**最后更新**: 2026-05-14  
**版本**: v0.1.0 (核心功能版)

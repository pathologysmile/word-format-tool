import streamlit as st
import os
import json
import io
import pandas as pd
from src.document_parser import DocumentParser
from src.font_utils import FontUtils
from src.title_detector import TitleDetector
from src.document_formatter import DocumentFormatter

# 页面配置
st.set_page_config(
    page_title="Word 文档格式化工具",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Word 文档格式自动化工具")
st.markdown("自动将 Word 文档格式化为标准格式，支持公文、学术、商务、工作汇报、会议纪要等多种模板。")

# 侧边栏：文件上传与模板选择
with st.sidebar:
    st.header("⚙️ 配置")
    
    # 文件上传
    uploaded_file = st.file_uploader("上传 Word 文档 (.docx)", type=["docx"])
    
    # 模板选择
    templates_dir = "templates"
    template_files = [f for f in os.listdir(templates_dir) if f.endswith('.json')]
    template_options = {}
    for tf in template_files:
        with open(os.path.join(templates_dir, tf), 'r', encoding='utf-8') as f:
            t_data = json.load(f)
            template_options[t_data['name']] = tf
    
    selected_template_name = st.selectbox("选择格式化模板", list(template_options.keys()))
    selected_template_file = template_options[selected_template_name]
    
    # 文档清理功能
    st.markdown("---")
    st.subheader("🧹 文档清理")
    
    clean_empty = st.checkbox("清除空白段落", value=False)
    merge_blanks = st.checkbox("合并连续空行(保留1个)", value=True)
    remove_duplicates = st.checkbox("清除连续重复段落", value=False)
    
    clean_button = st.button("🧹 执行清理", disabled=not uploaded_file)
    
    # 操作按钮
    st.markdown("---")
    process_button = st.button("🚀 开始格式化", type="primary", disabled=not uploaded_file)
    
    # 模板管理入口
    if st.button("🛠️ 模板管理"):
        st.session_state.show_template_manager = True
    
    # 模板导入(仅会话期间有效,云环境不支持持久化)
    uploaded_template = st.file_uploader("📤 导入模板 (JSON)", type=["json"])
    if uploaded_template:
        try:
            content = uploaded_template.read().decode('utf-8')
            template_data = json.loads(content) # 验证格式
            
            # 云环境提示
            if FontUtils.is_cloud_environment():
                st.warning("⚠️ 云环境下模板仅在会话期间有效,刷新后将丢失")
                # 存储到 session_state
                if 'custom_templates' not in st.session_state:
                    st.session_state.custom_templates = {}
                st.session_state.custom_templates[uploaded_template.name] = template_data
                st.success(f"✅ 模板已加载: {uploaded_template.name}")
            else:
                # 本地环境保存到文件
                save_path = os.path.join(templates_dir, f"imported_{uploaded_template.name}")
                with open(save_path, "w", encoding='utf-8') as f:
                    f.write(content)
                st.success(f"✅ 模板已保存: {uploaded_template.name}")
                st.rerun()
        except Exception as e:
            st.error(f"❌ 导入失败: {str(e)}")

# 主区域：预览与结果
if 'show_template_manager' not in st.session_state:
    st.session_state.show_template_manager = False

if st.session_state.show_template_manager:
    # 顶部返回按钮（更显眼）
    col_back1, col_back2 = st.columns([1, 5])
    with col_back1:
        if st.button("⬅️ 返回主页", type="primary", use_container_width=True):
            st.session_state.show_template_manager = False
            st.rerun()
    
    st.header("🛠️ 模板管理")
    
    tab1, tab2, tab3 = st.tabs(["查看现有模板", "可视化编辑器", "导入/导出"])
    
    with tab1:
        for tf in template_files:
            with open(os.path.join(templates_dir, tf), 'r', encoding='utf-8') as f:
                t_data = json.load(f)
            with st.expander(f"📄 {t_data['name']} ({t_data.get('version', '1.0')})"):
                st.write(t_data.get('description', ''))
                st.json(t_data)
                # 导出按钮
                st.download_button(
                    label=f"💾 导出 {t_data['name']}",
                    data=json.dumps(t_data, ensure_ascii=False, indent=2),
                    file_name=tf,
                    mime="application/json"
                )
    
    with tab2:
        st.subheader("✏️ 自定义模板编辑器")
        
        # 操作栏：新建与选择
        col_act1, col_act2 = st.columns([1, 3])
        with col_act1:
            if st.button("➕ 新建空白模板"):
                new_template = {
                    "name": "新模板",
                    "version": "1.0",
                    "description": "在此处添加描述",
                    "page": {"margin_top_mm": 25, "margin_bottom_mm": 25, "margin_left_mm": 25, "margin_right_mm": 25},
                    "levels": {
                        "title": {"font_main": "方正小标宋简体", "font_size_pt": 22, "bold": True},
                        "heading_1": {"font_main": "黑体", "font_size_pt": 16, "bold": True},
                        "body": {"font_main": "仿宋_GB2312", "font_size_pt": 16}
                    }
                }
                st.session_state.editing_template = new_template
                st.session_state.editing_filename = "new_template.json"
                st.rerun()

        edit_template_name = st.selectbox("选择要编辑的模板", list(template_options.keys()))
        edit_file = template_options[edit_template_name]
        
        if st.button("📂 加载选中模板"):
            with open(os.path.join(templates_dir, edit_file), 'r', encoding='utf-8') as f:
                st.session_state.editing_template = json.load(f)
                st.session_state.editing_filename = edit_file

        if 'editing_template' in st.session_state:
            t = st.session_state.editing_template
            
            # 基础信息
            col_base1, col_base2 = st.columns(2)
            with col_base1: t['name'] = st.text_input("模板名称", t['name'])
            with col_base2: t['description'] = st.text_area("描述", t['description'])
            
            st.markdown("---")
            st.markdown("#### 📏 页面设置 (mm)")
            page = t.setdefault('page', {})
            p_col1, p_col2, p_col3, p_col4 = st.columns(4)
            with p_col1: page['margin_top_mm'] = st.number_input("上边距", value=page.get('margin_top_mm', 25))
            with p_col2: page['margin_bottom_mm'] = st.number_input("下边距", value=page.get('margin_bottom_mm', 25))
            with p_col3: page['margin_left_mm'] = st.number_input("左边距", value=page.get('margin_left_mm', 25))
            with p_col4: page['margin_right_mm'] = st.number_input("右边距", value=page.get('margin_right_mm', 25))

            st.markdown("---")
            st.markdown("#### 🔤 各级标题与正文样式配置")
            
            # 优化：将字体列表存入 session_state，避免重复扫描导致卡顿
            if 'system_fonts' not in st.session_state:
                with st.spinner('正在加载系统字体...'):
                    st.session_state.system_fonts = FontUtils.get_system_fonts()
            system_fonts = st.session_state.system_fonts
            
            levels = t.setdefault('levels', {})
            level_names = {
                'title': '材料总标题',
                'heading_1': '一级标题 (一、)',
                'heading_2': '二级标题 ((一))',
                'heading_3': '三级标题 (1.)',
                'heading_4': '四级标题 ((1))',
                'body': '正文'
            }
            
            for key, label in level_names.items():
                with st.expander(f"{label} ({key})"):
                    lvl = levels.setdefault(key, {})
                    l_col1, l_col2, l_col3 = st.columns(3)
                    with l_col1:
                        current_font = lvl.get('font_main', '宋体')
                        font_options = system_fonts.copy()
                        if current_font not in font_options:
                            font_options.append(current_font)
                        try:
                            idx = font_options.index(current_font)
                        except ValueError:
                            idx = 0
                            
                        lvl['font_main'] = st.selectbox(
                            "中文字体", 
                            options=font_options, 
                            index=idx,
                            key=f"font_{key}"
                        )
                        # 新增：英文/数字字体配置
                        current_num_font = lvl.get('font_number', 'Times New Roman')
                        num_font_options = system_fonts.copy()
                        if 'Times New Roman' not in num_font_options:
                            num_font_options.insert(0, 'Times New Roman')
                        if current_num_font not in num_font_options:
                            num_font_options.append(current_num_font)
                        try:
                            num_idx = num_font_options.index(current_num_font)
                        except ValueError:
                            num_idx = 0
                            
                        lvl['font_number'] = st.selectbox(
                            "英文/数字字体", 
                            options=num_font_options, 
                            index=num_idx,
                            key=f"num_font_{key}"
                        )
                    with l_col2:
                        lvl['font_size_pt'] = st.number_input("字号 (pt)", value=lvl.get('font_size_pt', 12), key=f"size_{key}")
                        lvl['bold'] = st.checkbox("加粗", value=lvl.get('bold', False), key=f"bold_{key}")
                        lvl['first_line_indent_chars'] = st.number_input("首行缩进 (字符)", value=lvl.get('first_line_indent_chars', 0), key=f"indent_{key}")
                    with l_col3:
                        # 完整的行距类型选项（与 Word 一致）
                        line_spacing_options = {
                            'single': '单倍行距',
                            '1.5': '1.5 倍行距',
                            'double': '2 倍行距',
                            'at_least': '最小值',
                            'exactly': '固定值',
                            'multiple': '多倍行距'
                        }
                        
                        # 兼容旧模板的 'fixed' -> 'exactly'
                        current_ls_type = lvl.get('line_spacing_type', 'multiple')
                        if current_ls_type == 'fixed':
                            current_ls_type = 'exactly'
                            lvl['line_spacing_type'] = 'exactly'
                        
                        # 安全获取索引
                        ls_type_keys = list(line_spacing_options.keys())
                        if current_ls_type not in ls_type_keys:
                            current_ls_type = 'multiple'
                        ls_type_idx = ls_type_keys.index(current_ls_type)
                        
                        selected_ls_key = st.selectbox(
                            "行距类型", 
                            options=ls_type_keys,
                            format_func=lambda x: line_spacing_options[x],
                            index=ls_type_idx,
                            key=f"ls_type_{key}"
                        )
                        lvl['line_spacing_type'] = selected_ls_key
                        
                        # 根据行距类型设置默认值
                        default_ls_val = 30.0 if selected_ls_key in ('exactly', 'at_least') else (2.0 if selected_ls_key == 'double' else (1.5 if selected_ls_key == '1.5' else 1.0))
                        
                        current_ls_val = lvl.get('line_spacing_value', default_ls_val)
                        # 确保是浮点数
                        try:
                            current_ls_val = float(current_ls_val)
                        except (ValueError, TypeError):
                            current_ls_val = default_ls_val
                        
                        lvl['line_spacing_value'] = st.number_input(
                            "行距值 (磅/倍数)", 
                            value=current_ls_val, 
                            step=0.5,
                            key=f"ls_val_{key}"
                        )
                        lvl['space_before_lines'] = st.number_input("段前空行数", value=float(lvl.get('space_before_lines', 0.0)), step=0.5, key=f"sb_{key}")
                        lvl['space_after_lines'] = st.number_input("段后空行数", value=float(lvl.get('space_after_lines', 0.0)), step=0.5, key=f"sa_{key}")

            # 保存与删除操作
            save_col, del_col = st.columns([3, 1])
            with save_col:
                if st.button("💾 保存/更新模板", type="primary"):
                    try:
                        # 云环境不支持持久化保存
                        if FontUtils.is_cloud_environment():
                            st.warning("⚠️ 云环境下无法保存模板到服务器")
                            st.info("💡 请使用'导入/导出'标签页下载模板文件，下次使用时重新上传")
                        else:
                            save_name = st.session_state.editing_filename
                            # 如果名称变了，更新文件名
                            clean_name = st.session_state.editing_filename.replace('.json', '').replace('custom_', '')
                            if t['name'] != clean_name and t['name'] != "新模板":
                                 save_name = f"custom_{t['name']}.json"
                            
                            save_path = os.path.join(templates_dir, save_name)
                            with open(save_path, 'w', encoding='utf-8') as f:
                                json.dump(t, f, ensure_ascii=False, indent=2)
                            
                            st.success(f"✅ 模板已成功保存为: {save_name}")
                            st.session_state.editing_filename = save_name
                            # 强制刷新以更新下拉列表
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ 保存失败: {str(e)}")
            
            with del_col:
                if st.button("🗑️ 删除当前模板", type="secondary"):
                    # 云环境不支持删除服务器文件
                    if FontUtils.is_cloud_environment():
                        st.warning("⚠️ 云环境下无法删除服务器模板")
                    else:
                        delete_path = os.path.join(templates_dir, st.session_state.editing_filename)
                        if os.path.exists(delete_path):
                            os.remove(delete_path)
                            st.success("✅ 模板已删除")
                            del st.session_state.editing_template
                            st.rerun()
    
    with tab3:
        st.info("在此处上传或下载 JSON 格式的模板文件。")
        
    if st.button("返回主页"):
        st.session_state.show_template_manager = False
        st.rerun()

elif uploaded_file:
    # 使用内存处理,避免临时文件(适合云环境)
    file_content = uploaded_file.read()
    file_stream = io.BytesIO(file_content)
    
    try:
        # 1. 解析文档(从内存流)
        parser = DocumentParser(file_stream)
        paragraphs = parser.extract_paragraphs()
        metadata = parser.get_metadata()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("📄 文档预览")
            st.json(metadata)
        
        with col2:
            st.subheader("📊 统计信息")
            st.metric("段落数", metadata['paragraph_count'])
            st.metric("表格数", metadata['table_count'])
            st.metric("文件大小", f"{metadata['file_size_kb']:.2f} KB")
        
        # 处理清理操作
        if clean_button:
            from src.document_cleaner import DocumentCleaner
            
            # 保存原始段落
            st.session_state.original_paragraphs = paragraphs.copy()
            
            # 执行清理
            cleaner = DocumentCleaner(paragraphs)
            clean_result = cleaner.clean_all({
                'remove_empty': clean_empty,
                'merge_blanks': merge_blanks,
                'remove_duplicates': remove_duplicates
            })
            
            # 更新段落
            paragraphs = clean_result['paragraphs']
            st.session_state.cleaned_paragraphs = paragraphs
            st.session_state.clean_stats = clean_result['stats']
            
            st.success("✅ 清理完成！")
            st.info(
                f"📊 清理统计:\n"
                f"- 删除空段落: {clean_result['stats']['removed_empty']} 个\n"
                f"- 合并空行: {clean_result['stats']['merged_blanks']} 个\n"
                f"- 删除重复: {clean_result['stats']['removed_duplicates']} 个\n"
                f"- 清理前: {clean_result['original_count']} 段 → 清理后: {clean_result['cleaned_count']} 段"
            )
            st.rerun()
        
        # 如果有清理后的段落，使用清理后的
        if 'cleaned_paragraphs' in st.session_state:
            paragraphs = st.session_state.cleaned_paragraphs
        
        # 显示恢复按钮
        if 'cleaned_paragraphs' in st.session_state:
            if st.button("🔄 恢复原始文档"):
                paragraphs = st.session_state.original_paragraphs
                st.session_state.cleaned_paragraphs = paragraphs
                if 'original_paragraphs' in st.session_state:
                    del st.session_state.original_paragraphs
                if 'clean_stats' in st.session_state:
                    del st.session_state.clean_stats
                st.rerun()

        # 2. 标题识别与手动修正
        detector = TitleDetector(paragraphs)
        detected_titles = detector.hybrid_detect()
        
        st.subheader("🔍 智能标题识别与修正")
        st.markdown("💡 **提示**：你可以直接在下方表格中修改段落的层级，以确保格式化结果精准。")
        
        # 将识别结果转换为可编辑的 DataFrame
        df = pd.DataFrame(detected_titles)
        
        # 定义层级选项
        level_options = ['title', 'heading_1', 'heading_2', 'heading_3', 'heading_4', 'body']
        
        # 使用 st.data_editor 允许用户修改层级
        edited_df = st.data_editor(
            df[['index', 'text', 'level', 'confidence', 'method']],
            column_config={
                "index": "序号",
                "text": st.column_config.TextColumn("文本内容", width="large"),
                "level": st.column_config.SelectboxColumn("层级", options=level_options, required=True),
                "confidence": st.column_config.ProgressColumn("置信度", min_value=0, max_value=1),
                "method": "识别方法"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # 更新 detected_titles 为用户修正后的结果
        for i, row in edited_df.iterrows():
            if i < len(detected_titles):
                detected_titles[i]['level'] = row['level']

        # 3. 字体检测
        with st.expander("🔤 系统字体环境检测"):
            available_fonts = FontUtils.get_available_chinese_fonts()
            st.write(f"当前系统可用中文字体 ({len(available_fonts)} 个):")
            st.write(", ".join(available_fonts))

        # 4. 格式化逻辑
        if process_button:
            with st.spinner('🚀 正在应用模板格式化，请稍候...'):
                try:
                    template_path = os.path.join(templates_dir, selected_template_file)
                    output_filename = f"formatted_{uploaded_file.name}"
                    
                    # 使用内存流进行格式化
                    output_stream = io.BytesIO()
                    
                    formatter = DocumentFormatter(template_path)
                    # 将识别出的标题层级传入格式化引擎
                    formatter.apply_formatting(file_stream, output_stream, detected_levels=detected_titles)
                    
                    st.success("✅ 格式化完成！")
                    
                    # 提供下载按钮(从内存流)
                    output_stream.seek(0)
                    st.download_button(
                        label="📥 下载格式化后的文档",
                        data=output_stream.getvalue(),
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.error(f"❌ 格式化失败: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
            
    except Exception as e:
        st.error(f"❌ 处理出错: {str(e)}")
else:
    st.info("👈 请在左侧上传 .docx 文件以开始使用")

# 底部说明
st.markdown("---")
st.caption("基于 python-docx 和 Streamlit 构建 | 符合 GB/T 9704-2012 标准")

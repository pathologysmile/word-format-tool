# Streamlit Cloud 部署指南

本文档说明如何将 Word 文档格式化工具部署到 Streamlit Cloud。

## 📋 部署前准备

### 1. GitHub 仓库准备

确保你的代码已推送到 GitHub 仓库,并且包含以下文件:

```
word-format-tool/
├── app.py                      # 主应用文件
├── requirements.txt            # Python 依赖
├── .streamlit/
│   ├── config.toml            # Streamlit 配置
│   └── secrets.toml.example   # 密钥配置示例
├── src/                        # 源代码模块
├── templates/                  # 预置模板
└── font/                       # 字体文件(可选)
```

### 2. 关键修改说明

本项目已针对云环境进行了以下优化:

#### ✅ 已完成优化

1. **内存流处理**: 使用 `io.BytesIO` 替代临时文件,避免云环境文件系统限制
2. **字体降级策略**: 检测云环境后自动使用通用字体(SimSun/SimHei)
3. **模板管理限制**: 云环境下禁用模板持久化保存,仅支持会话期间使用
4. **依赖版本锁定**: 明确指定依赖版本范围,确保云环境兼容性

#### ⚠️ 功能限制

- **自定义字体**: 云环境无法使用 `font/` 目录下的自定义字体
- **模板保存**: 用户上传的模板仅在会话期间有效,刷新后丢失
- **批量处理**: `batch_process.py` 不适用于云环境(需要本地运行)

---

## 🚀 部署步骤

### 步骤 1: 登录 Streamlit Cloud

访问 [https://streamlit.io/cloud](https://streamlit.io/cloud) 并使用 GitHub 账号登录。

### 步骤 2: 创建新应用

1. 点击 **"New app"** 按钮
2. 选择你的 GitHub 仓库
3. 配置应用参数:

```
Repository: your-username/word-format-tool
Branch: main (或你的分支名)
Main file path: app.py
```

### 步骤 3: 高级设置(可选)

如果需要配置环境变量:

1. 点击 **"Advanced settings"**
2. 添加环境变量(本项目暂不需要)

### 步骤 4: 部署

点击 **"Deploy!"** 按钮,等待部署完成(通常需要 2-5 分钟)。

---

## 🔧 常见问题

### Q1: 部署失败,提示 "ModuleNotFoundError"

**原因**: 依赖未正确安装

**解决方案**:
1. 检查 `requirements.txt` 是否包含所有依赖
2. 确保没有语法错误
3. 查看部署日志中的详细错误信息

### Q2: 应用运行缓慢

**原因**: Streamlit Cloud 免费层资源有限

**解决方案**:
1. 减少同时处理的文件大小(建议 < 10MB)
2. 避免上传过多大文件
3. 考虑升级到付费计划

### Q3: 字体显示不正确

**原因**: 云环境缺少中文字体

**解决方案**:
- 当前已配置字体降级策略,会自动使用通用字体
- 如需精确字体控制,建议在本地运行

### Q4: 模板保存后丢失

**原因**: 云环境不支持持久化存储

**解决方案**:
1. 使用"导入/导出"功能下载模板 JSON 文件
2. 下次使用时重新上传
3. 或在本地运行以保存模板

---

## 📊 性能优化建议

### 文件大小限制

- **推荐**: < 5MB
- **最大**: < 50MB (可能超时)

### 并发处理

Streamlit Cloud 免费层限制:
- 最多 1 个并发会话
- 每小时自动休眠(无活动时)

### 缓存策略

应用已使用内存流处理,无需额外缓存配置。

---

## 🔐 安全注意事项

1. **不要提交敏感信息**: `.streamlit/secrets.toml` 已在 `.gitignore` 中
2. **文件隐私**: 用户上传的文件仅在会话期间存在,不会持久化
3. **HTTPS**: Streamlit Cloud 默认启用 HTTPS

---

## 🧪 本地测试

在部署前,建议在本地测试:

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行应用
streamlit run app.py

# 3. 访问 http://localhost:8501
```

---

## 📞 获取帮助

- Streamlit 官方文档: [https://docs.streamlit.io](https://docs.streamlit.io)
- Streamlit Community Forum: [https://discuss.streamlit.io](https://discuss.streamlit.io)
- 项目 Issues: [GitHub Issues](your-repo-url/issues)

---

## 📝 更新应用

修改代码后:

1. 提交并推送到 GitHub
2. Streamlit Cloud 会自动检测变化并重新部署
3. 或者手动点击 **"Manage app" → "Redeploy"**

---

**最后更新**: 2026-05-15

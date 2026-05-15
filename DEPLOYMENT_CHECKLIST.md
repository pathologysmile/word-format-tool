# Streamlit Cloud 部署快速检查清单

## ✅ 部署前检查

### 1. 代码验证
```bash
# 运行自动化测试
python verify_deployment.py
```
- [ ] 所有 5 项测试通过

### 2. Git 状态检查
```bash
git status
```
- [ ] 没有未提交的 `.docx` 文件
- [ ] 没有提交 `.streamlit/secrets.toml`
- [ ] `temp/` 目录已清空

### 3. 依赖检查
```bash
pip install -r requirements.txt
```
- [ ] 无安装错误
- [ ] 版本兼容

### 4. 本地测试
```bash
streamlit run app.py
```
- [ ] 应用正常启动
- [ ] 上传文档能正常格式化
- [ ] 下载功能正常

---

## 🚀 部署步骤

### Step 1: 推送到 GitHub
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: 登录 Streamlit Cloud
访问: https://streamlit.io/cloud

### Step 3: 创建应用
- Repository: `your-username/word-format-tool`
- Branch: `main`
- Main file path: `app.py`

### Step 4: 等待部署
- 通常 2-5 分钟
- 查看日志确认无错误

---

## 🔍 部署后验证

### 1. 基本功能测试
- [ ] 页面正常加载
- [ ] 模板下拉列表显示 6 个预置模板
- [ ] 上传 .docx 文件成功

### 2. 核心流程测试
- [ ] 选择模板 → 点击"开始格式化"
- [ ] 标题识别表格正常显示
- [ ] 下载按钮出现

### 3. 云环境特性验证
- [ ] 字体检测显示空列表(或提示云环境)
- [ ] 尝试保存模板时显示警告信息
- [ ] 导入模板时显示会话有效期提示

---

## ⚠️ 常见问题速查

### Q: 部署失败,日志显示 "ModuleNotFoundError"
**解决**: 
```bash
# 检查 requirements.txt 是否包含所有依赖
cat requirements.txt
# 确保没有语法错误
```

### Q: 应用启动但页面空白
**解决**:
- 检查浏览器控制台是否有 CORS 错误
- 确认 `app.py` 路径正确
- 查看 Streamlit Cloud 日志

### Q: 上传文件后卡住
**解决**:
- 文件大小 < 50MB
- 检查网络超时设置
- 查看 Cloud 日志中的内存使用

### Q: 字体显示不正确
**说明**: 这是预期行为,云环境使用降级字体(SimSun/SimHei)

### Q: 模板保存后刷新丢失
**说明**: 这是预期行为,云环境不支持持久化存储

---

## 📊 性能指标参考

| 指标 | 预期值 | 说明 |
|------|--------|------|
| 冷启动时间 | 30-60s | 首次访问或休眠后 |
| 热启动时间 | 2-5s | 活跃状态下 |
| 小文件处理(<1MB) | 3-5s | 包含标题识别 |
| 中文件处理(1-5MB) | 5-15s | - |
| 大文件处理(5-50MB) | 15-60s | 可能超时 |

---

## 🆘 获取帮助

1. **查看日志**: Streamlit Cloud → Manage app → Logs
2. **官方文档**: https://docs.streamlit.io/streamlit-community-cloud
3. **社区论坛**: https://discuss.streamlit.io
4. **项目 Issues**: GitHub Issues

---

## 📝 更新应用

修改代码后:
```bash
git add .
git commit -m "Update description"
git push origin main
```
Streamlit Cloud 会自动重新部署(约 1-2 分钟)

---

**最后更新**: 2026-05-15

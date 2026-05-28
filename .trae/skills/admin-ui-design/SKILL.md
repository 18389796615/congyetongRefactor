---
name: "admin-ui-design"
description: "运维端UI设计规范skill。用于创建或审查运维管理系统原型时，确保UI布局、组件、筛选器、表格等符合统一规范。Invoke when designing admin pages or reviewing admin UI."
---

# 运维端UI设计规范

## 概述

本规范定义运维端管理系统的UI设计标准，适用于企业入驻、用户管理、配置管理、规则配置等所有运维管理页面。

---

## 一、页面布局规范

### 1.1 整体布局
```
页面容器 (max-width: 1400px, margin: 0 auto)
├── 面包屑导航 (breadcrumb)
├── 页面标题区 (page-header)
│   ├── 标题
│   └── 操作按钮
├── 筛选区域 (filter-bar)
├── 表格区域 (table-container)
└── 分页区域 (pagination)
```

### 1.2 间距规范
- 页面内边距：`24px`
- 区块间距：`20px`
- 组件间距：`12px`
- 按钮间距：`10px`

---

## 二、筛选器规范 (filter-bar)

### 2.1 结构
```html
<div class="filter-bar">
    <div class="filter-item">
        <input type="text" class="form-input filter-input" placeholder="搜索...">
    </div>
    <div class="filter-item">
        <select class="form-select filter-select">...</select>
    </div>
    <div class="filter-actions">
        <button class="btn btn-secondary">重置</button>
        <button class="btn btn-primary">筛选</button>
    </div>
</div>
```

### 2.2 规范要点
- **不使用label标签**：通过placeholder提示输入内容
- **输入框**：使用`filter-input`类，width: 220px
- **下拉框**：使用`filter-select`类，width: 160px
- **按钮区**：使用`filter-actions`类，margin-left: auto
- **筛选按钮**：btn-primary
- **重置按钮**：btn-secondary
- **去掉"全部"文案**：筛选项placeholder直接描述内容

---

## 三、表格规范

### 3.1 表格结构
```html
<div class="table-container">
    <table class="data-table">
        <thead>
            <tr>
                <th>表头1</th>
                <th>表头2</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>内容1</td>
                <td>内容2</td>
                <td>
                    <div class="action-links">
                        <span class="action-link">编辑</span>
                        <span class="action-link">删除</span>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### 3.2 操作列规范
- 使用`action-links`容器包裹
- 使用`action-link`类定义单个操作
- 操作之间用分隔符或空格区分
- 常用操作：查看、编辑、删除、启用/禁用

---

## 四、模态框规范

### 4.1 模态框结构
```html
<div class="modal-overlay" id="xxxModal">
    <div class="modal modal-lg">
        <div class="modal-header">
            <span class="modal-title">标题</span>
            <button class="modal-close">✕</button>
        </div>
        <div class="modal-body">
            <!-- 表单内容 -->
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary">取消</button>
            <button class="btn btn-primary">保存</button>
        </div>
    </div>
</div>
```

### 4.2 尺寸规范
- `modal-sm`：400px
- `modal-md`：560px
- `modal-lg`：800px
- `modal-xl`：1000px

---

## 五、表单规范

### 5.1 表单结构
```html
<div class="form-row">
    <div class="form-group">
        <label class="form-label">标签名 *</label>
        <input type="text" class="form-input" placeholder="请输入...">
    </div>
</div>
```

### 5.2 表单布局
- 使用`form-row`包裹一行多个表单项
- 使用`form-group`包裹单个表单项
- label使用`form-label`类
- 输入框使用`form-input`类
- 选择框使用`form-select`类
- 必填项在label后加`*`

---

## 六、按钮规范

### 6.1 按钮类型
| 类型 | 类名 | 用途 |
|------|------|------|
| 主要按钮 | btn-primary | 确认、提交、筛选 |
| 次要按钮 | btn-secondary | 取消、重置 |
| 轮廓按钮 | btn-outline | 辅助操作 |
| 危险按钮 | btn-danger | 删除、禁用 |

### 6.2 按钮尺寸
- `btn-sm`：小按钮（表格内操作）
- 默认：中按钮（表单操作）
- `btn-lg`：大按钮（主要操作）

---

## 七、状态标识规范

### 7.1 状态标签
```html
<span class="status-badge status-enabled">启用</span>
<span class="status-badge status-disabled">禁用</span>
<span class="status-badge status-pending">待处理</span>
```

### 7.2 行业标签
```html
<span class="industry-badge industry-coal">煤矿行业</span>
<span class="industry-badge industry-non-coal">非煤矿行业</span>
```

---

## 八、步骤流程规范

### 8.1 向导步骤结构
```
步骤指示器 (step-indicators)
├── 步骤1 (已完成/进行中/待完成)
├── 步骤2
├── 步骤3
...
步骤内容区 (step-content)
└── 按钮区 (上一步、下一步、完成)
```

### 8.2 入驻进度结构
```html
<div class="progress-step-item completed/pending/disabled">
    <div class="step-checkbox checked">
        <input type="checkbox">
    </div>
    <div class="step-content">
        <div class="step-title">步骤X: 标题</div>
        <div class="step-desc">描述</div>
        <div class="step-time">时间/状态</div>
    </div>
    <span class="step-status">已完成</span>
    <!-- 或 -->
    <button class="btn btn-sm btn-primary" onclick="navigateToStep(X)">立即配置</button>
</div>
```

---

## 九、交互规范

### 9.1 交互反馈
- 按钮点击：显示loading态
- 表单提交：toast提示成功/失败
- 数据操作：确认对话框
- 分页：loading态

### 9.2 Toast提示
```javascript
showToast('操作成功', 'success');
showToast('操作失败', 'error');
showToast('警告信息', 'warning');
```

---

## 十、名词定义

| 名词 | 定义 |
|------|------|
| 运维端 | 后台管理系统，用于企业管理、用户管理、配置管理等 |
| 企业入驻 | 新企业申请使用系统并完成初始配置的过程 |
| 入驻进度 | 企业入驻各步骤的完成状态 |
| 流程配置 | 定义企业入职的步骤流程 |
| 规则配置 | 定义业务规则和校验规则 |

---

## 十一、检查清单

新增或修改页面时，确保符合以下规范：

- [ ] 筛选区域使用filter-bar结构
- [ ] 不使用label作为筛选提示
- [ ] 按钮使用正确的类型和尺寸
- [ ] 表格操作列使用action-links
- [ ] 模态框结构完整
- [ ] 表单使用form-row/form-group
- [ ] 状态使用统一的status-badge
- [ ] Toast提示反馈操作结果

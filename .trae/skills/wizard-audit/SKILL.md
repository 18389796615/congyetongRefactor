---
name: "wizard-audit"
description: "审计向导/流程的完整性和一致性。适用于：需求变更后检查、流程调试、步骤跳转异常时。自动验证步骤结构、JS逻辑、数据保存、按钮显示的一致性。"
---

# 向导流程审计技能

## 功能说明

自动检查新增企业向导（或任何多步骤流程）的完整性和一致性，确保：
1. 步骤数量一致（HTML指示器、HTML内容、JS逻辑）
2. 步骤编号对应关系正确
3. 数据保存与步骤对应
4. 验证逻辑与步骤对应
5. 按钮显示逻辑与步骤数量匹配

## 使用场景

- **需求变更后**：每次修改向导步骤后自动执行
- **流程调试**：当用户反馈"下一步不生效"时执行
- **步骤跳转异常**：检查步骤3→4跳转问题时执行

## 审计清单

### 1. 步骤指示器检查
```javascript
// 查找 .wizard-steps 下的 .wizard-step 数量
// 对比 updateWizardUI() 中的按钮显示逻辑
document.getElementById('wizardNext').style.display = currentWizardStep < N ? 'block' : 'none';
```

### 2. 步骤内容检查
```javascript
// 查找所有 wizard-content (id="wizardStep1", "wizardStep2", ...)
// 确认每个步骤都有内容，且步骤数量 = N
```

### 3. validateStep 函数检查
```javascript
// 确认有 step === 1, 2, 3, ... N 的分支
// 确认每个分支引用的元素ID在对应步骤HTML中存在
```

### 4. saveStepData 函数检查
```javascript
// 确认有 step === 1, 2, 3, ... N 的分支
// 确认每个分支保存的数据与步骤内容一致
```

### 5. nextWizardStep 函数检查
```javascript
// 确认 currentWizardStep < N 时的按钮显示
// 确认 currentWizardStep === N 时显示"完成"按钮
// 确认步骤切换后的回调函数（如 populateSummary）引用的元素存在
```

### 6. populateSummary 函数检查
```javascript
// 确认所有 document.getElementById('summaryXXX') 引用的元素存在于 wizardStepN
// 确认所有 wizardData.XXX 引用在 saveStepData 中有保存
```

### 7. resetWizardForms 函数检查
```javascript
// 确认所有表单字段ID都在HTML步骤内容中存在
// 移除已删除步骤的字段
```

## 常见问题及修复

| 问题 | 原因 | 修复 |
|------|------|------|
| 下一步不生效 | validateStep缺少对应步骤的验证分支 | 添加 `else if (step === N)` 分支 |
| 数据丢失 | saveStepData缺少对应步骤 | 添加 `else if (step === N)` 保存逻辑 |
| 步骤内容错位 | HTML步骤内容与编号不匹配 | 重新排列HTML结构 |
| 按钮显示错误 | updateWizardUI中N值不正确 | 将N改为实际步骤数 |
| 摘要显示空白 | populateSummary引用了不存在的元素 | 检查元素ID或移除引用 |

## 执行方式

1. 读取HTML文件中的向导相关代码
2. 对照审计清单逐项检查
3. 发现问题后立即修复
4. 修复后再次执行审计确认

## 自查流程

```
1. 统计步骤数量 N
   ↓
2. 检查HTML: wizard-steps (应为N个)
   ↓
3. 检查HTML: wizard-content (应为N个)
   ↓
4. 检查JS: updateWizardUI 按钮逻辑 (N值)
   ↓
5. 检查JS: validateStep (1~N分支)
   ↓
6. 检查JS: saveStepData (1~N分支)
   ↓
7. 检查JS: populateSummary (所有引用元素存在)
   ↓
8. 检查JS: resetWizardForms (所有字段ID存在)
   ↓
9. 如有异常 → 修复 → 重新审计
```

# Decision Engine Issues
# 记录 Decision Engine 相关的问题和发现

---

## Issue 001: Decision Engine 可能只是 Prompt 包装

### 发现日期
2026-06-17

### 症状
- PCOS 输出看起来像 LLM 直接回答
- 没有明显体现 Identity 规则执行
- 特别是 prefer_optionality 模式没有生效

### 测试方法

**Test A: 关闭 Identity**
- 只给问题，不给 Identity 信息
- 观察输出

**Test B: 开启 Identity**
- 给完整的 Identity 信息
- 观察输出

**比较：**
- 如果 95% 一样 → Identity 没生效
- 如果明显不同 → Identity 开始影响决策

### 预期结果

如果 Identity 真正生效，Test B 应该：
1. 识别出 prefer_optionality 模式
2. 推荐 "AI+Java" 而非 "纯AI"
3. 输出 value_conflicts 显示 career_security 损失

### 状态
- [x] 已识别
- [ ] 待验证

---

## Issue 002: 一致性判断器是字符串比较

### 发现日期
2026-06-17

### 症状
- "AI为主+Java补充" vs "学习AI" 被判断为不一致
- 实际上方向一致，只是细节不同

### 修复

已更新为语义级别对齐计算：

```python
def calculate_decision_alignment(pcos_result, actual_decision):
    # 提取关键概念
    # 计算重叠度
    # 返回 0.0-1.0 的对齐分数
```

### 状态
- [x] 已识别
- [x] 已修复

---

## Issue 003: 缺少 Decision Influence Rate

### 发现日期
2026-06-17

### 症状
- 当前只有 "一致/不一致" 指标
- 无法知道 PCOS 是否真正影响了决策

### 新指标

**Decision Influence Rate**

统计 PCOS 建议是否改变了用户的最终决策。

```yaml
decision_001:
  before: 计划学Java
  pcos: 学AI
  after: 学AI
  influenced: true
```

### 实现方案

在 decision_workflow.py 中增加：
1. 记录 "你原本的计划是什么？"
2. 记录 "PCOS 建议后你改了吗？"
3. 计算 Influence Rate

### 状态
- [x] 已识别
- [ ] 待实现

---

## 待记录

（等待更多 Decision Engine 相关问题）

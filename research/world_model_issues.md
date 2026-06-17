# World Model Issues
# 记录 World Model 相关的问题和发现

---

## Issue 001: 信念检索是 Top-N 固定加载，不是 Topic-Based

### 发现日期
2026-06-17

### 症状
- 无论问什么问题，都返回同样的 3 个信念：
  - AI Agent市场正在快速增长
  - 中小企业AI需求不明确
  - LLM技术快速迭代

### 问题

问 "Should I learn Java?" 时，应该返回：
- enterprise_systems (企业系统依赖Java)
- legacy_software (遗留软件)
- backend_stability (后端稳定性)
- hiring_market (招聘市场)

但实际返回的是 AI 相关信念。

### 根本原因

`context_builder.py` 的信念检索逻辑：

```python
def filter_beliefs_by_topics(beliefs, topics):
    # 当前：如果话题匹配就返回
    # 问题：话题提取可能不够精确
```

可能的问题：
1. 话题提取不够精确
2. 信念内容与话题关键词不匹配
3. 信念数量太少，总是返回所有

### 修复方案

1. 改进话题提取逻辑
2. 增加更多信念到 world_model_data.yaml
3. 实现真正的语义检索 (未来)

### 状态
- [x] 已识别
- [ ] 待修复

---

## Issue 002: World Model 信念太少

### 发现日期
2026-06-17

### 症状
- 只有 5 个信念
- 覆盖范围有限

### 当前信念

```yaml
beliefs:
  - AI Agent市场正在快速增长 (0.70)
  - 中小企业AI需求不明确 (0.40)
  - X公司是直接竞争者 (0.60)
  - LLM技术快速迭代 (0.80)
  - 中小企业付费意愿有限 (0.50)
```

### 缺少的信念

- Java/后端市场相关
- 就业市场趋势
- 学习曲线和时间成本
- 个人能力评估

### 修复方案

1. 从真实决策中提取新信念
2. 定期更新 world_model_data.yaml
3. 建立信念衰减机制

### 状态
- [x] 已识别
- [ ] 待扩展

---

## 待记录

（等待更多 World Model 相关问题）

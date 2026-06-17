# Identity Issues
# 记录 Identity 相关的问题和发现

---

## Issue 001: Identity 是"理想中的你"，不是"实际做决策的你"

### 发现日期
2026-06-17

### 症状
- 用户选择 "AI+Java" (保留选择空间)
- PCOS 推荐 "纯AI" (专注)
- 用户实际更重视 career_security 和 optionality

### 证据

| 决策 | 用户选择 | 背后价值观 |
|------|----------|-----------|
| 学习方向 | AI为主+Java补充 | career_security, optionality |
| 是否外包 | 拒绝，专注自有项目 | autonomy, long_term_compounding |
| 技术栈 | Python+FastAPI | market_competitiveness |

### 诊断

当前 Identity 基于用户自述：
```yaml
autonomy: high
creativity: high
influence: high
learning: high
```

实际 Identity 应该基于行为：
```yaml
autonomy: 0.90
learning: 0.90
career_security: 0.85
market_competitiveness: 0.85
economic_resilience: 0.80
creativity: 0.70
influence: 0.60
```

### 修复方案

1. 从决策日志推断 Identity 权重
2. 建立 identity_candidates.yaml 积累证据
3. 10+ 证据后再更新 Identity

### 状态
- [x] 已识别
- [x] 已更新 identity_data.yaml
- [ ] 需要更多证据验证

---

## Issue 002: 缺少 optionality 偏好

### 发现日期
2026-06-17

### 症状
- 用户选择 "AI+Java" 而非 "纯AI"
- 用户拒绝外包但保留技术广度
- 用户似乎偏好"保留选择空间"

### 证据
- Case 001: AI为主+Java补充 > 纯AI
- 用户理由: "多学习一些才能更有竞争力"

### 假设
用户有 `prefer_optionality` 决策模式，倾向于保留更多选择而非押注单一路径。

### 验证方法
观察未来 5+ 个决策是否出现类似模式。

### 状态
- [x] 已识别
- [x] 已添加到 identity_candidates.yaml
- [ ] 需要更多证据验证

---

## 待记录

（等待更多 Identity 相关问题）

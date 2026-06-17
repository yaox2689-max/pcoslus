# PCOS Real Usage Validation

## 开始使用

### 1. 启动 PCOS 服务

```bash
cd D:/pycharm/decision
uv run uvicorn runtime.main:app --port 8001
```

### 2. 运行决策工作流

```bash
# 交互式决策
python decision_workflow.py

# 查看统计
python decision_workflow.py stats

# 查看失配案例
python decision_workflow.py mismatches
```

## 工作流程

```
1. 你有决策问题
       ↓
2. 运行 decision_workflow.py
       ↓
3. 输入问题和背景
       ↓
4. PCOS 给出建议 (含置信度、价值观、信念)
       ↓
5. 你做出最终决定
       ↓
6. 系统记录：PCOS建议 vs 你的选择
       ↓
7. 未来：记录结果，分析失配
```

## 决策类别

- **startup**: 创业方向、市场进入、商业模式
- **product**: 产品功能、优先级、发布策略
- **tech**: 技术栈选择、架构决策、工具选型
- **business**: 客户获取、定价、合作伙伴
- **hiring**: 招聘、合伙人、团队建设
- **career**: 职业发展、学习方向、机会评估
- **investment**: 融资、投资、资源配置

## 目标

### Phase A: 收集 50 个真实决策

每天记录 2-3 个决策：
- 早上：今天要做什么？
- 中午：这个功能要不要加？
- 晚上：这个客户要不要接？

### Phase B: 分析失配案例

当你的选择 ≠ PCOS 建议时，记录：
1. 为什么不同？
2. 是 Identity 错误？(价值观权重不准)
3. 是 World Model 错误？(信念过时)
4. 是 Prompt 错误？(系统理解偏差)

### Phase C: 修正 Identity 和 World Model

根据失配分析，更新：
- `pcos/identity_data.yaml` - 调整价值观、偏好
- `pcos/world_model_data.yaml` - 更新信念、添加新信念

### Phase D: 再次验证

修正后，继续收集决策，计算：
- 一致率提升：78% → 85% → 90%
- 失配案例减少

## 记录格式

### 决策记录 (自动)

```json
{
  "question": "Should I pivot to product?",
  "pcos_recommendation": "Yes, with caution",
  "pcos_confidence": 0.7,
  "actual_decision": "Yes, full pivot",
  "decision_match": false
}
```

### 结果记录 (手动，7天后)

```
outcome_after_7_days: positive
outcome_notes: "Pivot worked, found first customer"
reflection: "PCOS was right about caution, I should have kept some consulting"
```

### 失配分析 (手动)

```
mismatch_case_07:
  question: "Should I accept VC funding?"
  pcos: "No (autonomy conflict)"
  you: "Yes"
  reason: "I valued growth over autonomy more than PCOS thought"
  fix: "Update identity_data.yaml: autonomy weight 0.95 → 0.80"
```

## 什么时候进入下一阶段？

满足以下条件后，进入 Learning Engine：

1. ✅ 真实决策数 > 50
2. ✅ 至少发现 10 个失配案例
3. ✅ identity.yaml 经历 2 轮以上修正

那时你将拥有：
```
Decision → Outcome → Reflection → Identity Evolution
```
的真实数据闭环。

## 示例决策

### 创业类

```
问题: 要不要做 AI Agent 产品?
背景: 目前在做咨询，3个月runway，2个客户
类别: startup
```

### 产品类

```
问题: 要不要加多语言支持?
背景: 当前用户主要是英语用户，中文用户很少
类别: product
```

### 技术类

```
问题: 要不要从 FastAPI 换到 Django?
背景: 项目越来越复杂，需要更好的 ORM
类别: tech
```

### 商业类

```
问题: 要不要接这个大客户?
背景: 他们要定制开发，会占用 80% 时间
类别: business
```

### 招聘类

```
问题: 要不要找技术合伙人?
背景: 我自己做不过来了，需要帮手
类别: hiring
```

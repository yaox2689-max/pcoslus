# PCOS 验证指南

## 1. 快速验证 (5分钟)

### 1.1 启动服务

```bash
cd D:/pycharm/decision
uv run uvicorn runtime.main:app --port 8001
```

### 1.2 测试基础功能

```bash
# 健康检查
curl http://localhost:8001/health

# 测试决策 (会调用 Kimi API)
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I learn Python or Go?"}'
```

**预期结果：**
- 返回 JSON 包含 `thinking_mode`, `recommendation`, `confidence`
- `thinking_mode` 应为 `fast` (简单问题)
- `confidence` 在 0.3-0.95 之间

---

## 2. 功能验证 (15分钟)

### 2.1 测试 Fast vs Slow Thinking

```bash
# Fast Thinking (简单问题)
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I eat lunch now?"}'

# Slow Thinking (复杂问题)
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I pivot my startup from consulting to product?", "context": "3 months runway, 2 customers, competitor raised $5M"}'
```

**验证点：**
- [ ] 简单问题返回 `fast`，复杂问题返回 `slow`
- [ ] `slow` 模式有 3+ 个选项评估
- [ ] `fast` 模式有 1-2 个选项评估

### 2.2 测试价值观对齐

```bash
# 这个决策应该与"自主性"冲突
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I accept VC funding with board seat?", "context": "6 months runway, want to keep control"}'
```

**验证点：**
- [ ] `values_alignment` 包含"自主性"
- [ ] 如果推荐接受融资，应说明与自主性的冲突

### 2.3 测试信念引用

```bash
# 这个决策应该引用"AI Agent市场增长"的信念
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I build an AI Agent product?"}'
```

**验证点：**
- [ ] `beliefs_used` 包含相关信念
- [ ] 信念内容与 `pcos/world_model_data.yaml` 一致

### 2.4 测试 Decision Simulator

```bash
curl -X POST http://localhost:8001/decide/simulate \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I raise funding?", "option": "Raise $500K seed with 20% equity"}'
```

**验证点：**
- [ ] 返回 `alignment` 分数
- [ ] 返回 `conflicts` 列表
- [ ] 返回 `risks` 列表

---

## 3. 数据验证 (10分钟)

### 3.1 检查决策日志

```bash
# 做几个决策后查看日志
curl http://localhost:8001/decide/journal
```

**验证点：**
- [ ] 日志包含 `context_snapshot`
- [ ] 日志包含 `values_used`
- [ ] 日志包含 `beliefs_used`
- [ ] 日志包含 `thinking_mode`

### 3.2 检查执行轨迹

```bash
curl http://localhost:8001/decide/traces
```

**验证点：**
- [ ] 轨迹文件存在于 `runtime/traces/`
- [ ] 轨迹包含 `topics_detected`
- [ ] 轨迹包含 `context_snapshot`

### 3.3 检查 SQLite 数据库

```bash
# 使用 sqlite3 查看数据库
sqlite3 runtime/db/pcos_v2.db

# 查看表结构
.schema decisions

# 查看数据
SELECT id, question, thinking_mode, confidence FROM decisions LIMIT 5;
```

---

## 4. 模型切换验证 (5分钟)

### 4.1 测试模型切换

```bash
# 查看当前模型
curl http://localhost:8001/decide/providers

# 切换到 DeepSeek (需要配置 API Key)
curl -X POST http://localhost:8001/decide/providers/deepseek

# 切换到 Qwen
curl -X POST http://localhost:8001/decide/providers/qwen
```

**验证点：**
- [ ] 切换成功返回新模型信息
- [ ] 切换后决策仍正常工作

---

## 5. 基准测试 (30分钟)

### 5.1 运行基准测试

```bash
# 运行测试
python -m pytest tests/test_benchmark.py -v
```

### 5.2 手动测试 5 个场景

从 `pcos/decision_benchmark.yaml` 选择 5 个场景测试：

```bash
# 场景 S01: 市场进入
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Should I pivot from consulting to product?",
    "context": "3 months runway, 2 customers, competitor raised $5M"
  }'

# 场景 S04: 产品功能
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Which 2 features should I build next?",
    "context": "Options: Multi-language, Custom workflow, Analytics, API integration. Current users are English-speaking."
  }'

# 场景 S07: 资源分配
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How to allocate $10K?",
    "context": "6 months runway, slow user acquisition, need development capacity"
  }'

# 场景 S10: 技术决策
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Which LLM approach should I use?",
    "context": "4-week launch deadline, 100 users, cost-sensitive market. Options: OpenAI API, Open-source LLM, Hybrid"
  }'

# 场景 S20: 融资决策
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Should I accept seed funding?",
    "context": "$500K offer, 20% equity + board seat, 6 months runway, want to keep control"
  }'
```

### 5.3 记录结果

创建 `validation_results.md`：

```markdown
# PCOS 验证结果

## 场景 S01: 市场进入
- Thinking Mode: slow ✅
- Confidence: 0.7
- Values Aligned: 自主性, 创造力, 影响力, 持续学习
- Recommendation: ...
- 评分: ___/10

## 场景 S04: 产品功能
...

## 总结
- 平均 Thinking Mode 准确率: ___%
- 平均 Confidence: ___
- 价值观对齐率: ___%
```

---

## 6. 性能验证 (可选)

### 6.1 响应时间

```bash
# 测量响应时间
time curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I learn Python?"}' \
  --max-time 30
```

**预期：**
- Fast Thinking: < 10 秒
- Slow Thinking: < 30 秒

### 6.2 Token 使用量

检查 Kimi API 的 token 使用情况（如果有 dashboard）。

---

## 7. 边界测试

### 7.1 空问题

```bash
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": ""}'
```

**预期：** 返回 422 或错误信息

### 7.2 超长问题

```bash
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "这是一个非常非常非常长的问题... (1000+ 字)"}'
```

**预期：** 正常返回或超时错误

### 7.3 无效 JSON

```bash
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d 'invalid json'
```

**预期：** 返回 422 错误

---

## 验证清单

### 基础功能
- [ ] 服务启动正常
- [ ] 健康检查通过
- [ ] 决策返回 JSON

### 核心功能
- [ ] Fast Thinking 正确识别
- [ ] Slow Thinking 正确识别
- [ ] 价值观对齐显示
- [ ] 信念引用显示
- [ ] 选项评估完整
- [ ] 推理链清晰

### 数据持久化
- [ ] 决策日志记录
- [ ] 执行轨迹记录
- [ ] SQLite 数据库正常

### 模型切换
- [ ] 切换 API 正常
- [ ] 切换后决策正常

### 边界情况
- [ ] 空问题处理
- [ ] 超长问题处理
- [ ] 无效输入处理

---

## 问题排查

### 问题：API Key 错误

```
LLM API error: Incorrect API key
```

**解决：** 检查 `.env` 中的 API Key 是否正确

### 问题：连接超时

```
LLM API error: Connection error
```

**解决：** 
1. 检查网络连接
2. 检查 API 端点是否可达
3. 尝试切换模型

### 问题：JSON 解析失败

```
Failed to parse Claude response
```

**解决：** 
1. 检查 LLM 返回的内容
2. 尝试切换模型
3. 查看 `runtime/traces/` 中的轨迹

### 问题：数据库错误

```
sqlite3.OperationalError
```

**解决：**
1. 删除 `runtime/db/pcos_v2.db`
2. 重启服务

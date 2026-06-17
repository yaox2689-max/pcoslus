# PCOS Runtime v0.1

Personal Cognitive Operating System - 像人一样思考的数字决策引擎

## 什么是 PCOS？

PCOS 不是一个普通的 AI 助手。它是一个**认知操作系统**：

- **理解你的身份** - 价值观、偏好、决策模式
- **建立世界模型** - 带置信度的信念系统，不是事实数据库
- **混合思考** - 简单决策快速直觉，复杂决策深度分析
- **价值对齐** - 每个决策都与你的核心价值观对齐
- **持续学习** - 从经验中进化，记录决策轨迹

## 架构

```
User Input
    ↓
Context Builder (按话题过滤 beliefs，不全量加载)
    ↓
Prompt Builder (强制 JSON 输出)
    ↓
LLM (DeepSeek / Kimi / Qwen / MIMO)
    ↓
JSON 解析 + Journal + Trace
    ↓
Output
```

## 快速开始

### 1. 安装

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

### 2. 配置

编辑 `.env`：

```bash
# 选择模型
LLM_PROVIDER=kimi

# Kimi (Moonshot)
KIMI_API_KEY=sk-your-key
KIMI_BASE_URL=https://api.moonshot.cn/v1
KIMI_MODEL=moonshot-v1-8k

# DeepSeek
DEEPSEEK_API_KEY=sk-your-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# Qwen (通义千问)
QWEN_API_KEY=sk-your-key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
```

### 3. 启动

```bash
uv run uvicorn runtime.main:app --port 8001
```

### 4. 测试

```bash
# 做决策
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I pivot from consulting to product?", "context": "3 months runway, 2 customers"}'

# 模拟选项
curl -X POST http://localhost:8001/decide/simulate \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I raise funding?", "option": "Raise $500K seed"}'

# 查看决策日志
curl http://localhost:8001/decide/journal

# 查看执行轨迹
curl http://localhost:8001/decide/traces
```

## API 端点

### 决策

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/decide/` | 做一个 PCOS 决策 |
| POST | `/decide/simulate` | 模拟特定选项 |
| GET | `/decide/journal` | 查看决策日志 |
| GET | `/decide/journal/{id}` | 查看特定决策 |

### 模型管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/decide/providers` | 查看当前模型 |
| POST | `/decide/providers/{name}` | 切换模型 |

### 系统

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 服务信息 |
| GET | `/health` | 健康检查 |
| GET | `/decide/traces` | 执行轨迹 |

## 决策输出示例

```json
{
  "thinking_mode": "slow",
  "confidence": 0.7,
  "recommendation": "Proceed with caution towards pivoting to a product-based approach",
  "reasoning_chain": [
    "Pivoting aligns with your value of creativity",
    "Given the fast AI Agent market growth...",
    "However, there is a high risk with limited runway..."
  ],
  "options_evaluated": [
    {
      "option": "remain in consulting",
      "score": {
        "value_alignment": 0.4,
        "belief_support": 0.3,
        "resource_feasibility": 0.8,
        "risk_acceptability": 0.7,
        "learning_potential": 0.5,
        "weighted_total": 0.57
      }
    },
    {
      "option": "pivot to product",
      "score": {
        "value_alignment": 0.8,
        "belief_support": 0.6,
        "resource_feasibility": 0.4,
        "risk_acceptability": 0.35,
        "learning_potential": 0.8,
        "weighted_total": 0.63
      }
    }
  ],
  "values_alignment": [
    "自主性: Making independent choices",
    "创造力: Crafting a new product",
    "影响力: Having a more profound impact",
    "持续学习: Learning through product development"
  ],
  "beliefs_used": [
    "AI Agent market is rapidly growing",
    "SME AI needs are unclear",
    "LLM technology is fast iterating"
  ],
  "key_risks": ["Uncertainty in SME AI demand", "Limited runway"],
  "key_assumptions": ["Pivoting will leverage market growth"]
}
```

## 文件结构

```
decision/
├── pcos/                          # PCOS 配置
│   ├── identity.yaml              # 身份模型 Schema
│   ├── identity_data.yaml         # 用户身份数据
│   ├── world_model.yaml           # 世界模型 Schema
│   ├── world_model_data.yaml      # 信念数据
│   ├── strategy_engine.yaml       # 战略引擎 Schema
│   ├── decision_engine.yaml       # 决策引擎 Schema
│   └── decision_benchmark.yaml    # 27 个测试场景
│
├── runtime/                       # PCOS Runtime
│   ├── config.py                  # 配置加载
│   ├── models.py                  # 数据模型
│   ├── services/
│   │   ├── claude_client.py       # 多模型统一客户端
│   │   ├── context_builder.py     # 话题过滤
│   │   ├── prompt_builder.py      # JSON 强制输出
│   │   ├── decision_journal.py    # 决策日志 (SQLite)
│   │   └── trace_logger.py        # 执行轨迹
│   ├── routers/
│   │   └── decide.py              # API 路由
│   ├── db/
│   │   └── pcos_v2.db             # SQLite 数据库
│   └── traces/                    # 执行轨迹文件
│
├── tests/
│   └── test_benchmark.py          # 基准测试
│
├── pyproject.toml                 # uv 配置
├── .env                           # 环境变量
└── README.md
```

## 设计文档

详细设计文档位于：

- `docs/superpowers/specs/2026-06-17-pcos-design.md` - 完整设计规范
- `pcos/event_flow_trace.md` - 事件流追踪
- `pcos/validation_report.md` - PCOS vs 普通 Claude 对比

## 核心概念

### 1. Identity First

决策首先对齐你的价值观：

```yaml
core_values:
  - 自主性
  - 创造力
  - 影响力
  - 持续学习
```

### 2. Belief System

世界模型存储的是**信念**，不是事实：

```yaml
beliefs:
  - content: "AI Agent market is growing"
    confidence: 0.70
    source: "user_declared"
    evidence: [...]
```

### 3. Mixed Thinking

- **Fast Thinking**: 简单、低风险、有先例 → 1-2 个选项
- **Slow Thinking**: 复杂、高风险、无先例 → 3+ 选项，含情景分析

### 4. Decision Journal

每个决策记录完整中间状态，支持未来 Reflection Engine：

```yaml
context_snapshot: {...}
values_used: [...]
beliefs_used: [...]
thinking_mode: "slow"
decision: "..."
confidence: 0.7
```

## 路线图

### v0.1 (当前)
- ✅ 核心决策引擎
- ✅ 多模型支持 (DeepSeek/Kimi/Qwen/MIMO)
- ✅ 决策日志
- ✅ 执行轨迹

### v0.2
- [ ] 100+ 基准测试
- [ ] Decision Simulator 增强
- [ ] Identity Extraction Pipeline
- [ ] 自动信念衰减

### v0.3
- [ ] Reflection Engine
- [ ] Learning Engine
- [ ] 策略引擎运行时
- [ ] Web UI

### v1.0
- [ ] 多用户支持
- [ ] 云端部署
- [ ] API 文档
- [ ] 插件系统

## License

MIT

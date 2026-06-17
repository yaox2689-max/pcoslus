<div align="center">

# 🧠 PCOS

### Personal Cognitive Operating System

**像人一样思考的数字决策引擎**

[![CI](https://github.com/yaox2689-max/pcos/actions/workflows/ci.yml/badge.svg)](https://github.com/yaox2689-max/pcos/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

[English](#english) · [中文](#中文) · [Documentation](docs/) · [Report Bug](https://github.com/yaox2689-max/pcos/issues/new?template=bug_report.yml) · [Request Feature](https://github.com/yaox2689-max/pcos/issues/new?template=feature_request.yml)

</div>

---

## 中文

### 什么是 PCOS？

PCOS 不是一个普通的 AI 助手。它是一个**认知操作系统**：

- **理解你的身份** - 价值观、偏好、决策模式
- **建立世界模型** - 带置信度的信念系统
- **混合思考** - 简单决策快速直觉，复杂决策深度分析
- **价值对齐** - 每个决策都与你的核心价值观对齐
- **持续学习** - 从经验中进化

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/yaox2689-max/pcos.git
cd pcos

# 2. 安装后端依赖
uv sync

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 4. 启动后端
uv run uvicorn runtime.main:app --port 8001

# 5. 安装前端依赖
cd frontend
npm install

# 6. 启动前端
npm run dev
```

访问 http://localhost:3000

### 示例

```bash
# 做一个决策
curl -X POST http://localhost:8001/decide/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I pivot from consulting to product?"}'
```

响应：
```json
{
  "thinking_mode": "slow",
  "confidence": 0.75,
  "recommendation": "先做咨询，验证市场后再做产品",
  "value_conflicts": {
    "gains": ["持续学习", "影响力"],
    "losses": ["职业安全", "经济韧性"],
    "dominant_conflict": "autonomy_vs_security"
  },
  "counter_argument": {
    "position": "直接做产品可能更快验证市场",
    "reasoning": "..."
  }
}
```

### 支持的模型

| 模型 | 提供商 | 状态 |
|------|--------|------|
| DeepSeek | DeepSeek | ✅ |
| Kimi | Moonshot | ✅ |
| Qwen | 阿里云 | ✅ |
| MIMO | MIMO | ✅ |

### 项目结构

```
pcos/
├── pcos/                    # 配置和 Schema
├── runtime/                 # 后端运行时
├── frontend/                # Next.js 前端
├── research/                # 研究和分析
└── tests/                   # 测试
```

### 文档

- [设计文档](docs/superpowers/specs/2026-06-17-pcos-design.md)
- [验证指南](VALIDATION_GUIDE.md)
- [工作流指南](WORKFLOW_GUIDE.md)
- [API 文档](http://localhost:8001/docs) (运行时访问)

### 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## English

### What is PCOS?

PCOS is not a regular AI assistant. It's a **cognitive operating system**:

- **Understands your identity** - values, preferences, decision patterns
- **Builds a world model** - belief system with confidence scores
- **Mixed thinking** - fast intuition for simple decisions, deep analysis for complex ones
- **Value alignment** - every decision aligns with your core values
- **Continuous learning** - evolves from experience

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yaox2689-max/pcos.git
cd pcos

# 2. Install backend dependencies
uv sync

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# 4. Start backend
uv run uvicorn runtime.main:app --port 8001

# 5. Install frontend dependencies
cd frontend
npm install

# 6. Start frontend
npm run dev
```

Visit http://localhost:3000

### Documentation

- [Design Document](docs/superpowers/specs/2026-06-17-pcos-design.md)
- [Validation Guide](VALIDATION_GUIDE.md)
- [Workflow Guide](WORKFLOW_GUIDE.md)
- [API Docs](http://localhost:8001/docs) (when running)

### Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ by the PCOS community**

</div>

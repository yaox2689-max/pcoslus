'use client';

interface Props {
  data: {
    decision_id: string;
    thinking_mode: string;
    recommendation: string;
    confidence: number;
    reasoning_chain: string[];
    options_evaluated: Array<{
      option: string;
      score: {
        value_alignment: number;
        belief_support: number;
        resource_feasibility: number;
        risk_acceptability: number;
        learning_potential: number;
        weighted_total: number;
      };
    }>;
    value_conflicts: {
      gains: string[];
      losses: string[];
      net_alignment: number;
      severity: number;
      dominant_conflict: string;
    };
    counter_argument: { position: string; reasoning: string };
    key_risks: string[];
    key_assumptions: string[];
    beliefs_used: string[];
  };
}

function ScoreBar({ label, value, emoji }: { label: string; value: number; emoji: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-kawaii-text-light">{emoji} {label}</span>
        <span className="font-bold text-primary-dark">{Math.round(value * 100)}%</span>
      </div>
      <div className="score-bar">
        <div className="score-bar-fill" style={{ width: `${value * 100}%` }} />
      </div>
    </div>
  );
}

export default function DecisionResult({ data }: Props) {
  const confColor = data.confidence > 0.7 ? 'bg-accent text-green-700' : data.confidence > 0.4 ? 'bg-secondary text-orange-700' : 'bg-red-100 text-red-600';

  return (
    <div className="space-y-6">
      {/* Main Recommendation */}
      <div className="kawaii-card p-6 md:p-8">
        <div className="flex items-center gap-3 mb-5">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-primary-light flex items-center justify-center text-2xl shadow-kawaii-sm">
            💡
          </div>
          <div>
            <h2 className="font-display text-xl text-primary-dark">我的建议</h2>
            <div className="flex items-center gap-2 mt-1">
              <span className={`badge-kawaii ${confColor}`}>
                置信度 {Math.round(data.confidence * 100)}%
              </span>
              <span className="badge-kawaii bg-primary/10 text-primary-dark">
                {data.thinking_mode === 'slow' ? '🧠 深度思考' : '⚡ 快速判断'}
              </span>
            </div>
          </div>
        </div>

        <p className="text-lg md:text-xl font-display text-kawaii-text leading-relaxed mb-6">
          {data.recommendation}
        </p>

        {/* Reasoning */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-kawaii-text flex items-center gap-2">
            🎯 推理过程
          </h3>
          <div className="space-y-2">
            {data.reasoning_chain.map((r, i) => (
              <div key={i} className="flex gap-3 text-sm text-kawaii-text animate-slide-up" style={{ animationDelay: `${i * 0.1}s` }}>
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold text-primary-dark">
                  {i + 1}
                </span>
                <span className="leading-relaxed">{r}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Value Conflicts */}
      <div className="kawaii-card p-6">
        <h3 className="font-bold text-kawaii-text flex items-center gap-2 mb-5">
          ⚖️ 价值观权衡
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-lg">💚</span>
              <span className="text-sm font-bold text-green-700">会增强的价值观</span>
            </div>
            <div className="space-y-2">
              {data.value_conflicts.gains.map((g, i) => (
                <div key={i} className="flex items-center gap-2 px-4 py-2 bg-accent/30 rounded-[15px] text-sm text-green-800">
                  <span className="w-2 h-2 rounded-full bg-green-400" />
                  {g}
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-lg">🧡</span>
              <span className="text-sm font-bold text-orange-700">会削弱的价值观</span>
            </div>
            <div className="space-y-2">
              {data.value_conflicts.losses.map((l, i) => (
                <div key={i} className="flex items-center gap-2 px-4 py-2 bg-secondary/30 rounded-[15px] text-sm text-orange-800">
                  <span className="w-2 h-2 rounded-full bg-orange-400" />
                  {l}
                </div>
              ))}
            </div>
          </div>
        </div>

        {data.value_conflicts.dominant_conflict && (
          <div className="mt-4 p-4 bg-primary/5 rounded-[15px] border border-primary/10">
            <p className="text-sm text-kawaii-text">
              <span className="font-bold">核心冲突：</span>
              {data.value_conflicts.dominant_conflict.replace(/_/g, ' vs ')}
            </p>
          </div>
        )}
      </div>

      {/* Counter Argument */}
      <div className="kawaii-card p-6">
        <h3 className="font-bold text-kawaii-text flex items-center gap-2 mb-4">
          🤔 反方观点
        </h3>
        <div className="bg-secondary/20 rounded-[15px] p-4 border border-secondary/30">
          <p className="font-bold text-kawaii-text mb-2">{data.counter_argument.position}</p>
          <p className="text-sm text-kawaii-text-light leading-relaxed">{data.counter_argument.reasoning}</p>
        </div>
      </div>

      {/* Options */}
      {data.options_evaluated.length > 0 && (
        <div className="kawaii-card p-6">
          <h3 className="font-bold text-kawaii-text flex items-center gap-2 mb-5">
            📊 选项评估
          </h3>
          <div className="space-y-4">
            {data.options_evaluated.map((opt, i) => (
              <div key={i} className="p-4 bg-primary/5 rounded-[15px] border border-primary/10">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-bold text-kawaii-text">{opt.option}</h4>
                  <span className="font-display text-xl text-primary-dark">{Math.round(opt.score.weighted_total * 100)}分</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
                  <ScoreBar label="价值观" value={opt.score.value_alignment} emoji="💎" />
                  <ScoreBar label="信念" value={opt.score.belief_support} emoji="🧠" />
                  <ScoreBar label="资源" value={opt.score.resource_feasibility} emoji="📦" />
                  <ScoreBar label="风险" value={opt.score.risk_acceptability} emoji="🛡️" />
                  <ScoreBar label="学习" value={opt.score.learning_potential} emoji="📚" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Risks & Assumptions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="kawaii-card p-6">
          <h3 className="font-bold text-kawaii-text flex items-center gap-2 mb-4">
            ⚠️ 风险提示
          </h3>
          <ul className="space-y-2">
            {data.key_risks.map((r, i) => (
              <li key={i} className="flex gap-2 text-sm text-kawaii-text">
                <span className="text-red-400">●</span>{r}
              </li>
            ))}
          </ul>
        </div>

        <div className="kawaii-card p-6">
          <h3 className="font-bold text-kawaii-text flex items-center gap-2 mb-4">
            🎯 关键假设
          </h3>
          <ul className="space-y-2">
            {data.key_assumptions.map((a, i) => (
              <li key={i} className="flex gap-2 text-sm text-kawaii-text">
                <span className="text-primary">●</span>{a}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

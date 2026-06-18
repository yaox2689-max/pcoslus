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

function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div className="space-y-1.5">
      <div className="flex justify-between text-xs">
        <span className="text-ink-muted">{label}</span>
        <span className="font-semibold text-ink">{Math.round(value * 100)}%</span>
      </div>
      <div className="score-bar">
        <div className="score-bar-fill" style={{ width: `${value * 100}%` }} />
      </div>
    </div>
  );
}

export default function DecisionResult({ data }: Props) {
  return (
    <div className="space-y-8">
      {/* Recommendation */}
      <div className="card !p-8">
        <div className="flex items-start gap-4 mb-6">
          <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center flex-shrink-0">
            <svg className="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-3 flex-wrap mb-3">
              <h2 className="font-heading text-xl font-bold text-ink">分析结论</h2>
              <span className={`pill ${data.confidence > 0.7 ? '!bg-emerald-500/10 !text-emerald-700' : data.confidence > 0.4 ? '!bg-amber-500/10 !text-amber-700' : '!bg-red-500/10 !text-red-600'}`}>
                置信度 {Math.round(data.confidence * 100)}%
              </span>
              <span className="pill">{data.thinking_mode === 'slow' ? '深度分析' : '快速判断'}</span>
            </div>
            <p className="text-lg font-heading text-ink leading-relaxed">{data.recommendation}</p>
          </div>
        </div>

        {/* Reasoning */}
        <div className="border-t border-border-light pt-6">
          <h3 className="font-heading font-semibold text-ink mb-4 flex items-center gap-2">
            <span className="w-6 h-6 rounded-lg bg-secondary/20 flex items-center justify-center text-xs font-bold text-secondary">R</span>
            推理链
          </h3>
          <ol className="space-y-3">
            {data.reasoning_chain.map((r, i) => (
              <li key={i} className="flex gap-4 text-sm text-ink-light animate-fade-up" style={{ animationDelay: `${i * 0.08}s` }}>
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-surface-alt flex items-center justify-center text-xs font-bold text-ink-muted">{i + 1}</span>
                <span className="leading-relaxed pt-0.5">{r}</span>
              </li>
            ))}
          </ol>
        </div>
      </div>

      {/* Value Conflicts */}
      <div className="card !p-8">
        <h3 className="font-heading font-bold text-ink mb-6 flex items-center gap-2">
          <span className="w-7 h-7 rounded-lg bg-accent/20 flex items-center justify-center">
            <svg className="w-4 h-4 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M12 3v18M3 12h18"/></svg>
          </span>
          价值观权衡
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-xs font-semibold text-emerald-700 uppercase tracking-wider mb-3">增强</p>
            <div className="space-y-2">
              {data.value_conflicts.gains.map((g, i) => (
                <div key={i} className="flex items-center gap-3 px-4 py-2.5 bg-emerald-500/5 rounded-xl text-sm text-ink">
                  <span className="w-2 h-2 rounded-full bg-emerald-400" />{g}
                </div>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs font-semibold text-amber-700 uppercase tracking-wider mb-3">削弱</p>
            <div className="space-y-2">
              {data.value_conflicts.losses.map((l, i) => (
                <div key={i} className="flex items-center gap-3 px-4 py-2.5 bg-amber-500/5 rounded-xl text-sm text-ink">
                  <span className="w-2 h-2 rounded-full bg-amber-400" />{l}
                </div>
              ))}
            </div>
          </div>
        </div>
        {data.value_conflicts.dominant_conflict && (
          <div className="mt-5 p-4 bg-surface-alt rounded-xl">
            <p className="text-sm text-ink-muted">
              <span className="font-semibold text-ink">核心冲突：</span>
              {data.value_conflicts.dominant_conflict.replace(/_/g, ' vs ')}
            </p>
          </div>
        )}
      </div>

      {/* Counter Argument */}
      <div className="card !p-8">
        <h3 className="font-heading font-bold text-ink mb-4 flex items-center gap-2">
          <span className="w-7 h-7 rounded-lg bg-accent/20 flex items-center justify-center">
            <svg className="w-4 h-4 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          </span>
          反方观点
        </h3>
        <div className="bg-surface-alt rounded-xl p-5 border border-border-light">
          <p className="font-heading font-semibold text-ink mb-2">{data.counter_argument.position}</p>
          <p className="text-sm text-ink-light leading-relaxed">{data.counter_argument.reasoning}</p>
        </div>
      </div>

      {/* Options */}
      {data.options_evaluated.length > 0 && (
        <div className="card !p-8">
          <h3 className="font-heading font-bold text-ink mb-6 flex items-center gap-2">
            <span className="w-7 h-7 rounded-lg bg-primary/10 flex items-center justify-center">
              <svg className="w-4 h-4 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            </span>
            选项评估
          </h3>
          <div className="space-y-5">
            {data.options_evaluated.map((opt, i) => (
              <div key={i} className="p-5 bg-surface-alt rounded-xl border border-border-light transition-all hover:border-primary/30">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-heading font-semibold text-ink">{opt.option}</h4>
                  <span className="font-heading text-2xl font-bold text-primary">{Math.round(opt.score.weighted_total * 100)}</span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <ScoreBar label="价值观" value={opt.score.value_alignment} />
                  <ScoreBar label="信念" value={opt.score.belief_support} />
                  <ScoreBar label="资源" value={opt.score.resource_feasibility} />
                  <ScoreBar label="风险" value={opt.score.risk_acceptability} />
                  <ScoreBar label="学习" value={opt.score.learning_potential} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Risks & Assumptions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card !p-8">
          <h3 className="font-heading font-bold text-ink mb-4 flex items-center gap-2">
            <span className="w-6 h-6 rounded-lg bg-red-500/10 flex items-center justify-center text-xs text-red-500">!</span>
            风险提示
          </h3>
          <ul className="space-y-2.5">
            {data.key_risks.map((r, i) => <li key={i} className="flex gap-3 text-sm text-ink-light"><span className="text-red-400 mt-0.5">●</span>{r}</li>)}
          </ul>
        </div>
        <div className="card !p-8">
          <h3 className="font-heading font-bold text-ink mb-4 flex items-center gap-2">
            <span className="w-6 h-6 rounded-lg bg-primary/10 flex items-center justify-center text-xs text-primary">A</span>
            关键假设
          </h3>
          <ul className="space-y-2.5">
            {data.key_assumptions.map((a, i) => <li key={i} className="flex gap-3 text-sm text-ink-light"><span className="text-primary mt-0.5">●</span>{a}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
}

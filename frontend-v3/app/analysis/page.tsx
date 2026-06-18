'use client';

import Sidebar from '@/components/Sidebar';

const values = [
  { name: '自主性', value: 0.90 },
  { name: '持续学习', value: 0.90 },
  { name: '职业安全', value: 0.85 },
  { name: '市场竞争力', value: 0.85 },
  { name: '经济韧性', value: 0.80 },
  { name: '创造力', value: 0.70 },
  { name: '影响力', value: 0.60 },
];

const patterns = [
  { name: '偏好可选性', desc: '保留更多选择空间', conf: 0.85 },
  { name: '避免二选一', desc: '寻找组合策略', conf: 0.80 },
  { name: '数据优先', desc: '用真实数据验证假设', conf: 0.85 },
  { name: '对冲不确定性', desc: '面对不确定时对冲风险', conf: 0.75 },
  { name: '长期复利', desc: '偏好长期收益', conf: 0.75 },
  { name: '风险可控增长', desc: '愿意冒险但需安全网', conf: 0.70 },
];

export default function AnalysisPage() {
  return (
    <main className="min-h-screen">
      <Sidebar />
      <div className="md:ml-[280px] pt-14 md:pt-0 p-4 md:p-10 pb-24 md:pb-10">
        <div className="max-w-[960px] mx-auto">
          <div className="mb-10">
            <h1 className="font-heading text-3xl md:text-4xl font-bold text-ink tracking-tight mb-2">洞察</h1>
            <p className="text-ink-light text-lg">理解你的价值观分布与决策模式</p>
          </div>

          {/* Values */}
          <div className="card !p-8 mb-8">
            <h2 className="font-heading text-xl font-bold text-ink mb-6">价值观画像</h2>
            <div className="space-y-5">
              {values.map((v, i) => (
                <div key={v.name}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-semibold text-ink">{v.name}</span>
                    <span className="text-sm font-bold text-primary">{Math.round(v.value * 100)}%</span>
                  </div>
                  <div className="h-2 bg-surface-alt rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-primary to-accent transition-all duration-1000" style={{ width: `${v.value * 100}%`, transitionDelay: `${i * 0.1}s` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Patterns */}
          <div className="card !p-8 mb-8">
            <h2 className="font-heading text-xl font-bold text-ink mb-6">决策模式</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {patterns.map(p => (
                <div key={p.name} className="p-5 bg-surface-alt rounded-xl border border-border-light transition-all hover:border-primary/30">
                  <h3 className="font-heading font-semibold text-ink text-sm mb-1">{p.name}</h3>
                  <p className="text-xs text-ink-muted mb-3">{p.desc}</p>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-1.5 bg-border-light rounded-full overflow-hidden">
                      <div className="h-full bg-primary rounded-full" style={{ width: `${p.conf * 100}%` }} />
                    </div>
                    <span className="text-xs text-ink-muted">{Math.round(p.conf * 100)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Insights */}
          <div className="card !p-8">
            <h2 className="font-heading text-xl font-bold text-ink mb-6">关键洞察</h2>
            <div className="space-y-4">
              <div className="p-5 bg-emerald-500/5 rounded-xl border border-emerald-500/10">
                <h4 className="font-heading font-semibold text-emerald-800 mb-1">优势</h4>
                <p className="text-sm text-emerald-700">你的决策高度对齐&ldquo;持续学习&rdquo;和&ldquo;自主性&rdquo;——你是一个注重成长和独立思考的人。</p>
              </div>
              <div className="p-5 bg-amber-500/5 rounded-xl border border-amber-500/10">
                <h4 className="font-heading font-semibold text-amber-800 mb-1">注意</h4>
                <p className="text-sm text-amber-700">&ldquo;影响力&rdquo;得分较低（60%）。如果目标是扩大影响，决策中需要更多考虑这个维度。</p>
              </div>
              <div className="p-5 bg-primary/5 rounded-xl border border-primary/10">
                <h4 className="font-heading font-semibold text-primary-dark mb-1">发现</h4>
                <p className="text-sm text-ink-light">你有强烈的&ldquo;数据优先&rdquo;倾向——在创业者中少见，说明你更可能做出基于证据的决策。</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

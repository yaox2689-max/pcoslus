'use client';

import Sidebar from '@/components/Sidebar';

const values = [
  { name: '自主性', value: 0.90, emoji: '🦅' },
  { name: '持续学习', value: 0.90, emoji: '📚' },
  { name: '职业安全', value: 0.85, emoji: '🛡️' },
  { name: '市场竞争力', value: 0.85, emoji: '⚔️' },
  { name: '经济韧性', value: 0.80, emoji: '💰' },
  { name: '创造力', value: 0.70, emoji: '🎨' },
  { name: '影响力', value: 0.60, emoji: '🌟' },
];

const patterns = [
  { name: '偏好可选性', desc: '倾向于保留更多选择空间', conf: 0.85, emoji: '🔀' },
  { name: '避免二选一', desc: '寻找组合策略，而非非此即彼', conf: 0.80, emoji: '🤝' },
  { name: '数据优先', desc: '优先获取真实数据验证假设', conf: 0.85, emoji: '📊' },
  { name: '对冲不确定性', desc: '面对不确定时倾向对冲风险', conf: 0.75, emoji: '🛡️' },
  { name: '长期复利', desc: '偏好长期收益而非短期回报', conf: 0.75, emoji: '📈' },
  { name: '风险可控增长', desc: '愿意冒险但需要安全网', conf: 0.70, emoji: '🎯' },
];

export default function AnalysisPage() {
  return (
    <main className="min-h-screen">
      <Sidebar />
      <div className="md:ml-[260px] p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-3xl mx-auto">
          <div className="mb-8 animate-fade-in">
            <h1 className="font-display text-3xl md:text-4xl text-primary-dark mb-2">🔮 洞察分析</h1>
            <p className="text-kawaii-text-light">了解你的决策模式和价值观分布~</p>
          </div>

          {/* Value Radar */}
          <div className="kawaii-card p-6 mb-6 animate-slide-up stagger-1">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">💎</span>
              <div>
                <h2 className="font-display text-xl text-primary-dark">价值观画像</h2>
                <p className="text-sm text-kawaii-text-light">基于你的决策行为推断</p>
              </div>
            </div>
            <div className="space-y-4">
              {values.map((v, i) => (
                <div key={v.name} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-kawaii-text">{v.emoji} {v.name}</span>
                    <span className="text-sm font-bold text-primary-dark">{Math.round(v.value * 100)}%</span>
                  </div>
                  <div className="h-3 bg-primary/10 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-primary to-primary-light transition-all duration-1000"
                      style={{ width: `${v.value * 100}%`, animationDelay: `${i * 0.1}s` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Decision Patterns */}
          <div className="kawaii-card p-6 mb-6 animate-slide-up stagger-2">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">🧩</span>
              <div>
                <h2 className="font-display text-xl text-primary-dark">决策模式</h2>
                <p className="text-sm text-kawaii-text-light">你倾向于这样思考问题</p>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {patterns.map(p => (
                <div key={p.name} className="p-4 bg-primary/5 rounded-[15px] border border-primary/10 transition-all hover:shadow-kawaii-sm">
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{p.emoji}</span>
                    <div className="flex-1">
                      <h3 className="font-bold text-kawaii-text text-sm">{p.name}</h3>
                      <p className="text-xs text-kawaii-text-light mt-1">{p.desc}</p>
                      <div className="mt-2 flex items-center gap-2">
                        <div className="flex-1 h-2 bg-primary/10 rounded-full overflow-hidden">
                          <div className="h-full bg-primary rounded-full" style={{ width: `${p.conf * 100}%` }} />
                        </div>
                        <span className="text-xs text-kawaii-text-light">{Math.round(p.conf * 100)}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Insights */}
          <div className="kawaii-card p-6 animate-slide-up stagger-3">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">💡</span>
              <div>
                <h2 className="font-display text-xl text-primary-dark">关键洞察</h2>
                <p className="text-sm text-kawaii-text-light">从你的决策中发现</p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="p-4 bg-accent/30 rounded-[15px] border border-accent">
                <h4 className="font-bold text-green-800 mb-1">✅ 优势</h4>
                <p className="text-sm text-green-700">
                  你的决策高度对齐&ldquo;持续学习&rdquo;和&ldquo;自主性&rdquo;价值观，说明你是一个注重成长和独立思考的人~
                </p>
              </div>
              <div className="p-4 bg-secondary/30 rounded-[15px] border border-secondary/30">
                <h4 className="font-bold text-orange-800 mb-1">⚠️ 注意</h4>
                <p className="text-sm text-orange-700">
                  &ldquo;影响力&rdquo;得分较低（60%），如果目标是扩大影响，可能需要在决策中更多考虑这个维度哦
                </p>
              </div>
              <div className="p-4 bg-primary/5 rounded-[15px] border border-primary/10">
                <h4 className="font-bold text-primary-dark mb-1">💡 发现</h4>
                <p className="text-sm text-kawaii-text">
                  你有强烈的&ldquo;数据优先&rdquo;倾向，这在创业者中很少见。这意味着你更可能做出基于证据的决策~
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

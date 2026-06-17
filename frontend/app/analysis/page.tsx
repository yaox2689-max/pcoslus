'use client';

import Navigation from '@/components/Navigation';
import { TrendingUp, PieChart, Activity, Target } from 'lucide-react';

export default function AnalysisPage() {
  // Mock data for visualization
  const valueData = [
    { name: '自主性', current: 0.90, target: 0.95 },
    { name: '持续学习', current: 0.90, target: 0.90 },
    { name: '职业安全', current: 0.85, target: 0.80 },
    { name: '市场竞争力', current: 0.85, target: 0.85 },
    { name: '经济韧性', current: 0.80, target: 0.80 },
    { name: '创造力', current: 0.70, target: 0.75 },
    { name: '影响力', current: 0.60, target: 0.70 },
  ];

  const patterns = [
    { name: '偏好可选性', description: '倾向于保留更多选择空间', confidence: 0.85, icon: '🔀' },
    { name: '避免二选一', description: '寻找组合策略，而非非此即彼', confidence: 0.80, icon: '🤝' },
    { name: '对冲不确定性', description: '面对不确定时倾向对冲风险', confidence: 0.75, icon: '🛡️' },
    { name: '长期复利', description: '偏好长期收益而非短期回报', confidence: 0.75, icon: '📈' },
    { name: '风险可控增长', description: '愿意冒险但需要安全网', confidence: 0.70, icon: '🎯' },
    { name: '数据优先', description: '优先获取真实数据验证假设', confidence: 0.85, icon: '📊' },
  ];

  return (
    <main className="min-h-screen">
      <Navigation />

      <div className="md:ml-64 p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in">
            <h1 className="font-serif text-3xl md:text-4xl font-bold text-warm-800 mb-2">
              洞察分析
            </h1>
            <p className="text-warm-500 text-lg">
              了解你的决策模式和价值观分布
            </p>
          </div>

          {/* Value Radar (simplified as bars) */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6 mb-6 animate-fade-in stagger-1">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-sage-100 flex items-center justify-center">
                <Target className="w-5 h-5 text-sage-600" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-warm-800">价值观画像</h2>
                <p className="text-sm text-warm-500">基于你的决策行为推断</p>
              </div>
            </div>

            <div className="space-y-4">
              {valueData.map((value, index) => (
                <div key={value.name} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-warm-700">{value.name}</span>
                    <span className="text-sm text-warm-500">{Math.round(value.current * 100)}%</span>
                  </div>
                  <div className="relative h-3 bg-warm-100 rounded-full overflow-hidden">
                    <div
                      className="absolute inset-y-0 left-0 bg-gradient-to-r from-warm-400 to-warm-500 rounded-full transition-all duration-1000"
                      style={{ width: `${value.current * 100}%`, animationDelay: `${index * 0.1}s` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Decision Patterns */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6 mb-6 animate-fade-in stagger-2">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-warm-100 flex items-center justify-center">
                <Activity className="w-5 h-5 text-warm-600" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-warm-800">决策模式</h2>
                <p className="text-sm text-warm-500">你倾向于这样思考问题</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {patterns.map((pattern, index) => (
                <div
                  key={pattern.name}
                  className="p-4 bg-warm-50/50 rounded-xl border border-warm-100 card-hover"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{pattern.icon}</span>
                    <div>
                      <h3 className="font-medium text-warm-800">{pattern.name}</h3>
                      <p className="text-sm text-warm-500 mt-1">{pattern.description}</p>
                      <div className="mt-2 flex items-center gap-2">
                        <div className="flex-1 h-1.5 bg-warm-100 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-warm-400 rounded-full"
                            style={{ width: `${pattern.confidence * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-warm-400">{Math.round(pattern.confidence * 100)}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Key Insights */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6 animate-fade-in stagger-3">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-cream-200 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-warm-600" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-warm-800">关键洞察</h2>
                <p className="text-sm text-warm-500">从你的决策中发现</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="p-4 bg-sage-50 rounded-xl border border-sage-100">
                <h4 className="font-medium text-sage-800 mb-1">✅ 优势</h4>
                <p className="text-sm text-sage-700">
                  你的决策高度对齐"持续学习"和"自主性"价值观，这说明你是一个注重成长和独立思考的人。
                </p>
              </div>

              <div className="p-4 bg-warm-50 rounded-xl border border-warm-100">
                <h4 className="font-medium text-warm-800 mb-1">⚠️ 注意</h4>
                <p className="text-sm text-warm-700">
                  "影响力"得分较低（60%），如果你的目标是扩大影响，可能需要在决策中更多考虑这个维度。
                </p>
              </div>

              <div className="p-4 bg-cream-100 rounded-xl border border-cream-200">
                <h4 className="font-medium text-warm-800 mb-1">💡 发现</h4>
                <p className="text-sm text-warm-700">
                  你有强烈的"数据优先"倾向，这在创业者中很少见。这意味着你更可能做出基于证据的决策，而非直觉。
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

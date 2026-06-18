'use client';

import { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';

interface Decision {
  id: string;
  timestamp: string;
  question: string;
  thinking_mode: string;
  confidence: number;
  decision: string;
}

export default function HistoryPage() {
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch('/api/decide/journal?limit=50')
      .then(r => r.json())
      .then(setDecisions)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const formatDate = (ts: string) => {
    const d = new Date(ts);
    return d.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  const getConfBadge = (c: number) => {
    if (c > 0.7) return 'bg-accent text-green-700';
    if (c > 0.4) return 'bg-secondary text-orange-700';
    return 'bg-red-100 text-red-600';
  };

  return (
    <main className="min-h-screen">
      <Sidebar />
      <div className="md:ml-[260px] p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in">
            <h1 className="font-display text-3xl md:text-4xl text-primary-dark mb-2">📖 回忆录</h1>
            <p className="text-kawaii-text-light">回顾过去的决定，看看你的成长轨迹~</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="kawaii-card p-5 text-center animate-slide-up stagger-1">
              <p className="font-display text-3xl text-primary-dark">{decisions.length}</p>
              <p className="text-xs text-kawaii-text-light mt-1">总决策数</p>
            </div>
            <div className="kawaii-card p-5 text-center animate-slide-up stagger-2">
              <p className="font-display text-3xl text-green-600">{decisions.filter(d => d.confidence > 0.7).length}</p>
              <p className="text-xs text-kawaii-text-light mt-1">高置信度</p>
            </div>
            <div className="kawaii-card p-5 text-center animate-slide-up stagger-3">
              <p className="font-display text-3xl text-orange-600">{decisions.filter(d => d.thinking_mode === 'slow').length}</p>
              <p className="text-xs text-kawaii-text-light mt-1">深度思考</p>
            </div>
          </div>

          {/* Filter */}
          <div className="flex gap-2 mb-6">
            {['all', 'slow', 'fast'].map(m => (
              <button
                key={m}
                onClick={() => setFilter(m)}
                className={`px-5 py-2 rounded-full text-sm font-bold transition-all ${
                  filter === m
                    ? 'bg-gradient-to-r from-primary to-primary-light text-white shadow-kawaii-sm'
                    : 'bg-white/60 text-kawaii-text hover:bg-primary/10'
                }`}
              >
                {m === 'all' ? '全部' : m === 'slow' ? '🧠 深度思考' : '⚡ 快速判断'}
              </button>
            ))}
          </div>

          {/* List */}
          {loading ? (
            <div className="text-center py-16">
              <div className="flex justify-center gap-2 mb-4">
                <div className="thinking-dot" />
                <div className="thinking-dot" />
                <div className="thinking-dot" />
              </div>
              <p className="text-kawaii-text-light">加载中...</p>
            </div>
          ) : decisions.length === 0 ? (
            <div className="kawaii-card p-12 text-center">
              <span className="text-5xl block mb-4">📝</span>
              <p className="text-kawaii-text font-bold">还没有决策记录</p>
              <p className="text-kawaii-text-light text-sm mt-1">去做你的第一个决定吧~</p>
            </div>
          ) : (
            <div className="space-y-4">
              {decisions
                .filter(d => filter === 'all' || d.thinking_mode === filter)
                .map((d, i) => (
                  <div key={d.id} className="kawaii-card p-5 animate-slide-up" style={{ animationDelay: `${i * 0.05}s` }}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-display text-lg text-kawaii-text mb-2">{d.question}</p>
                        <p className="text-sm text-kawaii-text-light line-clamp-2 mb-3">{d.decision}</p>
                        <div className="flex items-center gap-3 flex-wrap">
                          <span className="text-xs text-kawaii-text-light">{formatDate(d.timestamp)}</span>
                          <span className={`badge-kawaii ${getConfBadge(d.confidence)}`}>
                            {Math.round(d.confidence * 100)}%
                          </span>
                          <span className="badge-kawaii bg-primary/10 text-primary-dark text-xs">
                            {d.thinking_mode === 'slow' ? '🧠 深度' : '⚡ 快速'}
                          </span>
                        </div>
                      </div>
                      <span className="text-2xl ml-4">→</span>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

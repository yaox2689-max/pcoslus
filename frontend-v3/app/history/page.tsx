'use client';

import { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';

interface Decision { id: string; timestamp: string; question: string; thinking_mode: string; confidence: number; decision: string; }

export default function HistoryPage() {
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch('/api/decide/journal?limit=50').then(r => r.json()).then(setDecisions).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const fmt = (ts: string) => new Date(ts).toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  return (
    <main className="min-h-screen">
      <Sidebar />
      <div className="md:ml-[280px] pt-14 md:pt-0 p-4 md:p-10 pb-24 md:pb-10">
        <div className="max-w-[960px] mx-auto">
          <div className="mb-10">
            <h1 className="font-heading text-3xl md:text-4xl font-bold text-ink tracking-tight mb-2">回顾</h1>
            <p className="text-ink-light text-lg">审视过去的决定，发现你的决策规律</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 mb-8">
            {[
              { label: '总决策', value: decisions.length, color: 'text-ink' },
              { label: '高置信', value: decisions.filter(d => d.confidence > 0.7).length, color: 'text-emerald-600' },
              { label: '深度分析', value: decisions.filter(d => d.thinking_mode === 'slow').length, color: 'text-primary' },
            ].map(s => (
              <div key={s.label} className="card text-center">
                <p className={`font-heading text-3xl font-bold ${s.color}`}>{s.value}</p>
                <p className="text-xs text-ink-muted mt-1">{s.label}</p>
              </div>
            ))}
          </div>

          {/* Filter */}
          <div className="flex gap-2 mb-6">
            {[{v:'all',l:'全部'},{v:'slow',l:'深度分析'},{v:'fast',l:'快速判断'}].map(f => (
              <button key={f.v} onClick={() => setFilter(f.v)} className={filter === f.v ? 'btn--primary !py-2 !px-5 !text-xs' : 'btn--secondary !py-2 !px-5 !text-xs'}>{f.l}</button>
            ))}
          </div>

          {/* List */}
          {loading ? (
            <div className="text-center py-20"><div className="flex justify-center gap-2 mb-4"><div className="typing-dot"/><div className="typing-dot"/><div className="typing-dot"/></div><p className="text-ink-muted">加载中...</p></div>
          ) : decisions.length === 0 ? (
            <div className="card text-center py-16"><p className="text-4xl mb-4">📋</p><p className="font-heading font-semibold text-ink">还没有决策记录</p><p className="text-ink-muted text-sm mt-1">去做你的第一个决定吧</p></div>
          ) : (
            <div className="space-y-4">
              {decisions.filter(d => filter === 'all' || d.thinking_mode === filter).map((d, i) => (
                <div key={d.id} className="card group" style={{ animationDelay: `${i * 0.05}s` }}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-heading font-semibold text-ink mb-2">{d.question}</p>
                      <p className="text-sm text-ink-light line-clamp-2 mb-3">{d.decision}</p>
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="text-xs text-ink-muted">{fmt(d.timestamp)}</span>
                        <span className={`pill ${d.confidence > 0.7 ? '!bg-emerald-500/10 !text-emerald-700' : d.confidence > 0.4 ? '!bg-amber-500/10 !text-amber-700' : '!bg-red-500/10 !text-red-600'}`}>{Math.round(d.confidence * 100)}%</span>
                        <span className="pill">{d.thinking_mode === 'slow' ? '深度' : '快速'}</span>
                      </div>
                    </div>
                    <svg className="w-5 h-5 text-ink-muted group-hover:text-primary transition-colors mt-1 ml-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><polyline points="9 18 15 12 9 6"/></svg>
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

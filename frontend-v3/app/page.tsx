'use client';

import { useState, useEffect, useRef } from 'react';
import Sidebar from '@/components/Sidebar';
import DecisionForm from '@/components/DecisionForm';
import DecisionResult from '@/components/DecisionResult';
import RecordDecision from '@/components/RecordDecision';

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');

  // Scroll reveal observer
  useEffect(() => {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
    }, { threshold: 0.1, rootMargin: '-60px' });
    document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
    return () => obs.disconnect();
  }, [result]);

  return (
    <main className="min-h-screen">
      <Sidebar />
      <div className="md:ml-[280px] pt-14 md:pt-0 p-4 md:p-10 pb-24 md:pb-10">
        <div className="max-w-[960px] mx-auto">
          {/* Hero */}
          {!result && !loading && (
            <div className="reveal visible py-16 md:py-24 text-center">
              <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl font-bold text-ink tracking-tight mb-4" style={{ lineHeight: '1.2' }}>
                今天，有什么<br />
                <span className="text-primary">重要的决定</span>要做？
              </h1>
              <p className="text-ink-light text-lg md:text-xl max-w-xl mx-auto mt-6 leading-relaxed">
                把你的困惑告诉我。我会用你的价值观、信念和过往经验，帮你理清思路。
              </p>
            </div>
          )}

          {/* Form */}
          <div className="reveal visible">
            <DecisionForm
              onResult={(data, q) => { setResult(data); setQuestion(q); }}
              setLoading={setLoading}
              loading={loading}
            />
          </div>

          {/* Loading */}
          {loading && (
            <div className="card p-10 mt-8 text-center animate-bubble-in">
              <div className="flex justify-center gap-2 mb-5">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
              <p className="font-heading font-semibold text-ink">正在深入思考</p>
              <p className="text-ink-muted text-sm mt-2">分析你的价值观、信念与当前情境...</p>
            </div>
          )}

          {/* Result */}
          {result && !loading && (
            <div className="mt-10 space-y-8 animate-fade-up">
              <DecisionResult data={result} />
              <RecordDecision decisionId={result.decision_id} question={question} recommendation={result.recommendation} />
            </div>
          )}

          {/* Tips */}
          {!result && !loading && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
              {[
                { icon: '01', title: '明确问题', desc: '"选 A 还是 B" 比 "我该怎么办" 更容易分析', delay: 'stagger-1' },
                { icon: '02', title: '提供背景', desc: '你的资源、约束和目标，会直接影响分析', delay: 'stagger-2' },
                { icon: '03', title: '开放心态', desc: '我可能会挑战你的假设——这正是我的价值', delay: 'stagger-3' },
              ].map(t => (
                <div key={t.icon} className={`card reveal ${t.delay} group`}>
                  <span className="inline-block font-heading text-3xl font-bold text-primary/30 group-hover:text-primary transition-colors mb-3">{t.icon}</span>
                  <h3 className="font-heading font-semibold text-ink mb-2">{t.title}</h3>
                  <p className="text-ink-muted text-sm leading-relaxed">{t.desc}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

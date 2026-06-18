'use client';

import { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import DecisionForm from '@/components/DecisionForm';
import DecisionResult from '@/components/DecisionResult';
import RecordDecision from '@/components/RecordDecision';

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');

  return (
    <main className="min-h-screen">
      <Sidebar />

      <div className="md:ml-[260px] p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-3xl mx-auto">
          {/* Welcome Header */}
          {!result && !loading && (
            <div className="text-center mb-10 animate-fade-in">
              <div className="text-7xl mb-4 animate-float">🐱</div>
              <h1 className="font-display text-3xl md:text-4xl text-primary-dark mb-2">
                今天有什么决定要做呀？
              </h1>
              <p className="text-kawaii-text-light text-lg">
                把你的困惑告诉我，我帮你理清思路~
              </p>
            </div>
          )}

          {/* Decision Form */}
          <div className="animate-fade-in">
            <DecisionForm
              onResult={(data, q) => { setResult(data); setQuestion(q); }}
              setLoading={setLoading}
              loading={loading}
            />
          </div>

          {/* Loading State */}
          {loading && (
            <div className="mt-8 kawaii-card p-8 text-center animate-slide-up">
              <div className="flex justify-center gap-2 mb-4">
                <div className="thinking-dot" />
                <div className="thinking-dot" />
                <div className="thinking-dot" />
              </div>
              <p className="text-kawaii-text font-semibold">让我仔细想想...</p>
              <p className="text-kawaii-text-light text-sm mt-1">正在分析你的价值观和信念</p>
            </div>
          )}

          {/* Result */}
          {result && !loading && (
            <div className="mt-8 space-y-6 animate-slide-up">
              <DecisionResult data={result} />
              <RecordDecision
                decisionId={result.decision_id}
                question={question}
                recommendation={result.recommendation}
              />
            </div>
          )}

          {/* Tips */}
          {!result && !loading && (
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="kawaii-card p-5 animate-slide-up stagger-1">
                <span className="text-3xl block mb-3">🎯</span>
                <h3 className="font-bold text-kawaii-text mb-1">具体化你的问题</h3>
                <p className="text-sm text-kawaii-text-light">
                  &ldquo;要不要做 A 还是 B&rdquo; 比 &ldquo;我该怎么办&rdquo; 更容易分析
                </p>
              </div>

              <div className="kawaii-card p-5 animate-slide-up stagger-2">
                <span className="text-3xl block mb-3">📋</span>
                <h3 className="font-bold text-kawaii-text mb-1">提供背景信息</h3>
                <p className="text-sm text-kawaii-text-light">
                  你的资源、约束、目标，这些会影响分析结果哦
                </p>
              </div>

              <div className="kawaii-card p-5 animate-slide-up stagger-3">
                <span className="text-3xl block mb-3">💡</span>
                <h3 className="font-bold text-kawaii-text mb-1">开放心态</h3>
                <p className="text-sm text-kawaii-text-light">
                  我可能会挑战你的假设，这正是我的价值呀
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

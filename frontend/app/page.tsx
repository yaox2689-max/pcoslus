'use client';

import { useState } from 'react';
import Navigation from '@/components/Navigation';
import DecisionForm from '@/components/DecisionForm';
import DecisionResult from '@/components/DecisionResult';

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <main className="min-h-screen">
      <Navigation />

      <div className="md:ml-64 p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in">
            <h1 className="font-serif text-3xl md:text-4xl font-bold text-warm-800 mb-2">
              今天有什么决定要做？
            </h1>
            <p className="text-warm-500 text-lg">
              把你的困惑告诉我，我帮你理清思路
            </p>
          </div>

          {/* Decision Form */}
          <div className="animate-fade-in stagger-1">
            <DecisionForm
              onResult={setResult}
              setLoading={setLoading}
              loading={loading}
            />
          </div>

          {/* Result */}
          {result && (
            <div className="mt-8 animate-fade-in">
              <DecisionResult data={result} />
            </div>
          )}

          {/* Tips */}
          {!result && !loading && (
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4 animate-fade-in stagger-3">
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-5 border border-warm-100 card-hover">
                <div className="w-10 h-10 rounded-xl bg-warm-100 flex items-center justify-center mb-3">
                  <span className="text-xl">🎯</span>
                </div>
                <h3 className="font-medium text-warm-800 mb-1">具体化你的问题</h3>
                <p className="text-sm text-warm-500">
                  "要不要做 A 还是 B" 比 "我该怎么办" 更容易分析
                </p>
              </div>

              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-5 border border-warm-100 card-hover">
                <div className="w-10 h-10 rounded-xl bg-sage-100 flex items-center justify-center mb-3">
                  <span className="text-xl">📋</span>
                </div>
                <h3 className="font-medium text-warm-800 mb-1">提供背景信息</h3>
                <p className="text-sm text-warm-500">
                  你的资源、约束、目标，这些会影响分析结果
                </p>
              </div>

              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-5 border border-warm-100 card-hover">
                <div className="w-10 h-10 rounded-xl bg-cream-200 flex items-center justify-center mb-3">
                  <span className="text-xl">💡</span>
                </div>
                <h3 className="font-medium text-warm-800 mb-1">开放心态</h3>
                <p className="text-sm text-warm-500">
                  PCOS 可能会挑战你的假设，这正是它的价值
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

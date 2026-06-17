'use client';

import { useState, useEffect } from 'react';
import Navigation from '@/components/Navigation';
import { Clock, Filter, Search, ChevronRight } from 'lucide-react';

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
    fetchDecisions();
  }, []);

  const fetchDecisions = async () => {
    try {
      const response = await fetch('/api/decide/journal?limit=50');
      const data = await response.json();
      setDecisions(data);
    } catch (error) {
      console.error('Failed to fetch decisions:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('zh-CN', {
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.7) return 'text-sage-600 bg-sage-50';
    if (confidence > 0.4) return 'text-warm-600 bg-warm-50';
    return 'text-red-500 bg-red-50';
  };

  return (
    <main className="min-h-screen">
      <Navigation />

      <div className="md:ml-64 p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in">
            <h1 className="font-serif text-3xl md:text-4xl font-bold text-warm-800 mb-2">
              决策历史
            </h1>
            <p className="text-warm-500 text-lg">
              回顾过去的决定，看看你的决策模式
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 mb-8 animate-fade-in stagger-1">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-5 border border-warm-100 text-center">
              <p className="text-3xl font-serif font-bold text-warm-700">{decisions.length}</p>
              <p className="text-sm text-warm-500 mt-1">总决策数</p>
            </div>
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-5 border border-warm-100 text-center">
              <p className="text-3xl font-serif font-bold text-sage-600">
                {decisions.filter(d => d.confidence > 0.7).length}
              </p>
              <p className="text-sm text-warm-500 mt-1">高置信度</p>
            </div>
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-5 border border-warm-100 text-center">
              <p className="text-3xl font-serif font-bold text-warm-600">
                {decisions.filter(d => d.thinking_mode === 'slow').length}
              </p>
              <p className="text-sm text-warm-500 mt-1">深度思考</p>
            </div>
          </div>

          {/* Filter */}
          <div className="flex gap-2 mb-6 animate-fade-in stagger-2">
            {['all', 'slow', 'fast'].map((mode) => (
              <button
                key={mode}
                onClick={() => setFilter(mode)}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                  filter === mode
                    ? 'bg-warm-500 text-white shadow-warm'
                    : 'bg-white/60 text-warm-600 hover:bg-warm-50'
                }`}
              >
                {mode === 'all' ? '全部' : mode === 'slow' ? '深度思考' : '快速判断'}
              </button>
            ))}
          </div>

          {/* Decision list */}
          {loading ? (
            <div className="text-center py-12">
              <div className="w-8 h-8 border-2 border-warm-300 border-t-warm-500 rounded-full animate-spin mx-auto" />
              <p className="text-warm-500 mt-4">加载中...</p>
            </div>
          ) : decisions.length === 0 ? (
            <div className="text-center py-12 bg-white/60 rounded-2xl border border-warm-100">
              <Clock className="w-12 h-12 text-warm-300 mx-auto mb-4" />
              <p className="text-warm-600 font-medium">还没有决策记录</p>
              <p className="text-warm-400 text-sm mt-1">去做你的第一个决定吧</p>
            </div>
          ) : (
            <div className="space-y-4">
              {decisions
                .filter(d => filter === 'all' || d.thinking_mode === filter)
                .map((decision, index) => (
                  <div
                    key={decision.id}
                    className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-5 card-hover animate-fade-in"
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-serif text-lg text-warm-800 mb-2">
                          {decision.question}
                        </p>
                        <p className="text-sm text-warm-600 line-clamp-2 mb-3">
                          {decision.decision}
                        </p>
                        <div className="flex items-center gap-3">
                          <span className="text-xs text-warm-400">
                            {formatDate(decision.timestamp)}
                          </span>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getConfidenceColor(decision.confidence)}`}>
                            {Math.round(decision.confidence * 100)}%
                          </span>
                          <span className="text-xs text-warm-400">
                            {decision.thinking_mode === 'slow' ? '深度思考' : '快速判断'}
                          </span>
                        </div>
                      </div>
                      <ChevronRight className="w-5 h-5 text-warm-300 flex-shrink-0 ml-4" />
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

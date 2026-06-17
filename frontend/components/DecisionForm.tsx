'use client';

import { useState } from 'react';
import { Send, Loader2, ChevronDown } from 'lucide-react';

interface DecisionFormProps {
  onResult: (result: any) => void;
  setLoading: (loading: boolean) => void;
  loading: boolean;
}

const categories = [
  { value: '', label: '自动识别' },
  { value: 'startup', label: '创业' },
  { value: 'product', label: '产品' },
  { value: 'tech', label: '技术' },
  { value: 'business', label: '商业' },
  { value: 'hiring', label: '招聘' },
  { value: 'career', label: '职业' },
  { value: 'investment', label: '投资' },
  { value: 'personal', label: '个人' },
];

export default function DecisionForm({ onResult, setLoading, loading }: DecisionFormProps) {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [category, setCategory] = useState('');
  const [showContext, setShowContext] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    setLoading(true);
    onResult(null);

    try {
      const response = await fetch('/api/decide/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: question.trim(),
          context: context.trim() || undefined,
          category: category || undefined,
        }),
      });

      if (!response.ok) throw new Error('请求失败');

      const data = await response.json();
      onResult(data);
    } catch (error) {
      console.error('Decision error:', error);
      alert('请求失败，请检查 PCOS 服务是否运行');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Main question input */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 shadow-warm overflow-hidden">
        <div className="p-4 md:p-6">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="你想做什么决定？例如：要不要接受这个工作机会？要不要开始做这个项目？"
            className="w-full h-32 text-lg text-warm-800 placeholder:text-warm-300 bg-transparent resize-none focus:outline-none font-serif"
            disabled={loading}
          />
        </div>

        {/* Context toggle */}
        <div className="border-t border-warm-50 px-4 md:px-6 py-3 flex items-center justify-between">
          <button
            type="button"
            onClick={() => setShowContext(!showContext)}
            className="flex items-center gap-2 text-sm text-warm-500 hover:text-warm-600 transition-colors"
          >
            <ChevronDown className={`w-4 h-4 transition-transform ${showContext ? 'rotate-180' : ''}`} />
            {showContext ? '收起背景信息' : '添加背景信息（可选）'}
          </button>

          <div className="flex items-center gap-3">
            {/* Category select */}
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="text-sm text-warm-600 bg-warm-50 border border-warm-100 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-warm-200"
              disabled={loading}
            >
              {categories.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>

            {/* Submit button */}
            <button
              type="submit"
              disabled={!question.trim() || loading}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all duration-200 ${
                question.trim() && !loading
                  ? 'bg-gradient-to-r from-warm-400 to-warm-500 text-white shadow-warm hover:shadow-warm-lg hover:scale-[1.02]'
                  : 'bg-warm-100 text-warm-300 cursor-not-allowed'
              }`}
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>思考中...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>问问 PCOS</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Context input (collapsible) */}
      {showContext && (
        <div className="bg-white/60 backdrop-blur-sm rounded-2xl border border-warm-100 p-4 md:p-6 animate-fade-in">
          <label className="block text-sm font-medium text-warm-600 mb-2">
            背景信息
          </label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="你的资源、约束、目标是什么？例如：有3个月时间，10万预算，想验证市场需求"
            className="w-full h-24 text-warm-700 placeholder:text-warm-300 bg-transparent resize-none focus:outline-none"
            disabled={loading}
          />
        </div>
      )}
    </form>
  );
}

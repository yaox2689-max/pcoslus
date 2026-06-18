'use client';

import { useState } from 'react';

interface Props {
  onResult: (data: any, question: string) => void;
  setLoading: (v: boolean) => void;
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
  { value: 'personal', label: '个人' },
];

export default function DecisionForm({ onResult, setLoading, loading }: Props) {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [category, setCategory] = useState('');
  const [showContext, setShowContext] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    setLoading(true);
    try {
      const res = await fetch('/api/decide/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: question.trim(),
          context: context.trim() || undefined,
          category: category || undefined,
        }),
      });
      if (!res.ok) throw new Error('请求失败');
      const data = await res.json();
      onResult(data, question.trim());
    } catch (err) {
      alert('请求失败，请检查 PCOS 服务是否运行 (port 8001)');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="kawaii-card overflow-hidden">
        <div className="p-5 md:p-6">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="你想做什么决定呀？例如：要不要接受这个工作机会？要不要开始做这个项目？"
            className="textarea-kawaii h-28 text-base font-display"
            disabled={loading}
          />
        </div>

        <div className="border-t border-primary/10 px-5 md:px-6 py-3 flex items-center justify-between flex-wrap gap-3">
          <button
            type="button"
            onClick={() => setShowContext(!showContext)}
            className="flex items-center gap-1 text-sm text-kawaii-text-light hover:text-primary-dark transition-colors"
          >
            <span className={`transition-transform inline-block ${showContext ? 'rotate-180' : ''}`}>▼</span>
            {showContext ? '收起背景' : '添加背景（可选）'}
          </button>

          <div className="flex items-center gap-3">
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="text-sm bg-primary/5 border-2 border-primary/10 rounded-full px-4 py-2 text-kawaii-text focus:outline-none focus:border-primary transition-colors"
              disabled={loading}
            >
              {categories.map((c) => (
                <option key={c.value} value={c.value}>{c.label}</option>
              ))}
            </select>

            <button
              type="submit"
              disabled={!question.trim() || loading}
              className="btn-kawaii-primary flex items-center gap-2"
            >
              {loading ? (
                <>
                  <span className="animate-spin">🌀</span>
                  <span>思考中</span>
                </>
              ) : (
                <>
                  <span>🐾</span>
                  <span>问问猫咪</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {showContext && (
        <div className="kawaii-card p-5 animate-slide-up">
          <label className="block text-sm font-semibold text-kawaii-text mb-2">
            背景信息
          </label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="你的资源、约束、目标是什么？例如：有3个月时间，10万预算，想验证市场需求"
            className="textarea-kawaii h-20"
            disabled={loading}
          />
        </div>
      )}
    </form>
  );
}

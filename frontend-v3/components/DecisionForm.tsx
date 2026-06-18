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
        body: JSON.stringify({ question: question.trim(), context: context.trim() || undefined, category: category || undefined }),
      });
      if (!res.ok) throw new Error('请求失败');
      onResult(await res.json(), question.trim());
    } catch { alert('请求失败，请确认 PCOS 服务运行在 8001 端口'); }
    finally { setLoading(false); }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="card !p-0 overflow-hidden">
        <div className="p-5 md:p-6">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="你想做什么决定？例如：要不要接受这个工作机会？要不要开始做这个项目？"
            className="textarea !bg-transparent !border-0 !p-0 !rounded-none h-28 text-lg font-heading"
            disabled={loading}
          />
        </div>

        <div className="border-t border-border-light px-5 md:px-6 py-3 flex items-center justify-between flex-wrap gap-3">
          <button type="button" onClick={() => setShowContext(!showContext)}
            className="flex items-center gap-1.5 text-sm text-ink-muted hover:text-primary transition-colors">
            <svg className={`w-4 h-4 transition-transform ${showContext ? 'rotate-180' : ''}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><polyline points="6 9 12 15 18 9"/></svg>
            {showContext ? '收起背景' : '添加背景信息'}
          </button>

          <div className="flex items-center gap-3">
            <select value={category} onChange={(e) => setCategory(e.target.value)}
              className="input !w-auto !py-2 !px-4 !rounded-full text-sm" disabled={loading}>
              {categories.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
            </select>

            <button type="submit" disabled={!question.trim() || loading} className="btn--primary flex items-center gap-2">
              {loading ? (
                <><svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" strokeDasharray="30 70"/></svg><span>分析中</span></>
              ) : (
                <><span>开始分析</span><svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></>
              )}
            </button>
          </div>
        </div>
      </div>

      {showContext && (
        <div className="card animate-fade-up">
          <label className="block text-sm font-heading font-semibold text-ink mb-3">背景信息</label>
          <textarea value={context} onChange={(e) => setContext(e.target.value)}
            placeholder="你的资源、约束、目标是什么？例如：有3个月时间，10万预算，想验证市场需求"
            className="textarea h-20" disabled={loading} />
        </div>
      )}
    </form>
  );
}

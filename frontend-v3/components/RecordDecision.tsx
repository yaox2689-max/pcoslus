'use client';

import { useState } from 'react';

interface Props {
  decisionId: string;
  question: string;
  recommendation: string;
}

export default function RecordDecision({ decisionId, question, recommendation }: Props) {
  const [originalPlan, setOriginalPlan] = useState('');
  const [myDecision, setMyDecision] = useState('');
  const [reasoning, setReasoning] = useState('');
  const [saved, setSaved] = useState(false);
  const [alignment, setAlignment] = useState<number | null>(null);

  const handleSave = () => {
    if (!myDecision.trim()) return;
    const recWords = recommendation.toLowerCase().split(/\s+/).slice(0, 5);
    const myLower = myDecision.toLowerCase();
    setAlignment(recWords.filter(w => myLower.includes(w)).length / Math.max(recWords.length, 1));
    setSaved(true);
  };

  if (saved) {
    return (
      <div className="card !p-8 border-2 border-emerald-200 dark:border-emerald-800 animate-fade-up">
        <div className="flex items-center gap-3 mb-4">
          <span className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center">
            <svg className="w-5 h-5 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><polyline points="20 6 9 17 4 12"/></svg>
          </span>
          <h3 className="font-heading text-lg font-bold text-ink">决定已记录</h3>
        </div>
        <div className="bg-surface-alt rounded-xl p-5 space-y-2 text-sm text-ink-light">
          <p><span className="font-semibold text-ink">你的选择：</span>{myDecision}</p>
          {originalPlan && <p><span className="font-semibold text-ink">原计划：</span>{originalPlan}</p>}
          {reasoning && <p><span className="font-semibold text-ink">理由：</span>{reasoning}</p>}
          {alignment !== null && (
            <p><span className="font-semibold text-ink">对齐度：</span>
              <span className={alignment > 0.6 ? 'text-emerald-600 font-bold' : 'text-amber-600 font-bold'}>{Math.round(alignment * 100)}%</span>
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="card !p-8 animate-fade-up">
      <div className="flex items-center gap-3 mb-6">
        <span className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
          <svg className="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        </span>
        <div>
          <h3 className="font-heading text-lg font-bold text-ink">记录你的决定</h3>
          <p className="text-sm text-ink-muted">建议已给出，最终决定权在你</p>
        </div>
      </div>
      <div className="space-y-5">
        <div>
          <label className="block text-sm font-heading font-semibold text-ink mb-2">看到分析前，你的原计划是？</label>
          <input value={originalPlan} onChange={(e) => setOriginalPlan(e.target.value)} placeholder="例如：我本来想选 A" className="input" />
        </div>
        <div>
          <label className="block text-sm font-heading font-semibold text-ink mb-2"><span className="text-red-400">*</span> 你最终的决定是？</label>
          <textarea value={myDecision} onChange={(e) => setMyDecision(e.target.value)} placeholder="告诉我你的最终选择..." className="textarea h-24" />
        </div>
        <div>
          <label className="block text-sm font-heading font-semibold text-ink mb-2">为什么？（可选）</label>
          <textarea value={reasoning} onChange={(e) => setReasoning(e.target.value)} placeholder="你的思考过程..." className="textarea h-20" />
        </div>
        <div className="flex justify-end">
          <button onClick={handleSave} disabled={!myDecision.trim()} className="btn--primary">
            记录决定
          </button>
        </div>
      </div>
    </div>
  );
}

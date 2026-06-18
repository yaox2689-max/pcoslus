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

    // Simple alignment calculation
    const recWords = recommendation.toLowerCase().split(/\s+/).slice(0, 5);
    const myLower = myDecision.toLowerCase();
    const matchCount = recWords.filter(w => myLower.includes(w)).length;
    setAlignment(matchCount / Math.max(recWords.length, 1));

    setSaved(true);
  };

  if (saved) {
    return (
      <div className="kawaii-card p-6 border-2 border-accent animate-slide-up">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-3xl">✅</span>
          <h3 className="font-display text-lg text-green-700">已记录你的决定~</h3>
        </div>
        <div className="space-y-2 text-sm text-kawaii-text bg-accent/20 rounded-[15px] p-4">
          <p><span className="font-bold">你的选择：</span>{myDecision}</p>
          {originalPlan && <p><span className="font-bold">原计划：</span>{originalPlan}</p>}
          {reasoning && <p><span className="font-bold">理由：</span>{reasoning}</p>}
          {alignment !== null && (
            <p>
              <span className="font-bold">与猫咪建议对齐度：</span>
              <span className={alignment > 0.6 ? 'text-green-600 font-bold' : 'text-orange-600 font-bold'}>
                {Math.round(alignment * 100)}%
              </span>
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="kawaii-card p-6 animate-slide-up">
      <div className="flex items-center gap-3 mb-6">
        <span className="text-3xl">📝</span>
        <div>
          <h3 className="font-display text-lg text-primary-dark">记录你的决定</h3>
          <p className="text-sm text-kawaii-text-light">猫咪给了建议，最终决定权在你手上~</p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-bold text-kawaii-text mb-2">
            在看到分析之前，你原本的计划是？
          </label>
          <input
            type="text"
            value={originalPlan}
            onChange={(e) => setOriginalPlan(e.target.value)}
            placeholder="例如：我本来想选 A"
            className="input-kawaii"
          />
        </div>

        <div>
          <label className="block text-sm font-bold text-kawaii-text mb-2">
            <span className="text-red-400">*</span> 你最终的决定是？
          </label>
          <textarea
            value={myDecision}
            onChange={(e) => setMyDecision(e.target.value)}
            placeholder="告诉我你的最终选择吧..."
            className="textarea-kawaii h-24"
          />
        </div>

        <div>
          <label className="block text-sm font-bold text-kawaii-text mb-2">
            为什么做出这个决定？（可选）
          </label>
          <textarea
            value={reasoning}
            onChange={(e) => setReasoning(e.target.value)}
            placeholder="你的思考过程..."
            className="textarea-kawaii h-20"
          />
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleSave}
            disabled={!myDecision.trim()}
            className="btn-kawaii-primary flex items-center gap-2"
          >
            <span>🐾</span>
            <span>记录我的决定</span>
          </button>
        </div>
      </div>
    </div>
  );
}

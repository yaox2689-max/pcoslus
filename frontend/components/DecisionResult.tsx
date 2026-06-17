'use client';

import { useState } from 'react';
import {
  Lightbulb,
  AlertTriangle,
  ThumbsUp,
  ThumbsDown,
  Scale,
  Target,
  Shield,
  Zap,
  CheckCircle,
  Save,
  Loader2
} from 'lucide-react';

interface DecisionResultProps {
  data: {
    decision_id: string;
    question: string;
    thinking_mode: string;
    thinking_mode_reason: string;
    recommendation: string;
    confidence: number;
    reasoning_chain: string[];
    options_evaluated: Array<{
      option: string;
      score: {
        value_alignment: number;
        belief_support: number;
        resource_feasibility: number;
        risk_acceptability: number;
        learning_potential: number;
        weighted_total: number;
      };
    }>;
    value_conflicts: {
      gains: string[];
      losses: string[];
      net_alignment: number;
      severity: number;
      dominant_conflict: string;
    };
    counter_argument: {
      position: string;
      reasoning: string;
    };
    key_risks: string[];
    key_assumptions: string[];
    beliefs_used: string[];
  };
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-warm-500">{label}</span>
        <span className="font-medium text-warm-700">{Math.round(value * 100)}%</span>
      </div>
      <div className="h-2 bg-warm-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${value * 100}%` }}
        />
      </div>
    </div>
  );
}

export default function DecisionResult({ data }: DecisionResultProps) {
  const confidenceColor = data.confidence > 0.7 ? 'text-sage-600' : data.confidence > 0.4 ? 'text-warm-600' : 'text-red-500';
  const confidenceBg = data.confidence > 0.7 ? 'bg-sage-50' : data.confidence > 0.4 ? 'bg-warm-50' : 'bg-red-50';

  return (
    <div className="space-y-6">
      {/* Main recommendation */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 shadow-warm-lg overflow-hidden">
        <div className="p-6 md:p-8">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-warm-400 to-warm-500 flex items-center justify-center">
                <Lightbulb className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-warm-800">我的建议</h2>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-xs px-2 py-0.5 rounded-full ${confidenceBg} ${confidenceColor} font-medium`}>
                    置信度 {Math.round(data.confidence * 100)}%
                  </span>
                  <span className="text-xs text-warm-400">
                    {data.thinking_mode === 'slow' ? '深度思考' : '快速判断'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <p className="text-lg md:text-xl text-warm-800 font-serif leading-relaxed mb-6">
            {data.recommendation}
          </p>

          {/* Reasoning chain */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-warm-600 flex items-center gap-2">
              <Target className="w-4 h-4" />
              推理过程
            </h3>
            <div className="space-y-2">
              {data.reasoning_chain.map((reason, index) => (
                <div
                  key={index}
                  className="flex gap-3 text-sm text-warm-700 animate-slide-in"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-warm-100 flex items-center justify-center text-xs font-medium text-warm-500">
                    {index + 1}
                  </span>
                  <span className="leading-relaxed">{reason}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Value conflicts */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 overflow-hidden">
        <div className="p-6">
          <h3 className="font-medium text-warm-800 flex items-center gap-2 mb-4">
            <Scale className="w-5 h-5 text-warm-500" />
            价值观权衡
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Gains */}
            <div>
              <div className="flex items-center gap-2 mb-3">
                <ThumbsUp className="w-4 h-4 text-sage-500" />
                <span className="text-sm font-medium text-sage-700">会增强的价值观</span>
              </div>
              <div className="space-y-2">
                {data.value_conflicts.gains.map((gain, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-2 px-3 py-2 bg-sage-50 rounded-lg text-sm text-sage-700"
                  >
                    <div className="w-2 h-2 rounded-full bg-sage-400" />
                    {gain}
                  </div>
                ))}
              </div>
            </div>

            {/* Losses */}
            <div>
              <div className="flex items-center gap-2 mb-3">
                <ThumbsDown className="w-4 h-4 text-warm-500" />
                <span className="text-sm font-medium text-warm-700">会削弱的价值观</span>
              </div>
              <div className="space-y-2">
                {data.value_conflicts.losses.map((loss, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-2 px-3 py-2 bg-warm-50 rounded-lg text-sm text-warm-700"
                  >
                    <div className="w-2 h-2 rounded-full bg-warm-400" />
                    {loss}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Dominant conflict */}
          {data.value_conflicts.dominant_conflict && (
            <div className="mt-4 p-3 bg-cream-100 rounded-xl">
              <p className="text-sm text-warm-600">
                <span className="font-medium">核心冲突：</span>
                {data.value_conflicts.dominant_conflict.replace(/_/g, ' vs ')}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Counter argument */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 overflow-hidden">
        <div className="p-6">
          <h3 className="font-medium text-warm-800 flex items-center gap-2 mb-4">
            <AlertTriangle className="w-5 h-5 text-warm-500" />
            反方观点
          </h3>
          <div className="bg-warm-50 rounded-xl p-4">
            <p className="font-medium text-warm-700 mb-2">{data.counter_argument.position}</p>
            <p className="text-sm text-warm-600 leading-relaxed">{data.counter_argument.reasoning}</p>
          </div>
        </div>
      </div>

      {/* Options evaluation */}
      {data.options_evaluated.length > 0 && (
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 overflow-hidden">
          <div className="p-6">
            <h3 className="font-medium text-warm-800 flex items-center gap-2 mb-4">
              <Zap className="w-5 h-5 text-warm-500" />
              选项评估
            </h3>
            <div className="space-y-4">
              {data.options_evaluated.map((option, index) => (
                <div
                  key={index}
                  className="p-4 bg-warm-50/50 rounded-xl border border-warm-100"
                >
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-medium text-warm-800">{option.option}</h4>
                    <span className="text-lg font-serif font-bold text-warm-600">
                      {Math.round(option.score.weighted_total * 100)}分
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    <ScoreBar label="价值观" value={option.score.value_alignment} color="bg-sage-400" />
                    <ScoreBar label="信念" value={option.score.belief_support} color="bg-warm-400" />
                    <ScoreBar label="资源" value={option.score.resource_feasibility} color="bg-blue-400" />
                    <ScoreBar label="风险" value={option.score.risk_acceptability} color="bg-purple-400" />
                    <ScoreBar label="学习" value={option.score.learning_potential} color="bg-pink-400" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Risks and assumptions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Risks */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6">
          <h3 className="font-medium text-warm-800 flex items-center gap-2 mb-4">
            <Shield className="w-5 h-5 text-warm-500" />
            风险提示
          </h3>
          <ul className="space-y-2">
            {data.key_risks.map((risk, index) => (
              <li key={index} className="flex gap-2 text-sm text-warm-600">
                <span className="text-warm-400">•</span>
                {risk}
              </li>
            ))}
          </ul>
        </div>

        {/* Assumptions */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6">
          <h3 className="font-medium text-warm-800 flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-warm-500" />
            关键假设
          </h3>
          <ul className="space-y-2">
            {data.key_assumptions.map((assumption, index) => (
              <li key={index} className="flex gap-2 text-sm text-warm-600">
                <span className="text-warm-400">•</span>
                {assumption}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Record My Decision */}
      <RecordDecision decisionId={data.decision_id} question={data.question} recommendation={data.recommendation} />
    </div>
  );
}

function RecordDecision({ decisionId, question, recommendation }: { decisionId: string; question: string; recommendation: string }) {
  const [myDecision, setMyDecision] = useState('');
  const [originalPlan, setOriginalPlan] = useState('');
  const [reasoning, setReasoning] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [alignment, setAlignment] = useState<number | null>(null);

  const handleSave = async () => {
    if (!myDecision.trim()) return;

    setSaving(true);
    try {
      // Calculate simple alignment
      const recLower = recommendation.toLowerCase();
      const myLower = myDecision.toLowerCase();
      const recWords = recLower.split(/\s+/).slice(0, 5);
      const matchCount = recWords.filter(w => myLower.includes(w)).length;
      const alignScore = matchCount / Math.min(recWords.length, 5);
      setAlignment(alignScore);

      // Save to backend (we'll add this endpoint later)
      setSaved(true);
    } catch (error) {
      console.error('Failed to save decision:', error);
    } finally {
      setSaving(false);
    }
  };

  if (saved) {
    return (
      <div className="bg-sage-50 rounded-2xl border border-sage-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <CheckCircle className="w-6 h-6 text-sage-600" />
          <h3 className="font-serif text-lg font-bold text-sage-800">已记录你的决定</h3>
        </div>
        <div className="space-y-2 text-sm text-sage-700">
          <p><span className="font-medium">你的选择：</span>{myDecision}</p>
          {originalPlan && <p><span className="font-medium">原计划：</span>{originalPlan}</p>}
          {reasoning && <p><span className="font-medium">理由：</span>{reasoning}</p>}
          {alignment !== null && (
            <p>
              <span className="font-medium">与 PCOS 对齐度：</span>
              <span className={alignment > 0.6 ? 'text-sage-600' : 'text-warm-600'}>
                {Math.round(alignment * 100)}%
              </span>
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 overflow-hidden">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-warm-100 flex items-center justify-center">
            <CheckCircle className="w-5 h-5 text-warm-600" />
          </div>
          <div>
            <h3 className="font-serif text-lg font-bold text-warm-800">记录你的决定</h3>
            <p className="text-sm text-warm-500">PCOS 给出了建议，最终决定权在你</p>
          </div>
        </div>

        <div className="space-y-4">
          {/* Original plan */}
          <div>
            <label className="block text-sm font-medium text-warm-700 mb-2">
              在看到 PCOS 分析之前，你原本的计划是什么？
            </label>
            <input
              type="text"
              value={originalPlan}
              onChange={(e) => setOriginalPlan(e.target.value)}
              placeholder="例如：我本来想选 A"
              className="w-full px-4 py-3 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300 text-warm-800 placeholder:text-warm-300"
            />
          </div>

          {/* My decision */}
          <div>
            <label className="block text-sm font-medium text-warm-700 mb-2">
              <span className="text-red-500">*</span> 你最终的决定是什么？
            </label>
            <textarea
              value={myDecision}
              onChange={(e) => setMyDecision(e.target.value)}
              placeholder="告诉我你的最终选择..."
              className="w-full h-24 px-4 py-3 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300 text-warm-800 placeholder:text-warm-300 resize-none"
            />
          </div>

          {/* Reasoning */}
          <div>
            <label className="block text-sm font-medium text-warm-700 mb-2">
              为什么做出这个决定？（可选）
            </label>
            <textarea
              value={reasoning}
              onChange={(e) => setReasoning(e.target.value)}
              placeholder="你的思考过程..."
              className="w-full h-20 px-4 py-3 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300 text-warm-800 placeholder:text-warm-300 resize-none"
            />
          </div>

          {/* Save button */}
          <div className="flex justify-end">
            <button
              onClick={handleSave}
              disabled={!myDecision.trim() || saving}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                myDecision.trim() && !saving
                  ? 'bg-gradient-to-r from-sage-400 to-sage-500 text-white shadow-lg hover:shadow-xl hover:scale-[1.02]'
                  : 'bg-warm-100 text-warm-300 cursor-not-allowed'
              }`}
            >
              {saving ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>保存中...</span>
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  <span>记录我的决定</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

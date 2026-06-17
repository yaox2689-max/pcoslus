'use client';

import { useState } from 'react';
import Navigation from '@/components/Navigation';
import { User, Target, Brain, Save, Plus, X } from 'lucide-react';

export default function SettingsPage() {
  const [values, setValues] = useState([
    { name: '自主性', weight: 0.90, category: 'life_philosophy' },
    { name: '持续学习', weight: 0.90, category: 'growth' },
    { name: '职业安全', weight: 0.85, category: 'security' },
    { name: '市场竞争力', weight: 0.85, category: 'security' },
    { name: '经济韧性', weight: 0.80, category: 'security' },
    { name: '创造力', weight: 0.70, category: 'work_style' },
    { name: '影响力', weight: 0.60, category: 'impact' },
  ]);

  const [preferences, setPreferences] = useState({
    decision_speed: 'fast',
    risk_tolerance: 'moderate',
    information_density: 'high',
    long_term_vs_short_term: 'long_term',
  });

  const [focus, setFocus] = useState({
    primary: '商业与创业',
    secondary: '技术与工程',
    time_horizon: 'medium',
  });

  const [showAddValue, setShowAddValue] = useState(false);
  const [newValue, setNewValue] = useState({ name: '', category: 'growth' });

  const handleAddValue = () => {
    if (newValue.name.trim()) {
      setValues([...values, { ...newValue, weight: 0.5 }]);
      setNewValue({ name: '', category: 'growth' });
      setShowAddValue(false);
    }
  };

  const handleRemoveValue = (index: number) => {
    setValues(values.filter((_, i) => i !== index));
  };

  const handleWeightChange = (index: number, weight: number) => {
    const newValues = [...values];
    newValues[index].weight = weight;
    setValues(newValues);
  };

  return (
    <main className="min-h-screen">
      <Navigation />

      <div className="md:ml-64 p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in">
            <h1 className="font-serif text-3xl md:text-4xl font-bold text-warm-800 mb-2">
              我的设置
            </h1>
            <p className="text-warm-500 text-lg">
              定义你的价值观和决策偏好
            </p>
          </div>

          {/* Values */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6 mb-6 animate-fade-in stagger-1">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-sage-100 flex items-center justify-center">
                  <Target className="w-5 h-5 text-sage-600" />
                </div>
                <div>
                  <h2 className="font-serif text-xl font-bold text-warm-800">核心价值观</h2>
                  <p className="text-sm text-warm-500">这些价值观会影响 PCOS 的决策建议</p>
                </div>
              </div>
              <button
                onClick={() => setShowAddValue(true)}
                className="flex items-center gap-2 px-3 py-2 bg-warm-100 text-warm-600 rounded-xl hover:bg-warm-200 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span className="text-sm">添加</span>
              </button>
            </div>

            <div className="space-y-4">
              {values.map((value, index) => (
                <div
                  key={index}
                  className="flex items-center gap-4 p-3 bg-warm-50/50 rounded-xl border border-warm-100"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-warm-800">{value.name}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-warm-100 text-warm-500">
                        {value.category}
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={value.weight * 100}
                        onChange={(e) => handleWeightChange(index, parseInt(e.target.value) / 100)}
                        className="flex-1 h-2 bg-warm-200 rounded-full appearance-none cursor-pointer accent-warm-500"
                      />
                      <span className="text-sm font-medium text-warm-600 w-12 text-right">
                        {Math.round(value.weight * 100)}%
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => handleRemoveValue(index)}
                    className="p-1.5 text-warm-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>

            {/* Add value form */}
            {showAddValue && (
              <div className="mt-4 p-4 bg-cream-100 rounded-xl border border-cream-200 animate-fade-in">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={newValue.name}
                    onChange={(e) => setNewValue({ ...newValue, name: e.target.value })}
                    placeholder="价值观名称"
                    className="flex-1 px-3 py-2 bg-white border border-warm-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-warm-300"
                  />
                  <select
                    value={newValue.category}
                    onChange={(e) => setNewValue({ ...newValue, category: e.target.value })}
                    className="px-3 py-2 bg-white border border-warm-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-warm-300"
                  >
                    <option value="life_philosophy">人生哲学</option>
                    <option value="work_style">工作风格</option>
                    <option value="growth">成长</option>
                    <option value="security">安全</option>
                    <option value="impact">影响力</option>
                  </select>
                  <button
                    onClick={handleAddValue}
                    className="px-4 py-2 bg-warm-500 text-white rounded-lg hover:bg-warm-600 transition-colors"
                  >
                    添加
                  </button>
                  <button
                    onClick={() => setShowAddValue(false)}
                    className="px-3 py-2 text-warm-500 hover:bg-warm-100 rounded-lg transition-colors"
                  >
                    取消
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Preferences */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6 mb-6 animate-fade-in stagger-2">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-warm-100 flex items-center justify-center">
                <Brain className="w-5 h-5 text-warm-600" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-warm-800">决策偏好</h2>
                <p className="text-sm text-warm-500">你倾向于怎样做决定</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-warm-700">决策速度</label>
                <select
                  value={preferences.decision_speed}
                  onChange={(e) => setPreferences({ ...preferences, decision_speed: e.target.value })}
                  className="w-full px-3 py-2 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300"
                >
                  <option value="fast">快速决策</option>
                  <option value="moderate">平衡</option>
                  <option value="slow">深思熟虑</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-warm-700">风险承受</label>
                <select
                  value={preferences.risk_tolerance}
                  onChange={(e) => setPreferences({ ...preferences, risk_tolerance: e.target.value })}
                  className="w-full px-3 py-2 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300"
                >
                  <option value="conservative">保守</option>
                  <option value="moderate">适中</option>
                  <option value="aggressive">激进</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-warm-700">信息密度</label>
                <select
                  value={preferences.information_density}
                  onChange={(e) => setPreferences({ ...preferences, information_density: e.target.value })}
                  className="w-full px-3 py-2 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300"
                >
                  <option value="low">简洁</option>
                  <option value="moderate">适中</option>
                  <option value="high">详细</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-warm-700">时间视角</label>
                <select
                  value={preferences.long_term_vs_short_term}
                  onChange={(e) => setPreferences({ ...preferences, long_term_vs_short_term: e.target.value })}
                  className="w-full px-3 py-2 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300"
                >
                  <option value="short_term">短期</option>
                  <option value="moderate">平衡</option>
                  <option value="long_term">长期</option>
                </select>
              </div>
            </div>
          </div>

          {/* Current Focus */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-warm-100 p-6 mb-6 animate-fade-in stagger-3">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-cream-200 flex items-center justify-center">
                <User className="w-5 h-5 text-warm-600" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-warm-800">当前关注</h2>
                <p className="text-sm text-warm-500">你目前最关注的领域</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-warm-700">主要领域</label>
                <input
                  type="text"
                  value={focus.primary}
                  onChange={(e) => setFocus({ ...focus, primary: e.target.value })}
                  className="w-full px-3 py-2 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-warm-700">次要领域</label>
                <input
                  type="text"
                  value={focus.secondary}
                  onChange={(e) => setFocus({ ...focus, secondary: e.target.value })}
                  className="w-full px-3 py-2 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-warm-700">时间视角</label>
                <select
                  value={focus.time_horizon}
                  onChange={(e) => setFocus({ ...focus, time_horizon: e.target.value })}
                  className="w-full px-3 py-2 bg-warm-50 border border-warm-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-warm-300"
                >
                  <option value="short">短期</option>
                  <option value="medium">中期</option>
                  <option value="long">长期</option>
                </select>
              </div>
            </div>
          </div>

          {/* Save button */}
          <div className="flex justify-end animate-fade-in stagger-4">
            <button className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-warm-400 to-warm-500 text-white rounded-xl shadow-warm hover:shadow-warm-lg hover:scale-[1.02] transition-all duration-200">
              <Save className="w-5 h-5" />
              <span className="font-medium">保存设置</span>
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

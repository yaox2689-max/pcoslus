'use client';

import { useState } from 'react';
import Sidebar from '@/components/Sidebar';

const initialValues = [
  { name: '自主性', weight: 0.90, category: 'life_philosophy', emoji: '🦅' },
  { name: '持续学习', weight: 0.90, category: 'growth', emoji: '📚' },
  { name: '职业安全', weight: 0.85, category: 'security', emoji: '🛡️' },
  { name: '市场竞争力', weight: 0.85, category: 'security', emoji: '⚔️' },
  { name: '经济韧性', weight: 0.80, category: 'security', emoji: '💰' },
  { name: '创造力', weight: 0.70, category: 'work_style', emoji: '🎨' },
  { name: '影响力', weight: 0.60, category: 'impact', emoji: '🌟' },
];

export default function SettingsPage() {
  const [values, setValues] = useState(initialValues);
  const [prefs, setPrefs] = useState({
    decision_speed: 'fast',
    risk_tolerance: 'moderate',
    information_density: 'high',
    time_horizon: 'long_term',
  });
  const [focus, setFocus] = useState({
    primary: '商业与创业',
    secondary: '技术与工程',
    horizon: 'medium',
  });
  const [saved, setSaved] = useState(false);

  const updateWeight = (i: number, w: number) => {
    const v = [...values];
    v[i].weight = w;
    setValues(v);
  };

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <main className="min-h-screen">
      <Sidebar />
      <div className="md:ml-[260px] p-4 md:p-8 pb-24 md:pb-8">
        <div className="max-w-3xl mx-auto">
          <div className="mb-8 animate-fade-in">
            <h1 className="font-display text-3xl md:text-4xl text-primary-dark mb-2">⚙️ 设置</h1>
            <p className="text-kawaii-text-light">调整你的价值观和决策偏好~</p>
          </div>

          {/* Values */}
          <div className="kawaii-card p-6 mb-6 animate-slide-up stagger-1">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">💎</span>
              <div>
                <h2 className="font-display text-xl text-primary-dark">核心价值观</h2>
                <p className="text-sm text-kawaii-text-light">这些会影响决策建议</p>
              </div>
            </div>
            <div className="space-y-4">
              {values.map((v, i) => (
                <div key={i} className="flex items-center gap-4 p-3 bg-primary/5 rounded-[15px] border border-primary/10">
                  <span className="text-2xl">{v.emoji}</span>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-bold text-kawaii-text text-sm">{v.name}</span>
                      <span className="badge-kawaii bg-primary/10 text-primary-dark text-[10px]">{v.category}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={v.weight * 100}
                        onChange={(e) => updateWeight(i, parseInt(e.target.value) / 100)}
                        className="flex-1 h-2 bg-primary/10 rounded-full appearance-none cursor-pointer accent-primary"
                      />
                      <span className="text-sm font-bold text-primary-dark w-12 text-right">{Math.round(v.weight * 100)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Preferences */}
          <div className="kawaii-card p-6 mb-6 animate-slide-up stagger-2">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">🧠</span>
              <div>
                <h2 className="font-display text-xl text-primary-dark">决策偏好</h2>
                <p className="text-sm text-kawaii-text-light">你倾向于怎样做决定</p>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-bold text-kawaii-text mb-2 block">决策速度</label>
                <select value={prefs.decision_speed} onChange={e => setPrefs({...prefs, decision_speed: e.target.value})} className="input-kawaii">
                  <option value="fast">快速决策</option>
                  <option value="moderate">平衡</option>
                  <option value="slow">深思熟虑</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-bold text-kawaii-text mb-2 block">风险承受</label>
                <select value={prefs.risk_tolerance} onChange={e => setPrefs({...prefs, risk_tolerance: e.target.value})} className="input-kawaii">
                  <option value="conservative">保守</option>
                  <option value="moderate">适中</option>
                  <option value="aggressive">激进</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-bold text-kawaii-text mb-2 block">信息密度</label>
                <select value={prefs.information_density} onChange={e => setPrefs({...prefs, information_density: e.target.value})} className="input-kawaii">
                  <option value="low">简洁</option>
                  <option value="moderate">适中</option>
                  <option value="high">详细</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-bold text-kawaii-text mb-2 block">时间视角</label>
                <select value={prefs.time_horizon} onChange={e => setPrefs({...prefs, time_horizon: e.target.value})} className="input-kawaii">
                  <option value="short_term">短期</option>
                  <option value="moderate">平衡</option>
                  <option value="long_term">长期</option>
                </select>
              </div>
            </div>
          </div>

          {/* Focus */}
          <div className="kawaii-card p-6 mb-6 animate-slide-up stagger-3">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">🎯</span>
              <div>
                <h2 className="font-display text-xl text-primary-dark">当前关注</h2>
                <p className="text-sm text-kawaii-text-light">你目前最关注的领域</p>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-bold text-kawaii-text mb-2 block">主要领域</label>
                <input value={focus.primary} onChange={e => setFocus({...focus, primary: e.target.value})} className="input-kawaii" />
              </div>
              <div>
                <label className="text-sm font-bold text-kawaii-text mb-2 block">次要领域</label>
                <input value={focus.secondary} onChange={e => setFocus({...focus, secondary: e.target.value})} className="input-kawaii" />
              </div>
              <div>
                <label className="text-sm font-bold text-kawaii-text mb-2 block">时间视角</label>
                <select value={focus.horizon} onChange={e => setFocus({...focus, horizon: e.target.value})} className="input-kawaii">
                  <option value="short">短期</option>
                  <option value="medium">中期</option>
                  <option value="long">长期</option>
                </select>
              </div>
            </div>
          </div>

          {/* Save */}
          <div className="flex justify-end animate-slide-up stagger-4">
            <button onClick={handleSave} className="btn-kawaii-primary flex items-center gap-2">
              {saved ? (
                <><span>✅</span><span>已保存~</span></>
              ) : (
                <><span>💾</span><span>保存设置</span></>
              )}
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

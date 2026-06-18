'use client';

import { useState } from 'react';
import Sidebar from '@/components/Sidebar';

const initValues = [
  { name: '自主性', weight: 0.90, cat: 'life_philosophy' },
  { name: '持续学习', weight: 0.90, cat: 'growth' },
  { name: '职业安全', weight: 0.85, cat: 'security' },
  { name: '市场竞争力', weight: 0.85, cat: 'security' },
  { name: '经济韧性', weight: 0.80, cat: 'security' },
  { name: '创造力', weight: 0.70, cat: 'work_style' },
  { name: '影响力', weight: 0.60, cat: 'impact' },
];

export default function SettingsPage() {
  const [values, setValues] = useState(initValues);
  const [prefs, setPrefs] = useState({ speed: 'fast', risk: 'moderate', density: 'high', horizon: 'long_term' });
  const [focus, setFocus] = useState({ primary: '商业与创业', secondary: '技术与工程', horizon: 'medium' });
  const [saved, setSaved] = useState(false);

  const updateW = (i: number, w: number) => { const v = [...values]; v[i].weight = w; setValues(v); };
  const handleSave = () => { setSaved(true); setTimeout(() => setSaved(false), 2000); };

  return (
    <main className="min-h-screen">
      <Sidebar />
      <div className="md:ml-[280px] pt-14 md:pt-0 p-4 md:p-10 pb-24 md:pb-10">
        <div className="max-w-[960px] mx-auto">
          <div className="mb-10">
            <h1 className="font-heading text-3xl md:text-4xl font-bold text-ink tracking-tight mb-2">设置</h1>
            <p className="text-ink-light text-lg">调整你的价值观与决策偏好</p>
          </div>

          {/* Values */}
          <div className="card !p-8 mb-8">
            <h2 className="font-heading text-xl font-bold text-ink mb-6">核心价值观</h2>
            <div className="space-y-5">
              {values.map((v, i) => (
                <div key={i} className="flex items-center gap-4 p-4 bg-surface-alt rounded-xl">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="font-heading font-semibold text-ink text-sm">{v.name}</span>
                      <span className="pill !text-[10px]">{v.cat}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="range" min="0" max="100" value={v.weight * 100} onChange={e => updateW(i, parseInt(e.target.value) / 100)} className="flex-1 h-1.5 appearance-none bg-border rounded-full cursor-pointer accent-primary" />
                      <span className="text-sm font-bold text-primary w-10 text-right">{Math.round(v.weight * 100)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Preferences */}
          <div className="card !p-8 mb-8">
            <h2 className="font-heading text-xl font-bold text-ink mb-6">决策偏好</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[{k:'speed',l:'决策速度',o:[['fast','快速'],['moderate','平衡'],['slow','深思']]},{k:'risk',l:'风险承受',o:[['conservative','保守'],['moderate','适中'],['aggressive','激进']]},{k:'density',l:'信息密度',o:[['low','简洁'],['moderate','适中'],['high','详细']]},{k:'horizon',l:'时间视角',o:[['short_term','短期'],['moderate','平衡'],['long_term','长期']]}].map(f => (
                <div key={f.k}>
                  <label className="block text-sm font-heading font-semibold text-ink mb-2">{f.l}</label>
                  <select value={(prefs as any)[f.k]} onChange={e => setPrefs({...prefs, [f.k]: e.target.value})} className="input">
                    {f.o.map(o => <option key={o[0]} value={o[0]}>{o[1]}</option>)}
                  </select>
                </div>
              ))}
            </div>
          </div>

          {/* Focus */}
          <div className="card !p-8 mb-8">
            <h2 className="font-heading text-xl font-bold text-ink mb-6">当前关注</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div><label className="block text-sm font-heading font-semibold text-ink mb-2">主要领域</label><input value={focus.primary} onChange={e => setFocus({...focus, primary: e.target.value})} className="input" /></div>
              <div><label className="block text-sm font-heading font-semibold text-ink mb-2">次要领域</label><input value={focus.secondary} onChange={e => setFocus({...focus, secondary: e.target.value})} className="input" /></div>
              <div><label className="block text-sm font-heading font-semibold text-ink mb-2">时间视角</label><select value={focus.horizon} onChange={e => setFocus({...focus, horizon: e.target.value})} className="input"><option value="short">短期</option><option value="medium">中期</option><option value="long">长期</option></select></div>
            </div>
          </div>

          {/* Save */}
          <div className="flex justify-end">
            <button onClick={handleSave} className="btn--primary">
              {saved ? '已保存' : '保存设置'}
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

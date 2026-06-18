'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/', label: '做决定', emoji: '🐱', desc: '问问我的意见' },
  { href: '/history', label: '回忆录', emoji: '📖', desc: '过去的决定' },
  { href: '/analysis', label: '洞察', emoji: '🔮', desc: '了解你自己' },
  { href: '/settings', label: '设置', emoji: '⚙️', desc: '调整我的认知' },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-[260px] h-screen fixed left-0 top-0 bg-kawaii-sidebar border-r-2 border-primary/10 p-5 z-40">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 mb-10 group">
          <div className="w-[50px] h-[50px] rounded-full bg-white flex items-center justify-center text-3xl shadow-kawaii-sm animate-bounce-slow group-hover:animate-none">
            🐱
          </div>
          <div>
            <h1 className="font-display text-2xl text-primary-dark">PCOS</h1>
            <p className="text-xs text-kawaii-text-light">你的认知决策伙伴</p>
          </div>
        </Link>

        {/* Nav Items */}
        <nav className="flex-1 space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-[15px] transition-all duration-300 ${
                  isActive
                    ? 'bg-white text-primary-dark shadow-kawaii-sm translate-x-1'
                    : 'text-kawaii-text hover:bg-white/50 hover:translate-x-1'
                }`}
              >
                <span className="text-2xl">{item.emoji}</span>
                <div>
                  <p className="font-semibold text-sm">{item.label}</p>
                  <p className="text-xs text-kawaii-text-light">{item.desc}</p>
                </div>
                {isActive && (
                  <div className="ml-auto w-2 h-2 rounded-full bg-primary animate-pulse-soft" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Bottom info */}
        <div className="mt-auto p-4 bg-accent/30 rounded-[20px] border border-accent">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xl">🌟</span>
            <p className="font-semibold text-sm text-kawaii-text">今日状态</p>
          </div>
          <p className="text-xs text-kawaii-text-light">继续保持思考的好习惯~</p>
        </div>
      </aside>

      {/* Mobile Top Bar */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-sm border-b-2 border-primary/10 px-4 py-3">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl animate-bounce-slow">🐱</span>
            <h1 className="font-display text-xl text-primary-dark">PCOS</h1>
          </Link>
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-lg"
          >
            {mobileOpen ? '✕' : '☰'}
          </button>
        </div>

        {mobileOpen && (
          <nav className="mt-3 pb-3 space-y-2 animate-slide-up">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-[15px] transition-all ${
                    isActive ? 'bg-primary/10 text-primary-dark' : 'text-kawaii-text'
                  }`}
                >
                  <span className="text-xl">{item.emoji}</span>
                  <span className="font-semibold text-sm">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        )}
      </div>

      {/* Mobile Bottom Nav */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-sm border-t-2 border-primary/10">
        <div className="flex justify-around py-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex flex-col items-center gap-1 py-1 px-3 rounded-xl transition-all ${
                  isActive ? 'text-primary-dark' : 'text-kawaii-text-light'
                }`}
              >
                <span className="text-xl">{item.emoji}</span>
                <span className="text-[10px] font-semibold">{item.label}</span>
                {isActive && <div className="w-1 h-1 rounded-full bg-primary" />}
              </Link>
            );
          })}
        </div>
      </div>
    </>
  );
}

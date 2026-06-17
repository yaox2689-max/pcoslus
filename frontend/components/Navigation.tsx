'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  BookOpen,
  History,
  BarChart3,
  Settings,
  Sparkles,
  Menu,
  X
} from 'lucide-react';

const navItems = [
  { href: '/', label: '做决策', icon: Sparkles },
  { href: '/history', label: '历史记录', icon: History },
  { href: '/analysis', label: '洞察分析', icon: BarChart3 },
  { href: '/settings', label: '我的设置', icon: Settings },
];

export default function Navigation() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      {/* Desktop Navigation */}
      <nav className="hidden md:flex fixed left-0 top-0 h-full w-64 flex-col bg-white/80 backdrop-blur-sm border-r border-warm-100 p-6">
        <div className="mb-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-warm-400 to-warm-500 flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-serif font-bold text-lg text-warm-800">PCOS</h1>
              <p className="text-xs text-warm-500">认知决策伙伴</p>
            </div>
          </Link>
        </div>

        <div className="flex-1 space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  isActive
                    ? 'bg-warm-100 text-warm-700 shadow-warm'
                    : 'text-warm-600 hover:bg-warm-50 hover:text-warm-700'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-warm-500' : 'text-warm-400'}`} />
                <span className="font-medium">{item.label}</span>
                {isActive && (
                  <div className="ml-auto w-2 h-2 rounded-full bg-warm-400" />
                )}
              </Link>
            );
          })}
        </div>

        <div className="mt-auto p-4 bg-sage-50 rounded-2xl">
          <p className="text-sm text-sage-700 font-medium">今日决策</p>
          <p className="text-2xl font-serif font-bold text-sage-600">3</p>
          <p className="text-xs text-sage-500 mt-1">继续保持思考的好习惯</p>
        </div>
      </nav>

      {/* Mobile Navigation */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-sm border-b border-warm-100">
        <div className="flex items-center justify-between p-4">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-warm-400 to-warm-500 flex items-center justify-center">
              <BookOpen className="w-4 h-4 text-white" />
            </div>
            <span className="font-serif font-bold text-warm-800">PCOS</span>
          </Link>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg hover:bg-warm-50 transition-colors"
          >
            {mobileMenuOpen ? (
              <X className="w-5 h-5 text-warm-600" />
            ) : (
              <Menu className="w-5 h-5 text-warm-600" />
            )}
          </button>
        </div>

        {mobileMenuOpen && (
          <div className="border-t border-warm-100 p-4 space-y-2 animate-fade-in">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                    isActive
                      ? 'bg-warm-100 text-warm-700'
                      : 'text-warm-600 hover:bg-warm-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>
        )}
      </div>

      {/* Mobile bottom navigation */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-sm border-t border-warm-100">
        <div className="flex justify-around p-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all duration-200 ${
                  isActive ? 'text-warm-600' : 'text-warm-400'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="text-xs font-medium">{item.label}</span>
                {isActive && (
                  <div className="w-1 h-1 rounded-full bg-warm-400" />
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </>
  );
}

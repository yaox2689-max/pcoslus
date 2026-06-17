import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PCOS - 你的认知决策伙伴',
  description: 'Personal Cognitive Operating System - 帮助你做出更好的决策',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen gradient-warm noise-bg">
        <div className="relative z-10">
          {children}
        </div>
      </body>
    </html>
  );
}

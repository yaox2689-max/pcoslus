import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PCOS — 认知决策伙伴',
  description: '温润如玉的决策引擎，帮你做出更好的选择',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN" className="scroll-smooth">
      <body className="min-h-screen bg-base text-ink antialiased">
        {children}
      </body>
    </html>
  );
}

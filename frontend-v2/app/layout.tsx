import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PCOS - 你的认知决策伙伴',
  description: '像一只温暖的小猫，陪你做每一个重要决定',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen">
        {children}
      </body>
    </html>
  );
}

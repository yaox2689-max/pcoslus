/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        base: 'var(--color-base)',
        surface: 'var(--color-surface)',
        'surface-alt': 'var(--color-surface-alt)',
        primary: {
          DEFAULT: 'var(--color-primary)',
          light: 'var(--color-primary-light)',
          dark: 'var(--color-primary-dark)',
        },
        secondary: 'var(--color-secondary)',
        accent: 'var(--color-accent)',
        ink: {
          DEFAULT: 'var(--color-ink)',
          light: 'var(--color-ink-light)',
          muted: 'var(--color-ink-muted)',
        },
        border: {
          DEFAULT: 'var(--color-border)',
          light: 'var(--color-border-light)',
        },
      },
      fontFamily: {
        heading: ['Plus Jakarta Sans', 'Noto Sans SC', 'sans-serif'],
        body: ['Outfit', 'Noto Sans SC', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        sm: '8px', md: '12px', lg: '16px',
        xl: '20px', '2xl': '28px', full: '9999px',
      },
      boxShadow: {
        sm: '0 1px 2px rgba(45,42,38,0.05)',
        md: '0 4px 12px rgba(45,42,38,0.08)',
        lg: '0 8px 24px rgba(45,42,38,0.12)',
        xl: '0 16px 48px rgba(45,42,38,0.16)',
        glow: '0 0 0 4px rgba(196,149,106,0.15)',
      },
      animation: {
        'fade-up': 'fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) forwards',
        'fade-scale': 'fadeScale 0.9s cubic-bezier(0.16,1,0.3,1) forwards',
        'bubble-in': 'bubbleIn 0.35s cubic-bezier(0.16,1,0.3,1) forwards',
        'bounce-subtle': 'bounceSubtle 2s ease-in-out infinite',
      },
      keyframes: {
        fadeUp: {
          from: { opacity: '0', transform: 'translateY(24px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        fadeScale: {
          from: { opacity: '0', transform: 'scale(0.92)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
        bubbleIn: {
          from: { opacity: '0', transform: 'scale(0.97)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
        bounceSubtle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
      },
    },
  },
  plugins: [],
};

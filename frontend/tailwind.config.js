/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        warm: {
          50: '#fdf8f0',
          100: '#f9eedd',
          200: '#f3d9b8',
          300: '#eabc85',
          400: '#e09a52',
          500: '#d97e2f',
          600: '#ca6524',
          700: '#a94d20',
          800: '#883e22',
          900: '#6e351e',
        },
        sage: {
          50: '#f4f7f4',
          100: '#e0ebe0',
          200: '#c2d7c2',
          300: '#96b896',
          400: '#6a966a',
          500: '#4a7a4a',
          600: '#3a6139',
          700: '#304e30',
          800: '#293f29',
          900: '#233523',
        },
        cream: {
          50: '#fefdfb',
          100: '#fdf9f0',
          200: '#faf1de',
          300: '#f5e4c4',
          400: '#eed0a0',
          500: '#e5b77a',
          600: '#d99a54',
          700: '#bc7d3f',
          800: '#996436',
          900: '#7d522f',
        },
      },
      fontFamily: {
        sans: ['Noto Sans SC', 'system-ui', 'sans-serif'],
        serif: ['Noto Serif SC', 'Georgia', 'serif'],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        'warm': '0 4px 20px -4px rgba(217, 126, 47, 0.15)',
        'warm-lg': '0 10px 40px -10px rgba(217, 126, 47, 0.2)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};

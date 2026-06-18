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
        primary: {
          DEFAULT: '#ff9e99',
          light: '#ffb7b2',
          dark: '#e88a85',
        },
        secondary: {
          DEFAULT: '#ffdac1',
          light: '#ffe8d6',
        },
        accent: {
          DEFAULT: '#e2f0cb',
          light: '#edf5dc',
        },
        kawaii: {
          bg: '#fff5f5',
          sidebar: '#fff0f0',
          text: '#6d6875',
          'text-light': '#a5a5a5',
          'bot-msg': '#f0f8ff',
          'user-msg': '#ffb7b2',
        },
      },
      fontFamily: {
        sans: ['Nunito', 'Microsoft YaHei', 'sans-serif'],
        display: ['ZCOOL KuaiLe', 'cursive'],
      },
      borderRadius: {
        'kawaii': '20px',
        'kawaii-lg': '30px',
      },
      boxShadow: {
        'kawaii': '0 8px 24px rgba(255, 183, 178, 0.2)',
        'kawaii-sm': '0 4px 12px rgba(255, 183, 178, 0.15)',
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'float': 'float 3s ease-in-out infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'fade-in': 'fadeIn 0.3s ease-out',
        'pulse-soft': 'pulseSoft 2s infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          from: { transform: 'translateX(100%)' },
          to: { transform: 'translateX(0)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
      },
    },
  },
  plugins: [],
};

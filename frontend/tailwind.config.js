/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        thunder: {
          bg:       '#0f0f1a',
          surface:  '#1a1a2e',
          card:     '#16213e',
          border:   '#0f3460',
          accent:   '#e94560',
          accent2:  '#53d8fb',
          text:     '#e2e8f0',
          muted:    '#94a3b8',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'typing': 'typing 1.2s steps(3) infinite',
      },
    },
  },
  plugins: [],
};

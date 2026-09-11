/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0d14',
        sidebar: '#111521',
        card: '#161b2a',
        accent: '#6366f1',
        'accent-hover': '#4f46e5',
        border: '#23293e',
        muted: '#94a3b8'
      }
    },
  },
  plugins: [],
}
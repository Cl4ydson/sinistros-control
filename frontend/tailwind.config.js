/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Habilita modo escuro baseado em classe
  theme: {
    extend: {
      colors: {
        // Cores do tema claro
        primary: {
          50:  '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // Cores personalizadas para modo escuro
        dark: {
          bg: {
            primary: '#1a1a1a',
            secondary: '#2d2d2d',
            tertiary: '#404040',
          },
          text: {
            primary: '#ffffff',
            secondary: '#a3a3a3',
            tertiary: '#737373',
          },
          border: {
            primary: '#404040',
            secondary: '#525252',
          }
        }
      },
      // Configurações de background para temas
      backgroundColor: {
        'light-primary': '#ffffff',
        'light-secondary': '#f3f4f6',
        'dark-primary': '#1a1a1a',
        'dark-secondary': '#2d2d2d',
      }
    },
  },
  plugins: [],
} 
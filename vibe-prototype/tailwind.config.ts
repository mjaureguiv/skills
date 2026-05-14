import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        sap: {
          blue: '#0070f2',
          'blue-hover': '#0064d9',
          'blue-active': '#0058c0',
          text: '#1d2d3e',
          label: '#556b82',
          border: '#d9d9d9',
          'border-light': '#eaecee',
          surface: '#ffffff',
          'surface-alt': '#f5f6f7',
          success: '#188918',
          warning: '#e76500',
          error: '#ee0000',
        },
      },
      fontFamily: {
        sap: ['"72"', '"72full"', 'Arial', 'Helvetica', 'sans-serif'],
      },
      borderRadius: {
        sap: '12px',
        'sap-sm': '8px',
        'sap-xs': '4px',
      },
      boxShadow: {
        sap: '0 0 1px rgba(11,41,70,0.32), 0 4px 4px rgba(42,82,121,0.14)',
        'sap-hover': '0 0 1px rgba(11,41,70,0.32), 0 8px 16px rgba(42,82,121,0.18)',
      },
    },
  },
  plugins: [],
}
export default config

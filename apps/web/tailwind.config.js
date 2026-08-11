/** @type {import('tailwindcss').Config} */
module.exports = {
  presets: [require('@edgerunner/tokens/preset')],
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx}',
    '../../packages/brand/src/**/*.tsx',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

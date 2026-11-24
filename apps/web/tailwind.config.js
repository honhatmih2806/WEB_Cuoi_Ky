/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        nvidia: {
          green: "#76B900",
          dark: "#041e00",
          glow: "#8be300"
        },
        apple: {
          titanium: "#E5D3B3",
          dark: "#1D1D1F",
          silver: "#F5F5F7"
        },
        titan: {
          bg: "#0B0F19",
          card: "#131B2E",
          border: "#1E293B",
          accent: "#38BDF8"
        }
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
      }
    },
  },
  plugins: [],
};

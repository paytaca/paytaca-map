// Import the Tailwind CSS Config type
/** @type {import('tailwindcss').Config} */
// @ts-ignore

// Export the configuration object
export default {
  darkMode: 'class',
  // Specify the files Tailwind should analyze for generating utility classes
  content: [
    "./index.html", // HTML file(s) to analyze
    "./src/**/*.{vue,js,ts,jsx,tsx}" // Vue, JavaScript, TypeScript files to analyze in the src directory
  ],
  // Customize Tailwind CSS theme
  theme: {
    // Extend or override the default theme here
    // screens: {
    //   sm: '425px',
    //   md: '768px',
    //   lg: '976px',
    //   xl: '1440px',
    // },
    extend: {
      colors: {
        // Paytaca brand blue (matches paytaca.com), not the old green theme.
        brand: {
          50: 'rgb(var(--brand-50) / <alpha-value>)',
          100: 'rgb(var(--brand-100) / <alpha-value>)',
          200: 'rgb(var(--brand-200) / <alpha-value>)',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
        },
        mango: {
          100: 'rgb(var(--mango-100) / <alpha-value>)',
          300: '#FFD074',
          500: '#FFB020',
          600: '#F09300',
          700: '#C97700',
        },
        coral: {
          100: 'rgb(var(--coral-100) / <alpha-value>)',
          300: '#FFA79B',
          500: '#FF6B5A',
          600: '#EE4936',
          700: '#C43526',
        },
        sky: {
          100: 'rgb(var(--sky-100) / <alpha-value>)',
          200: 'rgb(var(--sky-200) / <alpha-value>)',
          300: '#7FD6E9',
          500: '#2BB8D8',
          600: '#1A9CBB',
          700: '#147C96',
        },
        pink: {
          100: 'rgb(var(--pink-100) / <alpha-value>)',
          200: 'rgb(var(--pink-200) / <alpha-value>)',
          300: '#FFB3C7',
          500: '#FF7AA2',
          600: '#EE5A87',
          700: '#C33C67',
        },
        cloud: {
          DEFAULT: 'rgb(var(--cloud) / <alpha-value>)',
          deep: 'rgb(var(--cloud-deep) / <alpha-value>)',
        },
        card: 'rgb(var(--card) / <alpha-value>)',
        ink: {
          DEFAULT: 'rgb(var(--ink) / <alpha-value>)',
          muted: 'rgb(var(--ink-muted) / <alpha-value>)',
          faint: 'rgb(var(--ink-faint) / <alpha-value>)',
        },
        soft: 'rgb(var(--soft) / <alpha-value>)',
      },
      fontFamily: {
        display: ['"Rubik"', 'system-ui', 'sans-serif'],
        sans: ['"Rubik"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.25rem',
        '3xl': '1.75rem',
      },
      boxShadow: {
        pop: '0 10px 30px -8px rgba(37, 99, 235, 0.35)',
        card: '0 6px 20px -6px rgba(15, 23, 42, 0.14)',
        'card-hover': '0 16px 34px -10px rgba(29, 78, 216, 0.28)',
      },
    }
  },
  // Specify additional plugins for Tailwind CSS
  plugins: [
    // You can add any additional Tailwind CSS plugins here
  ],
};

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
        brand: {
          50: 'rgb(var(--brand-50) / <alpha-value>)',
          100: 'rgb(var(--brand-100) / <alpha-value>)',
          200: 'rgb(var(--brand-200) / <alpha-value>)',
          300: '#5FE3A3',
          400: '#2ED592',
          500: '#10C57E',
          600: '#0AA76C',
          700: '#088455',
          800: '#0A6A46',
          900: '#0B5639',
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
          100: '#FFE7EE',
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
        display: ['"Baloo 2"', 'ui-rounded', 'system-ui', 'sans-serif'],
        sans: ['"Plus Jakarta Sans"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.25rem',
        '3xl': '1.75rem',
      },
      boxShadow: {
        pop: '0 10px 30px -8px rgba(16, 197, 126, 0.45)',
        card: '0 6px 20px -6px rgba(18, 36, 30, 0.14)',
        'card-hover': '0 16px 34px -10px rgba(10, 167, 108, 0.34)',
      },
    }
  },
  // Specify additional plugins for Tailwind CSS
  plugins: [
    // You can add any additional Tailwind CSS plugins here
  ],
};

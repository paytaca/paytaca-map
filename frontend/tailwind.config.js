// Import the Tailwind CSS Config type
/** @type {import('tailwindcss').Config} */
// @ts-ignore

// Export the configuration object
export default {
  // Specify the files Tailwind should analyze for generating utility classes
  content: [
    "./index.html", // HTML file(s) to analyze
    "./src/**/*.{vue,js,ts,jsx,tsx}" // Vue, JavaScript, TypeScript files to analyze in the src directory
  ],
  // Customize Tailwind CSS theme
  theme: {
    // Extend or override the default theme here
    screens: {
      sm: '425px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },
    colors: {
      'blue': '#1fb6ff',
      'purple': '#7e5bef',
      'pink': '#ff49db',
      'orange': '#ff7849',
      'green': '#13ce66',
      'yellow': '#ffc82c',
      'gray-dark': '#273444',
      'gray': '#8492a6',
      'gray-light': '#d3dce6',
      'bg-dark': '#1E293B',
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    extend: {
      spacing: {
        '128': '32rem',
        '144': '36rem',
      }
    }
  },
  // Specify additional plugins for Tailwind CSS
  plugins: [
    // You can add any additional Tailwind CSS plugins here
  ],
};

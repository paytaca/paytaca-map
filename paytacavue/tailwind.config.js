// Import the Tailwind CSS Config type
/** @type {import('tailwindcss').Config} */
// @ts-ignore

// Export the configuration object
module.exports = {
  // Specify the files Tailwind should analyze for generating utility classes
  content: [
    "./index.html", // HTML file(s) to analyze
    "./src/**/*.{vue,js,ts,jsx,tsx}" // Vue, JavaScript, TypeScript files to analyze in the src directory
  ],
  // Customize Tailwind CSS theme
  theme: {
    // Extend or override the default theme here
    extend: {
      // You can add customizations here, such as new colors, fonts, spacing, etc.
    },
  },
  // Specify additional plugins for Tailwind CSS
  plugins: [
    // You can add any additional Tailwind CSS plugins here
  ],
};

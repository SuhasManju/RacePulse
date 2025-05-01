/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{html,js,ts,jsx,tsx}", // For your frontend components
        "./index.html", // If you have an index.html in your frontend root
        "../../templates/**/*.html",       // For your top-level Django templates
        "../../**/templates/**/*.html",    // To catch templates in subdirectories of your apps (like Standing/templates/)
    ],
    theme: {
        extend: {},
    },
    plugins: [],
};
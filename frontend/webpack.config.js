// webpack.config.js
const path = require('path');

module.exports = {
    entry: './src/index.js',  // Path to your entry file
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, '../static/js'), // Output to Django's static directory
    },
    // Add loaders and plugins as needed
};
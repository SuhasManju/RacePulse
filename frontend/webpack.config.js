// webpack.config.js
const path = require('path');

module.exports = {
    entry: './src/index.js',  // Path to your entry file
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, '../static/js'), // Output to Django's static directory
    },
    module: {
        rules: [
            {
                test: /\.(png|jpe?g|gif|svg)$/i,
                type: 'asset/resource', // <-- Webpack 5 built-in asset handling
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'], // if you're importing Leaflet CSS
            },
        ],
    },
    // Add loaders and plugins as needed
};
const resolve = require('path').resolve;
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = {
    devtool: 'eval-source-map',
    mode: 'development',
    entry: './app/static/src/scripts/scripts.js',
    output: {
        path: resolve(__dirname, './app/static/dist'),
        filename: 'scripts.bundle.js'
    },
    mode: 'development',
    resolve: {
        extensions: ['.js', '.css']
    },
    module: {
        rules: [
            {
                test: /\.js?/,
                loader: 'babel-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    // { loader: "style-loader" },
                    { loader: MiniCssExtractPlugin.loader },
                    { loader: "css-loader" },
                    { loader: "postcss-loader" },
                    {
                        loader: "sass-loader",
                        options: { implementation: require("sass") }
                    },
                    { loader: "import-glob-loader" }
                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "bundle.css"
        })
    ]
};

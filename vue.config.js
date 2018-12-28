// vue.config.js
module.exports = {
    // options ...
    baseUrl : '/',  // 等同于webpack的output.publicPath, 但仍有额外用处
    outputDir : 'dest', // build后的文件生成目录(webpack的output.path)
    assetsDir : '', //相对于outputDir的目录用于生成assets
    indexPath : 'index.html', // 指定index.html的build路径(相对于outputDir), 可以使用绝对路径
    filenameHashing : true,   // 默认情况下，生成的assets包含hashes，这依赖vue cli自动生成index.html来支持。(若不使用vue cli自动生成index.html那么就把这个选项设为false)
    pages: undefined, // build a multi page app, 会用到html-webpack-plugin
    // pages: {
    //     index: {
    //         // entry for the page
    //         entry: 'src/index/main.js',
    //         // the source template
    //         template: 'public/index.html',
    //         // output as dist/index.html
    //         filename: 'index.html',
    //         // when using title option,
    //         // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
    //         title: 'Index Page',
    //         // chunks to include on this page, by default includes
    //         // extracted common chunks and vendor chunks.
    //         chunks: ['chunk-vendors', 'chunk-common', 'index']
    //     },
    //     // when using the entry-only string format,
    //     // template is inferred to be `public/subpage.html`
    //     // and falls back to `public/index.html` if not found.
    //     // Output filename is inferred to be `subpage.html`.
    //     subpage: 'src/subpage/main.js'
    // }
    // lintOnSave : true, 
    runtimeCompiler : false,
    transpileDependencies : [], // babel-loader默认忽略node_modules的所有文件，若需要显示的处理某些文件，则将他们添加在这里
    productionSourceMap : true, // 禁用后可以加速production builds
    crossorigin: undefined, // 对于html-webpack-plugin注入的link和script添加crossorigin属性
    integrity: false, // 对于html-webpack-plugin注入的link和script添加integrity属性, 提高安全性
    // configureWebpack : Object|Function, // https://github.com/vuejs/vue-cli/blob/dev/docs/guide/webpack.md#simple-configuration
    // configureWebpack: config => {
    // },
    // 调整webpack配置
    // chainWebpack: Function, // https://github.com/vuejs/vue-cli/blob/dev/docs/guide/webpack.md#chaining-advanced
    chainWebpack: config => {

    },
    css: { // https://github.com/vuejs/vue-cli/blob/dev/docs/guide/css.md#css-modules
        modules: false,
        extract: process.env.NODE_ENV == 'production',
        sourceMap: false,
        loaderOptions: {},
    },
    devServer: { // webpack-dev-server用到的任意选项
        // proxy: 'http://localhost:8080',
        // proxy: { // http-proxy-middleware
        //     '^/api': {
        //         target: '<url>',
        //         ws: true,
        //         changeOrigin: true
        //     },
        //     '^/foo': {
        //         target: '<other_url>'
        //     }
        // },
    }, 
    parallel: require('os').cpus().length > 1, // 指定是否将thread-loader用于babel或ts转换
    // pwa:{}, // PWA Plugin选项
    pluginOptions: { // 
        // foo : {} // 提供第三方插件的选项配置
    }
}

// Babel: vue使用babel.config.js(babel 7)而非.babelrc或babel处理加载配置
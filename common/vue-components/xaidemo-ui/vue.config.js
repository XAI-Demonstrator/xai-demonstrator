module.exports = {
    chainWebpack: config => {
        config.module
            .rule('vue')
            .use('vue-svg-inline-loader')
            .loader('vue-svg-inline-loader')
            .options({ /* ... */})

        if (process.env.NODE_ENV === 'development') {
            config.plugin('html')
                .tap(args => {
                    args[0].title = "XAI-Demonstrator";
                    args[0].favicon = './public/favicon.ico';
                    return args
                })
        }
    }
}

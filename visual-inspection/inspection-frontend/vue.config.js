module.exports = {
    publicPath: process.env.VUE_APP_PUBLIC_PATH,
    // Prevent errors when installing xaidemo-ui locally
    // https://cli.vuejs.org/guide/troubleshooting.html#symbolic-links-in-node-modules
    chainWebpack: (config) => {
        config.resolve.symlinks(false)

        config.plugin('html')
            .tap(args => {
                args[0].title = "XAI-Demonstrator";
                args[0].favicon = './public/favicon.ico';
                return args
            })

        config.module
            .rule('i18n')
            .resourceQuery(/blockType=i18n/)
            .type('javascript/auto')
            .use('i18n')
            .loader('@intlify/vue-i18n-loader')
    }
}

module.exports = {
    publicPath: process.env.VUE_APP_PUBLIC_PATH,
    // Prevent errors when installing xaidemo-ui locally
    // https://cli.vuejs.org/guide/troubleshooting.html#symbolic-links-in-node-modules
    chainWebpack: (config) => {
        config.resolve.symlinks(false)

        config.plugin('html')
            .tap(args => {
                args[0].title = "XAI-Demonstrator";
                args[0].favicon = './static/favicon.ico';
                return args
            })
    }
}

module.exports = {
    publicPath: process.env.VUE_APP_PUBLIC_PATH,
    // Prevent errors when installing xaidemo-ui locally
    // https://cli.vuejs.org/guide/troubleshooting.html#symbolic-links-in-node-modules
    chainWebpack: (config) => {
        config.resolve.symlinks(false)

        // Validate the VUE_APP_IMAGE_SEQUENCE_MODE
        const availableSequenceModes = ['classic', 'basic', 'recommender']
        if (!availableSequenceModes.includes(process.env.VUE_APP_IMAGE_SEQUENCE_MODE)) {
            throw "VUE_APP_IMAGE_SEQUENCE_MODE has to be set to one of the following values: " + availableSequenceModes
        }

        config.plugin('html')
            .tap(args => {
                args[0].title = "XAI-Demonstrator";
                args[0].favicon = './public/favicon.ico';
                return args
            })
    }
}

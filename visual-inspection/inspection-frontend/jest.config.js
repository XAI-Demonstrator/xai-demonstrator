module.exports = {
    preset: '@vue/cli-plugin-unit-jest',
    setupFilesAfterEnv: [
        "./jest.setup.js",
    ],
    transform: {
        "^.+.js$": "babel-jest",
        ".*.(vue)$": "@vue/vue3-jest"
    },
}

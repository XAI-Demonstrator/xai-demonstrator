module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  setupFilesAfterEnv: [
     './jest.setup.js',
  ],
  transform: {
    "^.+\\.vue$": "vue-jest",
  },
}

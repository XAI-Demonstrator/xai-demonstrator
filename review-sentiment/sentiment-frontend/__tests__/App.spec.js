import App from './../src/App.vue'

describe('App', () => {
    it('has data', () => {
        expect(typeof App.data).toBe('function')
    })
})

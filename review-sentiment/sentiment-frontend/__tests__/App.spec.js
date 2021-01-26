import {createLocalVue, shallowMount} from '@vue/test-utils'
import App from "@/App";

describe('Component', () => {

    const localVue = createLocalVue()
    const wrapper = shallowMount(App, localVue)

    wrapper.vm.$refs = {
        'analyzer': {resetComponent: jest.fn()},
        'explainer': {resetComponent: jest.fn()}
    }


    it('review text changed', () => {
        wrapper.vm.reviewTextChanged('nice restaurant')

        expect(wrapper.vm.$data.reviewText).toBe('nice restaurant')
        expect(wrapper.vm.$data.numberOfStars).toBeNull()
    })

    it('complete analysis', () => {
        wrapper.vm.analysisCompleted(4)

        expect(wrapper.vm.$data.numberOfStars).toBe(4)
    })

    it('requested analysis', () => {
        wrapper.setData({numberOfStars: 3})

        wrapper.vm.analysisRequested()

        expect(wrapper.vm.$data.numberOfStars).toBeNull()
    })

    it('if review text is set, use it', () => {
        wrapper.setData({reviewText: 'great view!'})

        expect(wrapper.vm.reviewTextToAnalyze).toBe('great view!')
    })

    it('if review text is not set, use default', () => {
        wrapper.setData({reviewText: null, reviewTopic: 'movie'})

        expect(wrapper.vm.reviewTextToAnalyze).toBe(wrapper.vm.$data.defaultReviews['movie'])
    })

})


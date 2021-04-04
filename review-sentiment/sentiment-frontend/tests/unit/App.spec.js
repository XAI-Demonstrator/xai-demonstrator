import {createLocalVue, shallowMount} from '@vue/test-utils'
import App from "@/App";
import axios from "axios";
import flushPromises from "flush-promises";

jest.mock('axios');

describe('App.vue', () => {

    const response = {
        data: {
            status: 'loaded'
        }
    }
    const loader = axios.get.mockImplementation(() => Promise.resolve(response))

    const localVue = createLocalVue()
    let wrapper = shallowMount(App, localVue)

    beforeEach(() => {
            wrapper = shallowMount(App, localVue);
            wrapper.vm.$refs = {
                'analyzer': {resetComponent: jest.fn()},
                'explainer': {resetComponent: jest.fn()}
            }
        }
    )

    it('triggers backend loading after mounting', async () => {
        loader.mockClear()

        await shallowMount(App, localVue)
        await flushPromises()

        expect(loader.mock.calls.length).toBe(1)
    })


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


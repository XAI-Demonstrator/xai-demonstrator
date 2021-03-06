import {createLocalVue, shallowMount} from '@vue/test-utils'
import AnalyzeReview from "@/components/AnalyzeReview";
import axios from 'axios';
import flushPromises from 'flush-promises';

jest.mock('axios');

describe('AnalyzeReview.vue', () => {

    const localVue = createLocalVue()
    let wrapper = shallowMount(AnalyzeReview, localVue);

    beforeEach(() => {
            wrapper = shallowMount(AnalyzeReview, localVue);
        }
    )

    it('component reset', async () => {
        await wrapper.setData({numOfStars: 5})

        await wrapper.vm.resetComponent()

        expect(wrapper.vm.$data.numOfStars).toBeNull()
        expect(wrapper.find('.the-sentiment').exists()).toBe(false)
        expect(wrapper.find('button').exists()).toBe(true)
        expect(wrapper.find('button').attributes('disabled')).toBeUndefined()
    })

    it('prediction is requested from backend', async () => {
        await wrapper.setProps({reviewText: "Boring food..."})

        const response = {
            data: {
                prediction: [
                    0.1,
                    0.5,
                    0.1,
                    0.1,
                    0.2
                ]
            }
        }
        axios.post.mockImplementationOnce(() => Promise.resolve(response))

        const button = wrapper.find('button')
        await button.trigger('click')

        expect(button.attributes('disabled')).toBe('disabled')

        await flushPromises()

        expect(wrapper.vm.$data.numOfStars).toBe(2)
        expect(wrapper.find('.sentiment-stars').findAll('img.my-star').length).toEqual(5)

    })

})

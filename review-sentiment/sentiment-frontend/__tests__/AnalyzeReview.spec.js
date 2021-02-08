import {createLocalVue, shallowMount} from '@vue/test-utils'
import AnalyzeReview from "@/components/AnalyzeReview";
import axios from 'axios';
import flushPromises from 'flush-promises';
import BarChart from "@/components/BarChart";

jest.mock('axios');

describe('Component', () => {

    const localVue = createLocalVue()
    let wrapper = shallowMount(AnalyzeReview, localVue);

    beforeEach(() => {
            wrapper = shallowMount(AnalyzeReview, localVue);
        }
    )

    it('component reset', () => {
        wrapper.setData({numOfStars: 5})

        wrapper.vm.resetComponent()

        expect(wrapper.vm.$data.numOfStars).toBeNull()
    })

    it('prediction is requested', async () => {
        wrapper.setProps({reviewText: "Boring food..."})

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

        wrapper.vm.requestAnalysis()
        await flushPromises()

        expect(wrapper.vm.$data.numOfStars).toBe(2)
    })

})

import { shallowMount} from "@vue/test-utils";
import InspectImage from "@/components/InspectImage";
import {MultiBounce} from "@xai-demonstrator/xaidemo-ui";
import axios from 'axios';
import flushPromises from 'flush-promises';

jest.mock('axios');

describe('App.vue', () => {
    it('shows bouncing dots while waiting for prediction', async () => {
        await wrapper.setData({waitingForExplanation: true})

        expect(wrapper.findComponent(SpinningIndicator).exists()).toBe(true)

        await wrapper.setData({waitingForExplanation: false})

        expect(wrapper.findComponent(MultiBounce).exists()).toBe(false)
    })

    it('requests a prediction', async () => {
        const response = {
            data: {
                class_label: 'israel'
            }
        }
        axios.post.mockImplementationOnce(() => Promise.resolve(response))

        await wrapper.vm.predict('fake-blob')
        await flushPromises()

        expect(wrapper.vm.$data.prediction).toStrictEqual('israel')
        expect(wrapper.emitted('inspection-completed')).toBeTruthy()
    })

    it('shows prediction only when it exists', async () => {
        await wrapper.setData({prediction: 'israel'})

        expect(wrapper.findComponent('').isVisible()).toBe(true)

        await wrapper.setData({prediction: null})

        expect(wrapper.find('p').isVisible()).toBe(false)
    })

    it('shows user answer only when it exists', async () => {
        await wrapper.setData({user_answer: 'israel'})

        expect(wrapper.findComponent('').isVisible()).toBe(true)

        await wrapper.setData({user_answer: null})

        expect(wrapper.find('p').isVisible()).toBe(false)
    })

    it('shows the correct text only when it exists', async () => {
        await wrapper.setData({user_answer: 'israel'})
        await wrapper.setData({class_label: 'israel'})

        expect(wrapper.findComponent('').isVisible()).toBe(true)
        expect(wrapper.find('p').isVisible()).toBe(false)

        await wrapper.setData({user_answer: 'germany'})
        await wrapper.setData({class_label: 'israel'})

        xpect(wrapper.findComponent('').isVisible()).toBe(true)
        expect(wrapper.find('p').isVisible()).toBe(false)
    })

})
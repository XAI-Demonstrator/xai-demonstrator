import {createLocalVue, shallowMount} from "@vue/test-utils";
import InspectImage from "@/components/InspectImage";
import {MultiBounce} from "@xai-demonstrator/xaidemo-ui";
import axios from 'axios';
import flushPromises from 'flush-promises';

jest.mock('axios');

describe('InspectImage.vue', () => {

    const localVue = createLocalVue()
    let wrapper = shallowMount(InspectImage, localVue);

    beforeEach(() => {
            wrapper = shallowMount(InspectImage, localVue);
            axios.CancelToken.source.mockImplementation(() => {
                return {token: 'abcde'}
            })
        }
    )

    it('shows bouncing dots while waiting for prediction', async () => {
        await wrapper.setData({prediction: null})

        expect(wrapper.findComponent(MultiBounce).exists()).toBe(true)

        await wrapper.setData({prediction: 'rain'})

        expect(wrapper.findComponent(MultiBounce).exists()).toBe(false)
    })

    it('shows prediction only when it exists', async () => {
        await wrapper.setProps({currentPrediction: true})
        await wrapper.setData({prediction: 'sunshine'})

        expect(wrapper.find('p').isVisible()).toBe(true)

        await wrapper.setData({prediction: null})

        expect(wrapper.find('p').isVisible()).toBe(false)
    })

    it('hides prediction if it is not current', async () => {
        await wrapper.setData({prediction: 'sunshine'})
        await wrapper.setProps({currentPrediction: true})

        expect(wrapper.find('p').isVisible()).toBe(true)

        await wrapper.setProps({currentPrediction: false})

        expect(wrapper.find('p').isVisible()).toBe(false)
    })

    it('requests a prediction', async () => {
        const response = {
            data: {
                class_label: 'foggy'
            }
        }
        axios.post.mockImplementationOnce(() => Promise.resolve(response))

        await wrapper.vm.predict('fake-blob')
        await flushPromises()

        expect(wrapper.vm.$data.prediction).toStrictEqual('foggy')
        expect(wrapper.emitted('inspection-completed')).toBeTruthy()
    })

    it('handles unavailable backend gracefully', async () => {
        axios.post.mockImplementationOnce(() => Promise.reject('some-error'))

        await wrapper.vm.predict('fake-blob')
        await flushPromises()

        expect(wrapper.vm.$data.prediction).toBeNull()
        expect(wrapper.emitted('inspection-completed')).toBeFalsy()
    })

    it('CancelToken is added to cancelArray upon each request', async () => {
        const response = {
            data: {
                class_label: 'foggy'
            }
        }
        axios.post.mockImplementationOnce(() => Promise.resolve(response))
        axios.CancelToken.source.mockImplementationOnce(() => {
            return {token: 'abcde'}
        })

        await wrapper.vm.predict('fake-blob')

        expect(wrapper.vm.$data.cancelArray.length).toBe(1)
        expect(wrapper.vm.$data.cancelArray[0]).toBe('abcde')
    })

    it('all pending requests are canceled before a new request is made', async () => {
        const firstToken = {cancel: jest.fn()}
        const secondToken = {cancel: jest.fn()}
        await wrapper.setData({cancelArray: [firstToken, secondToken]})

        axios.CancelToken.source.mockImplementationOnce(() => {
            return {token: 'abcde'}
        })

        const response = {
            data: {
                class_label: 'windy'
            }
        }
        axios.post.mockImplementation(() => Promise.resolve(response))

        await wrapper.vm.predict('fake-blob')

        expect(firstToken.cancel.mock.calls.length).toBe(1)
        expect(secondToken.cancel.mock.calls.length).toBe(1)
        expect(wrapper.vm.$data.cancelArray.length).toBe(1)
        expect(wrapper.vm.$data.cancelArray[0]).toBe('abcde')
    })

})

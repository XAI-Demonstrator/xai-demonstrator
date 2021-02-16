import {shallowMount, createLocalVue} from "@vue/test-utils";
import ExplainInspection from "@/components/ExplainInspection";
import {MultiBounce} from "@xai-demonstrator/xaidemo-ui";
import axios from "axios";
import flushPromises from "flush-promises";

jest.mock('axios');

describe('ExplainInspection.vue', () => {

    const {location} = window

    beforeAll(() => {
            delete window.location

            window.location = {
                href: '',
                search: ''
            }
        }
    )

    afterAll(() => {
        window.location = location
    })

    const localVue = createLocalVue()
    let wrapper = shallowMount(ExplainInspection, localVue);

    beforeEach(() => {
        wrapper = shallowMount(ExplainInspection, localVue);
    });

    afterEach(() => {
        jest.resetAllMocks()
    });

    it('disables button if prediction is not ready', async () => {
        await wrapper.setProps({predictionReady: false})

        expect(wrapper.find('button').attributes('disabled')).toBe('disabled')
    })

    it('enables button if prediction is ready', async () => {
        await wrapper.setProps({predictionReady: true})

        expect(wrapper.find('button').attributes('disabled')).toBeUndefined()
    })

    it('show bouncing dots while waiting for explanation', async () => {
        await wrapper.setData({waitingForExplanation: true})

        expect(wrapper.findComponent(MultiBounce).exists()).toBe(true)

        await wrapper.setData({waitingForExplanation: false})

        expect(wrapper.findComponent(MultiBounce).exists()).toBe(false)
    })

    it('button click triggers explanation-requested', async () => {
        await wrapper.setProps({predictionReady: true})

        const button = wrapper.find('button')

        await button.trigger('click')

        expect(wrapper.emitted('explanation-requested')).toBeTruthy()
    })

    it('requests an explanation', async () => {
        const response = {
            data: {
                image: 'data:image/png;base64,'
            }
        }
        axios.post.mockImplementationOnce(() => Promise.resolve(response))

        await wrapper.vm.explain('fake-blob')
        await flushPromises()

        expect(wrapper.emitted('explanation-received')).toBeTruthy()
        expect(wrapper.emitted('explanation-received')[0][0]).toStrictEqual('data:image/png;base64,')
    })

    it('handles unavailable backend gracefully', async () => {
        axios.post.mockImplementationOnce(() => Promise.reject('some-error'))

        await wrapper.vm.explain('fake-blob')
        await flushPromises()

        expect(wrapper.emitted('explanation-received')).toBeFalsy()
        expect(wrapper.vm.$data.waitingForExplanation).toBe(false)
    })

    it('passes query parameters to backend', async () => {
        window.location.search = "?method=lime&explainer.num_samples=20"

        const response = {
            data: {
                image: 'data:image/png;base64,'
            }
        }

        const expected = new FormData();
        expected.append("method", "lime")
        expected.append("settings", JSON.stringify({"explainer": {"num_samples": "20"}}))

        const mockPost = axios.post.mockImplementationOnce(() => Promise.resolve(response))

        await wrapper.vm.explain('fake-blob')
        await flushPromises()

        expect(mockPost).toHaveBeenCalled()
        expect(mockPost.mock.calls[0][0]).toStrictEqual('/explain')

        const payload = mockPost.mock.calls[0][1]

        for (const pair of expected.entries()) {
            console.log(pair, payload.get(pair[0]))
            expect(payload.has(pair[0])).toBe(true)
            expect(payload.get(pair[0])).toEqual(pair[1])
        }

    })

})

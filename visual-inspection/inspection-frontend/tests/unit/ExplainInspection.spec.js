import {shallowMount} from "@vue/test-utils";
import ExplainInspection from "@/components/ExplainInspection";
import {MultiBounce} from "@xai-demonstrator/xaidemo-ui";
import axios from "axios";
import flushPromises from "flush-promises";

jest.mock('axios');


function firstMatchesSecond(first, second) {
    for (const pair of first.entries()) {
        console.log(pair, first.get(pair[0]))
        expect(second.has(pair[0])).toBe(true)
        expect(second.get(pair[0])).toEqual(pair[1])
    }
}

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

    let wrapper = shallowMount(ExplainInspection);

    beforeEach(() => {
        wrapper = shallowMount(ExplainInspection);
    });

    afterEach(() => {
        jest.resetAllMocks()
    });

    it('disables button if prediction is not ready', async () => {
        await wrapper.setProps({predictionReady: false})

        expect(wrapper.find('button').element.disabled).toBeTruthy()
    })

    it('enables button if prediction is ready', async () => {
        await wrapper.setProps({predictionReady: true})

        expect(wrapper.find('button').element.disabled).toBeFalsy()
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
        expected.append("file", "fake-blob")
        expected.append("method", "lime")
        expected.append("settings", JSON.stringify({"explainer": {"num_samples": "20"}}))

        const mockPost = axios.post.mockImplementationOnce(() => Promise.resolve(response))

        await wrapper.vm.explain('fake-blob')
        await flushPromises()

        expect(mockPost).toHaveBeenCalled()
        expect(mockPost.mock.calls[0][0]).toStrictEqual('/explain')

        const payload = mockPost.mock.calls[0][1]

        firstMatchesSecond(expected, payload)
        firstMatchesSecond(payload, expected);
    })

    it('only adds settings if specified', async () => {
        window.location.search = "?method=lime"

        const response = {
            data: {
                image: 'data:image/png;base64,'
            }
        }

        const expected = new FormData();
        expected.append("method", "lime")

        const mockPost = axios.post.mockImplementationOnce(() => Promise.resolve(response))

        await wrapper.vm.explain('fake-blob')
        await flushPromises()

        expect(mockPost).toHaveBeenCalled()
        expect(mockPost.mock.calls[0][0]).toStrictEqual('/explain')

        const payload = mockPost.mock.calls[0][1]

        expect(payload.has('method')).toBe(true)
        expect(payload.has('settings')).toBe(false)
    })

    it('ignores embedded parameter', async () => {
        window.location.search = "?embedded"

        const response = {
            data: {
                image: 'data:image/png;base64,'
            }
        }

        const expected = new FormData();
        expected.append("method", "lime")

        const mockPost = axios.post.mockImplementationOnce(() => Promise.resolve(response))

        await wrapper.vm.explain('fake-blob')
        await flushPromises()

        expect(mockPost).toHaveBeenCalled()
        expect(mockPost.mock.calls[0][0]).toStrictEqual('/explain')

        const payload = mockPost.mock.calls[0][1]

        expect(payload.has('method')).toBe(false)
        expect(payload.has('settings')).toBe(false)
    })

})

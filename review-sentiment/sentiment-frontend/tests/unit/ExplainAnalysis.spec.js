import {createLocalVue, shallowMount} from '@vue/test-utils'
import ExplainAnalysis from "@/components/ExplainAnalysis";
import axios from "axios";
import flushPromises from 'flush-promises';

jest.mock('axios');

describe('ExplainAnalysis.vue', () => {

    const localVue = createLocalVue()
    let wrapper = shallowMount(ExplainAnalysis, localVue);

    beforeEach(() => {
            wrapper = shallowMount(ExplainAnalysis, localVue);
        }
    )

    it('component reset', async () => {
        await wrapper.setData({
            explanationResult: [
                {word: "Nice", score: 0.5},
                {word: "movie", score: "-0.1"}
            ]
        })

        wrapper.vm.resetComponent()

        expect(wrapper.vm.$data.explanationResult).toBeNull()
    })

    it('explanation is requested with default method', async () => {
        await wrapper.setProps({
            reviewText: "Boring food...",
        })
        await wrapper.setData({
            backendUrl: ""
        })

        const response = {
            data: {
                explanation: [
                    ["Boring", 0.7],
                    ["food", 0.3],
                    [".", 0.0],
                    [".", 0.0],
                    [".", 0.0]
                ]
            }
        }
        const mockPost = axios.post.mockImplementationOnce(() => Promise.resolve(response))

        const button = wrapper.find('button')
        await button.trigger('click')

        expect(button.attributes('disabled')).toBe('disabled')

        await flushPromises()

        expect(wrapper.vm.$data.explanationResult).toStrictEqual(
            [
                {word: "Boring", score: 0.7},
                {word: "food", score: 0.3},
                {word: ".", score: 0.0},
                {word: ".", score: 0.0},
                {word: ".", score: 0.0}
            ]
        )
        expect(mockPost).toBeCalledWith("/explain", {"text": "Boring food..."})

    })

    it('explanation is requested with specified method', async () => {
        global.window = Object.create(window)
        Object.defineProperty(window, 'location', {
            value: {
                href: "",
                search: "?method=random"
            }
        });

        await wrapper.setProps({
            reviewText: "Boring food..."
        })

        await wrapper.setData({
            backendUrl: ""
        })

        const response = {
            data: {
                explanation: [
                    ["Boring", 0.7],
                    ["food", 0.3],
                    [".", 0.0],
                    [".", 0.0],
                    [".", 0.0]
                ]
            }
        }
        const mockPost = axios.post.mockImplementationOnce(() => Promise.resolve(response))

        const button = wrapper.find('button')
        await button.trigger('click')

        expect(button.attributes('disabled')).toBe('disabled')

        await flushPromises()

        expect(wrapper.vm.$data.explanationResult).toStrictEqual(
            [
                {word: "Boring", score: 0.7},
                {word: "food", score: 0.3},
                {word: ".", score: 0.0},
                {word: ".", score: 0.0},
                {word: ".", score: 0.0}
            ]
        )
        expect(mockPost).toBeCalledWith("/explain", {
            "text": "Boring food...",
            "method": "random"
        })

    })

})

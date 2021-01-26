import {createLocalVue, shallowMount} from '@vue/test-utils'
import ExplainAnalysis from "@/components/ExplainAnalysis";
import axios from "axios";
import flushPromises from 'flush-promises';

jest.mock('axios');

describe('Component', () => {

    const localVue = createLocalVue()
    const wrapper = shallowMount(ExplainAnalysis, localVue);

    it('component reset', () => {
        wrapper.setData({
            explanationResult: [
                {word: "Nice", score: 0.5},
                {word: "movie", score: "-0.1"}
            ]
        })

        wrapper.vm.resetComponent()

        expect(wrapper.vm.$data.explanationResult).toBeNull()
    })

    it('explanation is requested', async () => {
        wrapper.setProps({reviewText: "Boring food..."})

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
        axios.post.mockImplementationOnce(() => Promise.resolve(response))

        wrapper.vm.requestExplanation()
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

    })

})

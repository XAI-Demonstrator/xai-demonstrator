import {createLocalVue, shallowMount} from '@vue/test-utils'
import BarChart from '@/components/BarChart.vue'

describe('Component', () => {

    const localVue = createLocalVue()
    let wrapper = shallowMount(BarChart, localVue);

    beforeEach(() => {
            wrapper = shallowMount(BarChart, localVue);
        }
    )

    it('scaling factor for empty explanation is 1', () => {
        const explanation = []
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(1.0)
    })

    it('explanations with scores above minLength are not scaled', async () => {
        await wrapper.setProps({minLengthOfLongestBar: 0.8})
        const explanation = [{"word": "the", "score": 0.9}, {"word": "world", "score": 0.7}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(1.0)
    })

    it('explanations with scores below minLength are scaled', async () => {
        await wrapper.setProps({minLengthOfLongestBar: 0.8})
        const explanation = [{"word": "the", "score": 0.3}, {"word": "world", "score": 0.4}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(2.0)
    })

    it('explanations with negative scores above minLength are scaled', async () => {
        await wrapper.setProps({minLengthOfLongestBar: 0.8})
        const explanation = [{"word": "the", "score": -0.2}, {"word": "world", "score": 0.1}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(4.0)
    })

    it('explanations with negative scores below minLength are scaled', async () => {
        await wrapper.setProps({minLengthOfLongestBar: 0.8})
        const explanation = [{"word": "the", "score": 0.5}, {"word": "world", "score": -0.9}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(1.0)
    })

    it('explanations are scaled', async () => {
        await wrapper.setProps({minLengthOfLongestBar: 0.5})
        const explanation = [{"word": "the", "score": -0.25}, {"word": "world", "score": 0.1}]
        expect(wrapper.vm.rescaleScores(explanation)).toStrictEqual(
            [{"word": "the", "score": -0.50}, {"word": "world", "score": 0.2}])
    })

    it('explanations are sorted', () => {
        const explanation = [
            {"word": "the", "score": -0.25},
            {"word": "world", "score": 0.7},
            {"word": "watches", "score": 0.2}
        ]
        expect(wrapper.vm.sortByScore(explanation)).toStrictEqual(
            [
                {"word": "world", "score": 0.7},
                {"word": "the", "score": -0.25},
                {"word": "watches", "score": 0.2}])
    })

})

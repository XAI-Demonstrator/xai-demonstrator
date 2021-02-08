import {createLocalVue, shallowMount} from '@vue/test-utils'
import TextHighlight from "@/components/TextHighlight";


describe('Component', () => {

    const localVue = createLocalVue()
    let wrapper = shallowMount(TextHighlight, localVue);

    beforeEach(() => {
        wrapper = shallowMount(TextHighlight, localVue)
    })

    it('HSL is calculated', async () => {
        await wrapper.setProps({preScaler: 1.0})
        expect(wrapper.vm.calcHSL(1.0)).toBe('hsl(' + 174 + ',100%,' + 27 + '%)')
        expect(wrapper.vm.calcHSL(0.5)).toBe('hsl(' + 174 + ',100%,' + 13.5 + '%)')
        expect(wrapper.vm.calcHSL(-0.5)).toBe('hsl(' + 0 + ',100%,' + 20 + '%)')
        expect(wrapper.vm.calcHSL(-1.0)).toBe('hsl(' + 0 + ',100%,' + 40 + '%)')
    })

    it('hue is selected based on sign', () => {
        expect(wrapper.vm.calcHue(-0.4)).toBe(0)
        expect(wrapper.vm.calcHue(0.25)).toBe(174)
    })

    it('no spaces in front of punctuation but in front of words', () => {
        expect(wrapper.vm.whitespace(",")).toBe("")
        expect(wrapper.vm.whitespace("great")).toBe(" ")
    })

    it('explanations are scaled', async () => {
        await wrapper.setProps({maxScore: 0.5})
        const explanation = [{"word": "the", "score": -0.25}, {"word": "world", "score": 0.1}]
        expect(wrapper.vm.rescaleScores(explanation)).toStrictEqual(
            [{"word": "the", "score": -0.50}, {"word": "world", "score": 0.2}])
    })

    it('scaling factor for empty explanation is 1', () => {
        const explanation = []
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(1.0)
    })

    it('scaling factor depends on maxScore', async () => {
        await wrapper.setProps({maxScore: 0.5})
        const explanation = [{"word": "the", "score": -0.25}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(2.0)
    })

    it('explanations with scores above minLength are not scaled', async () => {
        await wrapper.setProps({maxScore: 0.8})
        const explanation = [{"word": "the", "score": 0.9}, {"word": "world", "score": 0.7}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(1.0)
    })

    it('explanations with scores below minLength are scaled', async () => {
        await wrapper.setProps({maxScore: 0.8})
        const explanation = [{"word": "the", "score": 0.3}, {"word": "world", "score": 0.4}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(2.0)
    })

    it('explanations with negative scores above minLength are scaled', async () => {
        await wrapper.setProps({maxScore: 0.8})
        const explanation = [{"word": "the", "score": -0.2}, {"word": "world", "score": 0.1}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(4.0)
    })

    it('explanations with negative scores below minLength are scaled', async () => {
        await wrapper.setProps({maxScore: 0.8})
        const explanation = [{"word": "the", "score": 0.5}, {"word": "world", "score": -0.9}]
        expect(wrapper.vm.getScalingFactor(explanation)).toBeCloseTo(1.0)
    })

})

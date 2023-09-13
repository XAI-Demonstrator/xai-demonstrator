import {shallowMount} from '@vue/test-utils'
import MultiBounce from "@/components/MultiBounce";

describe('MultiBounce.vue', () => {

    it('renders numberOfDots dots', () => {
        const numberOfDots = 5

        const wrapper = shallowMount(MultiBounce, {
            propsData: {numberOfDots}
        })

        expect(wrapper.findAll('div.bouncing-dot').length).toBe(numberOfDots)
    })

    it('fits the animation into a single period', async () => {
        const numberOfDots = 10
        const period = 0.5

        const wrapper = shallowMount(MultiBounce, {
            propsData: {numberOfDots}
        })

        await wrapper.setData({period})

        expect(wrapper.vm.duration).toBe('5s')
        expect(wrapper.findAll('div.bouncing-dot').at(9).element.style.animationDelay).toBe('4.5s')
    })

})

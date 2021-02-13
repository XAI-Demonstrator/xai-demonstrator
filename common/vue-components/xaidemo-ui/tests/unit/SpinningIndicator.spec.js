import {shallowMount} from '@vue/test-utils'
import SpinningIndicator from "@/components/SpinningIndicator";

describe('SpinningIndicator.vue', () => {

    let wrapper = null

    beforeEach(() => {
        wrapper = shallowMount(SpinningIndicator)
    })

    it('is initially not visible', () => {
        expect(wrapper.find('div.wrapper').exists()).toBe(false)
    })

    it('appears and disappears', async () => {
        await wrapper.setProps({visible: true})

        expect(wrapper.find('div.wrapper').exists()).toBe(true)

        await wrapper.setProps({visible: false})

        expect(wrapper.find('div.wrapper').exists()).toBe(false)
    })

})

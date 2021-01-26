import {createLocalVue, shallowMount} from '@vue/test-utils'
import ComposeReview from "@/components/ComposeReview";


describe('Component', () => {

    const localVue = createLocalVue()
    const wrapper = shallowMount(ComposeReview, localVue);

    it('review changed is emitted', async () => {
        wrapper.setData({text: 'Nice movie!'})
        wrapper.vm.reviewChanged()
        await wrapper.vm.$nextTick()

        expect(wrapper.emitted().reviewChanged).toBeTruthy()
        expect(wrapper.emitted().reviewChanged[0]).toStrictEqual(['Nice movie!'])
    })

})
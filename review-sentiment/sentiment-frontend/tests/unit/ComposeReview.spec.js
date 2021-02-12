import {createLocalVue, shallowMount} from '@vue/test-utils'
import ComposeReview from "@/components/ComposeReview";


describe('ComposeReview.vue', () => {

    const localVue = createLocalVue()
    let wrapper = shallowMount(ComposeReview, localVue);

    beforeEach(() => {
            wrapper = shallowMount(ComposeReview, localVue);
        }
    )

    it('review-changed event is emitted when text changes', async () => {
        const review = 'The food was tasty!'
        const input = wrapper.find('#review-input-field')

        await input.setValue(review)

        expect(wrapper.emitted('review-changed')).toBeTruthy()
        expect(wrapper.emitted('review-changed')[0][0]).toStrictEqual(review)
    })

    it('intro text is visible when default review is visible', async () => {
        await wrapper.setProps({showIntro: true})
        await wrapper.setData({text: 'A review entered by a user'})

        expect(wrapper.find('.intro-text').exists()).toBe(false)

        await wrapper.setData({text: ''})

        expect(wrapper.find('.intro-text').exists()).toBe(true)
    })

})
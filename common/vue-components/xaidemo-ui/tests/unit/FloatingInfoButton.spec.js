import { shallowMount } from '@vue/test-utils'
import FloatingInfoButton from '@/components/FloatingInfoButton.vue'

describe('FloatingInfoButton.vue', () => {

  it('popup is not visible when mounted', () => {
    const wrapper = shallowMount(FloatingInfoButton)


    expect(wrapper.find('div.info-popup').exists()).toBe(false)
  })

  it('popup can be opened and closed', async () => {
    const wrapper = shallowMount(FloatingInfoButton)

    await wrapper.vm.openPopup()

    expect(wrapper.find('div.info-popup').exists()).toBe(true)

    await wrapper.vm.closePopup()

    expect(wrapper.find('div.info-popup').exists()).toBe(false)
  })

  it('info button opens popup', async () => {
    const wrapper = shallowMount(FloatingInfoButton)

    const infobutton = wrapper.find('div.icon-container').find('div.icon')
    expect(infobutton.classes()).toContain('open')

    await infobutton.trigger('click')

    expect(wrapper.find('div.info-popup').exists()).toBe(true)
    
    const closebutton = wrapper.find('div.icon-container').find('div.icon')
    expect(closebutton.classes()).toContain('close')

    await closebutton.trigger('click')

    expect(wrapper.find('div.info-popup').exists()).toBe(false)
  })
  
})

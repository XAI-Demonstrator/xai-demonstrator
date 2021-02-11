import { shallowMount } from '@vue/test-utils'
import UseCaseHeader from '@/components/UseCaseHeader.vue'

describe('UseCaseHeader.vue', () => {

  it('renders props.title when passed', () => {
    const title = 'Some Great Use Case'
    const wrapper = shallowMount(UseCaseHeader, {
      propsData: { title }
    })

    expect(wrapper.find('div.header-title').text()).toMatch(title)
  })

  it('omits back button  when props.standalone is true', () => {
    const wrapper = shallowMount(UseCaseHeader, {
      propsData: { standalone: true }
    })
 
    expect(wrapper.findAll('div.header-icon').at(0).element).toBeEmptyDOMElement()
  })

  it('adds  back button  when props.standalone is false', () => {
    const wrapper = shallowMount(UseCaseHeader, {
      propsData: { standalone: false }
    })
  
   const a = wrapper.findAll('div.header-icon').at(0).find('a');
   expect(a.exists()).toBe(true)
   expect(a.attributes().href).toBe('/')
  })
})

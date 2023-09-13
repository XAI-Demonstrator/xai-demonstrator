import {shallowMount} from '@vue/test-utils'
import UseCaseHeader from '@/components/UseCaseHeader.vue'

describe('UseCaseHeader.vue', () => {

    let windowSpy;

    beforeEach(() => {
        windowSpy = jest.spyOn(window, "window", "get");
    });

    afterEach(() => {
        windowSpy.mockRestore();
    });

    it('renders props.title when passed', () => {
        const title = 'Some Great Use Case'
        const wrapper = shallowMount(UseCaseHeader, {
            propsData: {title}
        })

        expect(wrapper.find('div.header-title').text()).toMatch(title)
    })

    it('omits back button when props.standalone is true', () => {
        const wrapper = shallowMount(UseCaseHeader, {
            propsData: {standalone: true}
        })

        expect(wrapper.findAll('div.header-icon').at(0).element).toBeEmptyDOMElement()
    })

    it('adds back button when props.standalone is false', () => {
        const wrapper = shallowMount(UseCaseHeader, {
            propsData: {standalone: false}
        })

        const a = wrapper.findAll('div.header-icon').at(0).find('a')
        expect(a.exists()).toBe(true)
        expect(a.attributes().href).toBe('/')
    })

    it('hides back button in embedded mode', () => {
        const searchString = '?embedded'
        windowSpy.mockImplementation(() => ({
            location: {
                search: searchString
            }
        }))

        const wrapper = shallowMount(UseCaseHeader, {
            propsData: {standalone: false}
        })

        const a = wrapper.findAll('div.header-icon').at(0).find('a')
        expect(a.exists()).toBe(false)
    })

    it('appends window.location.search to reload link', () => {
        const searchString = '?method=standard'
        windowSpy.mockImplementation(() => ({
            location: {
                search: searchString
            }
        }))
        const wrapper = shallowMount(UseCaseHeader)

        const a = wrapper.findAll('div.header-icon').at(1).find('a')
        expect(a.exists()).toBe(true)
        expect(a.attributes().href).toBe('./' + searchString)

    })

})

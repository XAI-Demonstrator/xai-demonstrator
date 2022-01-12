import {SpinningIndicator} from "@xai-demonstrator/xaidemo-ui";
// eslint-disable-next-line no-unused-vars
import axios from 'axios';
// import flushPromises from 'flush-promises';
import {shallowMount} from "@vue/test-utils";
import App from "@/App";

jest.mock('axios');



describe('App.vue', () => {
    let wrapper = shallowMount(App);

    beforeEach(() => {
        wrapper = shallowMount(App);
    })

     it('shows bouncing dots while waiting for prediction', async () => {
        let component = wrapper.findComponent(SpinningIndicator)

         await wrapper.setData({waitingForExplanation: false})
        
         expect(wrapper.vm.waitingForExplanation).toBe(false)

          expect(component.exists()).toBe(true)

    //     expect(component.isVisible()).toBe(false)
    //     //await wrapper.setData({waitingForExplanation: true})

    //     //expect(wrapper.findComponent(SpinningIndicator).isVisible()).toBe(true)
     })

    //  it('requests a prediction', async () => {
    //      const response = {
    //          data: {
    //              class_label: 'israel'
    //          }
    //      }
    //      axios.post.mockImplementationOnce(() => Promise.resolve(response))
    //     await wrapper.vm.predict('fake-blob')
    //     await flushPromises()
    //     expect(wrapper.vm.$data.prediction).toStrictEqual('israel')
    //      expect(wrapper.emitted('inspection-completed')).toBeTruthy()
    //  })

    // it('shows prediction only when it exists', async () => {
    //     await wrapper.setData({prediction: 'israel'})

    //     expect(wrapper.findComponent('').isVisible()).toBe(true)

    //     await wrapper.setData({prediction: null})

    //     expect(wrapper.find('p').isVisible()).toBe(false)
    // })

    // it('shows user answer only when it exists', async () => {
    //     await wrapper.setData({user_answer: 'israel'})

    //     expect(wrapper.findComponent('').isVisible()).toBe(true)

    //     await wrapper.setData({user_answer: null})

    //     expect(wrapper.find('p').isVisible()).toBe(false)
    // })

    // it('shows the correct text only when it exists', async () => {
    //     await wrapper.setData({user_answer: 'israel'})
    //     await wrapper.setData({class_label: 'israel'})

    //     expect(wrapper.findComponent('').isVisible()).toBe(true)
    //     expect(wrapper.find('p').isVisible()).toBe(false)

    //     await wrapper.setData({user_answer: 'germany'})
    //     await wrapper.setData({class_label: 'israel'})

    //     xpect(wrapper.findComponent('').isVisible()).toBe(true)
    //     expect(wrapper.find('p').isVisible()).toBe(false)
    // })

})
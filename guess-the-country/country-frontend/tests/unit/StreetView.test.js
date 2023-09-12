import StreetView from '@/components/StreetView.vue'
import {SpinningIndicator} from "@xai-demonstrator/xaidemo-ui";
import {mount} from '@vue/test-utils'
import {test, expect} from "vitest";

test('show spinning while waiting for backend', async () => {

    const wrapper = mount(StreetView)

    let component = wrapper.findComponent(SpinningIndicator)
    expect(component.exists()).toBe(true)

    await wrapper.setData({waitingForBackend: false})
    expect(component.find("div.wrapper").exists()).toBe(false)

    await wrapper.setData({waitingForBackend: true})
    expect(component.find("div.wrapper").exists()).toBe(true)
})

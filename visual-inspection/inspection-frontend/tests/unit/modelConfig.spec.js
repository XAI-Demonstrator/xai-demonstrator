import {modelConfig} from "@/modelConfig";

describe('modelConfig.js', () => {

    beforeEach(() => {
        jest.resetModules()
    })

    it('creates a model id', () => {
        modelConfig.smartphone.amount = "10"
        modelConfig.smartphone.label = "cup"

        modelConfig.pencil.amount = "22"
        modelConfig.pencil.label = "pencil"

        modelConfig.cup.amount = "15"
        modelConfig.cup.label = "cup"

        expect(modelConfig.getModelId()).toBe('model_10T_22_15')
    })

    it('does not add T if amount is 0', () => {
        modelConfig.smartphone.amount = "0"
        modelConfig.smartphone.label = "cup"

        modelConfig.pencil.amount = "22"
        modelConfig.pencil.label = "pencil"

        modelConfig.cup.amount = "15"
        modelConfig.cup.label = "cup"

        expect(modelConfig.getModelId()).toBe('model_0_22_15')
    })

})
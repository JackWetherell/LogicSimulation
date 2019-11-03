'''Definitions of the four fundamnetal logic gates: BUFF, AND, OR, NOT'''
import core


class BUFF(core.Component):
    '''Buffer gate'''
    def __init__(self, count=1):
        super().__init__()
        self.add_inputs(count=count)
        self.add_outputs(count=count)


    def evaluate(self):
        '''Definition of buffer evaluation'''
        for i, input in enumerate(self.input):
            if input.value is None: # interpret None as False
                self.output[i].value = False
            else:
                self.output[i].value = input.value


class AND(core.Component, count=2):
    '''And gate'''
    def __init__(self):
        super().__init__()
        self.add_inputs(count=count)
        self.add_outputs(count=1)


    def evaluate(self):
        '''Definition of and evaluation'''
        temp = list(map(lambda input: input.value, self.inputs))
        self.outputs[0] = all([False if t==None else t for t in temp]) # interpret None as False
        del temp


class Or(core.Component, count=2):
    '''Or gate'''
    def __init__(self):
        super().__init__()
        self.add_inputs(count=count)
        self.add_outputs(count=1)


    def evaluate(self):
        '''Definition of or evaluation'''
        temp = list(map(lambda input: input.value, self.inputs))
        self.outputs[0] = any([False if t==None else t for t in temp]) # interpret None as False
        del temp


class Not(core.Component):
    '''Not gate'''
    def __init__(self, count=1):
        super().__init__()
        self.add_inputs(count=count)
        self.add_outputs(count=count)


    def evaluate(self):
        '''Definition of not evaluation'''
        for i, input in enumerate(self.input):
            if input.value is None: # interpret None as False
                self.output[i].value = False
            else:
                self.output[i].value = not input.value
'''Definitions of many pre-made components'''
import core
from fundamental_gates import BUFF, AND, OR, NOT


class ExampleComponent(core.Component):
    '''Description of the ExampleComponent'''
    def __init__(self):
        super().__init__()

        # add inputs
        self.add_inputs(count=3)

        # add components`
        self.add_component(AND())
        self.add_component(OR())
        self.add_component(OR())

        # add outputs
        self.add_outputs(count=1)

        # add connections
        self.add_connection(self.inputs[0], self.components[0], end_index=0)
        self.add_connection(self.inputs[1], self.components[0], end_index=1)
        self.add_connection(self.inputs[1], self.components[1], end_index=0)
        self.add_connection(self.inputs[2], self.components[1], end_index=1)
        self.add_connection(self.components[0], self.components[2], start_index=0, end_index=0)
        self.add_connection(self.components[1], self.components[2], start_index=0, end_index=1)
        self.add_connection(self.components[2], self.outputs[0], start_index=0)


example_component = ExampleComponent()

example_component.inputs[0].value = False
example_component.inputs[1].value = True
example_component.inputs[2].value = False

example_component.evaluate()

print(list(map(lambda i: i.value, example_component.inputs)))
print(list(map(lambda i: i.value, example_component.outputs)))
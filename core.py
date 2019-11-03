'''Contains the core classes to define the behavior of logic gate modules and components'''
from enum import Enum


class ComponentTypes(Enum):
    '''Enumeration to define possible component types. SIMPLE, COMPOSITE as three dedicated inputs for clock, enable and load signals'''
    SIMPLE = 1
    COMPOSITE = 2


class ComponentException(Exception):
    '''Custom exception raised when a component is poorly defined in some way'''
    pass


class Container:
    '''Empty container struct'''
    pass


class Component:
    '''The component class defines the logic any component in a module follows'''
    def __init__(self, type=ComponentTypes.SIMPLE):
        '''Define an empty component'''
        self.inputs = list()
        self.components = list()
        self.outputs = list()
        self.connections = list()
        self.checkpoint = None
        self.type = type

        # reserved inputs for composite component 0: Clock, 1: Enable, 2: Load.
        if self.type == ComponentTypes.COMPOSITE:
            self.add_inputs(count=3)


    def add_inputs(self, count=1):
        '''Define a set of inputs for the component'''
        for _ in range(count):
            input = Input()
            self.inputs.append(input)


    def add_component(self, component):
        '''Define a set of components in the component'''
        self.components.append(component)


    def add_outputs(self, count=1):
        '''Define a set of outputs for the component'''
        for _ in range(count):
            output = Output()
            self.outputs.append(output)


    def add_connection(self, start_point, end_point, start_index=None, end_index=None):
        '''Connect two internal constituents directionally together'''
        connection = Connection()
        connection.start_point = start_point
        connection.end_point = end_point
        connection.start_index = start_index
        connection.end_index = end_index
        if isinstance(connection.start_point, Input):
            connection.start_point.start_indices.append(len(self.connections))
        if isinstance(connection.start_point, Component):
            assert start_index is not None, 'must specift start_index if start_point is a Component'
            connection.start_point.outputs[start_index].connection_indices.append(len(self.connections))
        if isinstance(connection.start_point, Output) or isinstance(end_point, Input):
            raise ComponentException('connection must not be connected to its own input or from its own output')
        if isinstance(connection.end_point, Component):
            assert end_index is not None, 'must specift end_index if end_index is a Component'
            connection.end_point.inputs[end_index].connection_indices.append(len(self.connections))
            assert len(connection.end_point.inputs[end_index].connection_indices) <= 1, 'cannot connect twice to the same input'
        if isinstance(connection.end_point, Output):
            pass
        self.connections.append(connection)


    def set_input(self, index, value):
        self.inputs[index].value = value


    def evaluate(self):
        '''Evaluate the component given a list of values. Returns True if result should be propogated, False if not'''
        # do we need to evaulate this component
        if self._check_checkpoint() == False:
            return

        # evaulate this component
        for input in self.inputs:
            for index in input.start_indices:
                self._evaluate_connection(index)

        # set the component checkpoint
        self._set_checkpoint()
        return


    def get_output(self, index):
        return self.outputs[index].value


    def _evaluate_connection(self, index):
        '''Take the value from the start_point, and propogate it to the end point'''
        # take the signal from the start point
        if isinstance(self.connections[index].start_point, Input):
            self.connections[index].value = self.connections[index].start_point.value
        if isinstance(self.connections[index].start_point, Component):
            self.connections[index].value = self.connections[index].start_point.outputs[self.connections[start_index]].value
        if isinstance(self.connections[index].start_point, Output):
            raise ComponentException('cannot evaluate a connection whose start_point is of type Output')

        # propigate the signal to the end point
        if isinstance(self.connections[index].end_point, Input):
            raise ComponentException('cannot evaluate a connection whose end_point is of type Input')
        if isinstance(self.connections[index].end_point, Component):
            self.connections[index].end_point.inputs[end_index].value = self.connections[index].value
            self.connections[index].end_point.evaluate()
            for output in self.connections[index].end_point.outputs:
                for connection_index in output.connection_indices:
                    self._evaluate_connection[connection_index]
        if isinstance(self.connections[index].end_point, Output):
            self.connections[index].end_point.value = self.connections[index].value
            return
        return


    def _set_checkpoint(self):
        '''private: set the checkpoint to the current state of the component'''
        self.checkpoint.inputs = list(map(lambda i: i.value, self.inputs))
        self.checkpoint.connections = list(map(lambda c: c.value, self.connections))


    def _check_checkpoint(self):
        '''private: compute if the checkpoint is different to the current state of the component'''
        if self.checkpoint == None:
            return True
        elif list(map(lambda i: i.value, self.inputs)) == self.checkpoint.inputs and list(map(lambda c: c.value, self.connections)) == self.checkpoint.connections:
            return False
        else:
            return True


class Input:
    '''The Input class defines the behavior of component inputs'''
    def __init__(self):
        '''Define a blank input'''
        self.value = None
        self.start_indices = list()
        self.connection_indices = list()


class Output:
    '''The Output class defines the behavior of component outputs'''
    def __init__(self):
        '''Define a blank output'''
        self.value = None
        self.connection_indices = list()


class Connection:
    '''The Connection class defines the behavior of thye connection between component internals'''
    def __init__(self):
        '''Define a floating connection'''
        self.start_point = None
        self.end_point = None
        self.start_index = None
        self.end_index = None
        self.value = None
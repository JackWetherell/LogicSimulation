'''Contains the core classes to define logic gate modules'''
from enum import Enum
import copy


class ComponentTypes(Enum):
    '''Enumeration to define possible component types. SIMPLE, COMPOSITE as three dedicated inputs for clocl, enable and load signals'''
    SIMPLE = 1
    COMPOSITE = 2


class ComponentException(Exception):
    '''Custom exception raised when a component is poorly defined in some way'''
    pass


class Container:
    '''Empty container struct'''
    pass


class Component:
    '''
    The component class defines the logic any component in the module follows
    '''
    def __init__(self, type=ComponentTypes.SIMPLE):
        '''Define an empty component'''
        self.inputs = list()
        self.outputs = list()
        self.components = list()
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


    def add_outputs(self, count=1):
        '''Define a set of outputs for the component'''
        for _ in range(count):
            output = Output()
            self.outputs.append(output)


    def add_components(self, components):
        '''Define a set of components in the component'''
        if isinstance(components, Component):
            self.components.append(components)
        if isinstance(components, list):
            for component in components:
                self.components.append(component)
        else:
            raise ComponentException('when adding components, argument must be a Component or list of Components')


    def add_connection(self, start_point, end_point, start_index=None, end_index=None):
        '''Connect two internal constituents directionally together'''
        connection = Connection()
        connection.start_point = start_point
        connection.end_point = end_point
        connection.start_index = start_index
        connection.end_index = end_index
        if isinstance(connection.start_point, Input):
            connection.start_point.start_indices.append(len(self.connections))
        if isinstance(connection.end_point, Output):
            pass
        if isinstance(connection.start_point, Component):
            assert start_index is not None, 'must specift start_index if start_point is a Component'
            connection.start_point.outputs[start_index].connection_indices.append(len(self.connections))
        if isinstance(connection.end_point, Component):
            assert end_index is not None, 'must specift start_index if start_point is a Component'
            connection.end_point.inputs[end_index].connection_indices.append(len(self.connections))
            assert len(connection.end_point.inputs[end_index].connection_indices) <= 1, 'cannot connect twice to the same input'
        if isinstance(connection.start_point, Output) or isinstance(end_point, Input):
            raise ComponentException('connection must not be connected to its own input or from its own output')
        self.connections.append(connection)


    def evaluate(self, values):
        '''Evaluate the component given a list of values. Returns True if result should be propogated, False if not'''
        assert isinstance(values, list), 'values not passed in as a list'
        assert len(values) == len(inputs), 'number of values passed as input must equall the number of inputs'

        # check we need to evaluate
        if self._check_checkpoint() == False:
            return

        # main evaluation loop
        for input in self.inputs:
            for index in input.start_indices:
                self.connections[index].value = input.value
                if isinstance(self.connections[index].end_point, Output):
                    self.connections[index].end_point.value = self.connections[index].value
                if isinstance(self.connections[index].end_point, Component):
                    values = list()
                    for i in self.connections[index].end_point.inputs:
                        values.append(self.connections[i.connection_indices[0]].value)
                    self.connections[index].end_point.evaulate(values)
                    for x in list(map(lambda o: o.connection_indices, self.connections[index].end_point.outputs)):
                        self.connections[x].value = self.connections[x].start_point.outputs[start_index]
                        if isinstance(self.connections[x].end_point, Output):
                            self.connections[x].end_point.value = self.connections[x].value
                        if isinstance(self.connections[x].end_point, Component):
                            values = list()
                            for i in self.connections[x].end_point.inputs:
                                values.append(self.connections[i.connection_indices[0]].value)
                                self.connections[x].end_point.evaulate(values)


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
    '''
    The Input class defines the behavior of component inputs
    '''
    def __init__(self):
        '''Define a blank input'''
        self.value = None
        self.start_indices = list()
        self.connection_indices = list()


class Output:
    '''
    The Output class defines the behavior of component outputs
    '''
    def __init__(self):
        '''Define a blank output'''
        self.value = None
        self.connection_indices = list()


class Connection:
    '''
    The Connection class defines the behavior of thye connection between component internals
    '''
    def __init__(self):
        '''Define a connection'''
        self.start_point = None
        self.end_point = None
        self.start_index = None
        self.end_index = None
        self.value = None


c = Component()
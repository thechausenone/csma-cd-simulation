from nodes.node import Node
from utils.random_variable_generator import RandomVariableGenerator
from abc import ABC, abstractmethod

class SimulatorBase(ABC):
    def __init__(self, num_nodes, arrival_rate, duration=1000):
        self.stability_criteria = 0.05
        self.duration = duration
        self.packet_length = 1500
        self.transmission_time = self.packet_length  / 1e6 # packet length / channel speed [secs]
        self.prop_time = 10 / ((2/3) * 3e8) # distance / prop_speed [secs]
        self.nodes = [Node(i, duration, arrival_rate) for i in range(0, num_nodes)]

    @abstractmethod
    def run_single_iteration(self):
        pass

    @abstractmethod
    def _check_stability(self, prev_result, curr_result):
        pass

    # Start simulation. Run it with increasing simulation time (up to 5 times), and check if the 
    # system is stable.
    def start(self):
        original_duration = self.duration
        initial_result = self.run_single_iteration()
        for _ in range(0, 5):
            curr_result = self.run_single_iteration()

            if self._check_stability(initial_result, curr_result):
                return initial_result
            else:
                initial_result = curr_result
                self.duration += original_duration
                print("Current system state is unstable, running again with T={}".format(self.duration))
        print("WARNING: System is unstable for current set of parameters, outputting results anyways...")
        return initial_result

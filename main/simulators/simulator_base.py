from utils.random_variable_generator import RandomVariableGenerator
from abc import ABC, abstractmethod

class Simulator(ABC):
    def __init__(self, num_nodes, arrival_rate, duration=1000):
        self.stability_criteria = 0.05
        self.duration = duration
        self.num_nodes = num_nodes
        self.arrival_rate = arrival_rate
        self.channel_speed = 1e6 # bits/sec
        self.packet_length = 1500 # bits
        self.distance = 10 # meters
        self.prop_speed = (2/3) * 3e8 # meters/sec

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
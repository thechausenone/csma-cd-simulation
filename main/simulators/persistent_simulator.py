from .simulator_base import Simulator
from utils.math_functions import percentage_change

class PersistentSimulator(Simulator):
    def __init__(self, num_nodes=20, arrival_rate=7):
        super().__init__(num_nodes=num_nodes, arrival_rate=arrival_rate)

    # Run one iteration of the simulation
    def run_single_iteration(self):
        print("Running!")

    # Check the stability of the system for varying simulation times
    def _check_stability(self, prev_result, curr_result):
        pass
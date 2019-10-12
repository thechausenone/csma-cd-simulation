from .simulator_base import Simulator
from .node_status import Status
from utils.math_functions import percentage_change

class PersistentSimulator(Simulator):
    def __init__(self, num_nodes=20, arrival_rate=7):
        super().__init__(num_nodes=num_nodes, arrival_rate=arrival_rate)

    # Run one iteration of the simulation
    def run_single_iteration(self):
        curr_simulation_time = 0
        while curr_simulation_time < self.duration:
            src_node = self.get_next_node()
            curr_simulation_time = src_node.get_queue_head_time()
            node_statuses = self.get_node_statuses(src_node)

    # Check the stability of the system for varying simulation times
    def _check_stability(self, prev_result, curr_result):
        pass

    # Returns the node with lowest timestamp packet in its queue
    def get_next_node(self):
        return min(self.nodes, key=lambda node: node.get_queue_head_time())

    def get_node_statuses(self, src_node):
        statuses = []
        src_node_packet_time = src_node.get_queue_head_time()
        for node in self.nodes:
            if src_node.id != node.id:
                num_props = abs(node.id - src_node.id)
                busy_lower_bound = self.prop_time * num_props + src_node_packet_time
                busy_upper_bound = busy_lower_bound + self.transmission_time
                if src_node_packet_time < busy_lower_bound:
                    statuses.append((Status.COLLISION, node, src_node))
                elif src_node_packet_time > busy_upper_bound:
                    statuses.append((Status.IDLE, node, src_node))
                else:
                    statuses.append((Status.BUSY, node, src_node))
        return statuses

    def handle_node_statuses(self, node_statuses):
        for node_status in node_statuses:
            status, dest_node, src_node = node_status
            # NOTE: how do we update waiting time for sending node if there are multiple collisions?
            if status == Status.COLLISION:
                pass
            elif status == Status.IDLE:
                continue
            elif status == Status.BUSY:
                pass

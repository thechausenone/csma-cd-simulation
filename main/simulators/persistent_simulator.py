from .simulator_base import Simulator
from .node_status import Status
from utils.math_functions import percentage_change
from utils.exponential_backoff import generate_backoff_time

class PersistentSimulator(Simulator):
    def __init__(self, num_nodes=20, arrival_rate=7, persistent_flag=True):
        super().__init__(num_nodes=num_nodes, arrival_rate=arrival_rate)
        self.persistent_flag = persistent_flag
        self.num_dropped = 0

    # Run one iteration of the simulation
    def run_single_iteration(self):
        curr_simulation_time = 0
        while curr_simulation_time < self.duration:
            try:
                src_node = self.get_next_node()
            except Exception as e:
                print(e)
                break
            curr_simulation_time = src_node.get_queue_head_time()
            node_statuses = self.get_node_statuses(src_node)
            self.handle_node_statuses(src_node, node_statuses)
        return self.compute_metrics()

    # Check the stability of the system for varying simulation times
    def _check_stability(self, prev_result, curr_result):
        pass

    # Returns the node with lowest timestamp packet in the queue's head position
    def get_next_node(self):
        curr_min_node = None
        curr_min_time = self.duration

        for node in self.nodes:
            time = node.get_queue_head_time()
            if time is None:
                continue
            if time < curr_min_time:
                curr_min_time = time
                curr_min_node = node
        
        if curr_min_node is None:
            raise Exception("There are no nodes with packets available, simulation will now terminate.")

        return curr_min_node

    def get_node_statuses(self, src_node):
        statuses = []
        collision_occured = False
        for node in self.nodes:
            if src_node.id != node.id:
                dest_node_packet_time = node.get_queue_head_time()
                # source does not need to account for destination because there are no packets in the queue
                if dest_node_packet_time is None:
                    continue
                busy_lower_bound, busy_upper_bound = self.compute_bounds(src_node, node)
                if dest_node_packet_time < busy_lower_bound:
                    collision_occured = True
                    statuses.append((Status.COLLISION, node))
                elif dest_node_packet_time > busy_upper_bound:
                    statuses.append((Status.IDLE, node))
                else:
                    statuses.append((Status.BUSY, node))

        if collision_occured:
            result = [status for status in statuses if status[0] is Status.COLLISION]
            return result

        return statuses

    # def get_node_statuses(self, src_node):
    #     statuses = []
    #     left_ptr = src_node.id - 1
    #     right_ptr = src_node.id + 1

    #     while left_ptr >= 0 or right_ptr < len(self.nodes):
    #         left_node = None
    #         right_node = None
    #         left_status = None
    #         right_status = None

    #         if left_ptr >= 0:
    #             left_node = self.nodes[left_ptr]
    #             left_status = self.get_node_status(src_node, left_node)
    #             left_ptr -= 1

    #         if right_ptr < len(self.nodes):
    #             right_node = self.nodes[right_ptr]
    #             right_status = self.get_node_status(src_node, right_node)
    #             right_ptr += 1
            
    #         if left_status and right_status and left_status[0] == Status.COLLISION and right_status[0] == Status.COLLISION:
    #             left_node_time = left_node.get_queue_head_time()
    #             right_node_time = right_node.get_queue_head_time()
    #             if left_node_time < right_node_time:
    #                 return [left_status]
    #             else:
    #                 return [right_status]
    #             break
    #         elif left_status and left_status[0] == Status.COLLISION:
    #             return [left_status]
    #         elif right_status and right_status[0] == Status.COLLISION:
    #             return [right_status]
    #         elif left_status and right_status:
    #             statuses.append(left_status)
    #             statuses.append(right_status)
    #         elif left_status: 
    #             statuses.append(left_status)
    #         elif right_status:
    #             statuses.append(right_status)
    #     return statuses

    # def get_node_status(self, src_node, dest_node):
    #     status = None
    #     dest_node_packet_time = dest_node.get_queue_head_time()

    #     # source does not need to account for destination because there are no packets in the queue
    #     if dest_node_packet_time is None:
    #         return status

    #     busy_lower_bound, busy_upper_bound = self.compute_bounds(src_node, dest_node)
    #     if dest_node_packet_time < busy_lower_bound:
    #         status = ((Status.COLLISION, dest_node))
    #     elif dest_node_packet_time > busy_upper_bound:
    #         status = ((Status.IDLE, dest_node))
    #     else:
    #         status = ((Status.BUSY, dest_node))
        
    #     return status

    def compute_bounds(self, src_node, dest_node):
        num_props = abs(dest_node.id - src_node.id)
        busy_lower_bound = self.prop_time * num_props + src_node.get_queue_head_time()
        busy_upper_bound = busy_lower_bound + self.transmission_time
        return (busy_lower_bound, busy_upper_bound)

    def handle_node_statuses(self, src_node, node_statuses):
        collision_occured = False

        # for destination nodes
        for status, dest_node in node_statuses:
            if status == Status.COLLISION:
                collision_occured = True
                dest_node.increment_collisions()
                wait_time = generate_backoff_time(dest_node.collision_counter)
                if wait_time is None:
                    dest_node.remove_queue_head_time()
                    dest_node.reset_collisions()
                    self.num_dropped += 1
                else:
                    _, busy_upper_bound = self.compute_bounds(src_node, dest_node)
                    dest_node.update_queue_times(wait_time + busy_upper_bound)
            elif status == Status.IDLE:
                continue
            elif status == Status.BUSY:
                _, busy_upper_bound = self.compute_bounds(src_node, dest_node)
                if self.persistent_flag:
                    dest_node.update_queue_times(busy_upper_bound)
                else:
                    dest_node.increment_busy_counter()
                    wait_time = generate_backoff_time(dest_node.busy_check_counter)
                    if wait_time is None:
                        dest_node.remove_queue_head_time()
                        dest_node.reset_busy_collisions()
                        self.num_dropped += 1
                    else:
                        dest_node.update_queue_times(busy_upper_bound + wait_time)

        # for source node
        if collision_occured:
            src_node.increment_collisions()
            wait_time = generate_backoff_time(src_node.collision_counter)
            if wait_time is None:
                src_node.remove_queue_head_time()
                src_node.reset_collisions()
                self.num_dropped += 1
            else:
                # update queue time of source node with minimum distance upperbound of reciever
                dest_node_of_min_props = node_statuses[0][1]
                min_props = abs(src_node.id - node_statuses[0][1].id)

                for status, dest_node in node_statuses:
                    if abs(src_node.id - dest_node.id) < min_props:
                        dest_node_of_min_props = dest_node

                _, busy_upper_bound = self.compute_bounds(src_node, dest_node_of_min_props)
                src_node.update_queue_times(wait_time + busy_upper_bound)
        else:
            src_node.num_successfully_transmitted += 1
            src_node.remove_queue_head_time()
            src_node.reset_collisions()
    
    def compute_metrics(self):
        total_num_successful = 0
        total_num_collisions = 0

        for node in self.nodes:
            total_num_successful += node.num_successfully_transmitted
            total_num_collisions += node.num_collisions

        print(total_num_successful)
        print(total_num_collisions)
        print(self.num_dropped)

        efficiency = total_num_successful / (total_num_collisions + total_num_successful)
        throughput = (total_num_successful * self.packet_length) / (self.duration * 1e6)

        return (efficiency, throughput)


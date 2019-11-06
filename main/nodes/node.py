from utils.random_variable_generator import RandomVariableGenerator

class Node:
    def __init__(self, node_id, duration, arrival_rate):
        self.busy_check_counter = 0
        self.busy_dropped_packets = 0
        self.collision_counter = 0
        self.num_collisions = 0
        self.num_successfully_transmitted = 0
        self.id = node_id
        self.duration = duration
        self.arrival_rate = arrival_rate
        self.queue = self.__generate_packet_times()
        self.min_packet_time = self.queue[0]

    def __generate_packet_times(self):
        curr_time = 0
        times = []
        while curr_time < self.duration:
            curr_time += RandomVariableGenerator.generate_input(self.arrival_rate)
            times.append(curr_time)
        return times[:-1]

    def reset_collisions(self):
        self.collision_counter = 0

    def increment_collisions(self):
        self.collision_counter += 1
        self.num_collisions += 1

    def reset_busy_collisions(self):
        self.busy_check_counter = 0
    
    def increment_busy_counter(self):
        self.busy_check_counter += 1

    def get_queue_head_time(self):
        if not self.queue:
            return None
        return max(self.queue[0], self.min_packet_time)

    def remove_queue_head_time(self):
        if self.queue:
            self.queue.pop(0)
            if self.queue and self.min_packet_time < self.queue[0]:
                self.min_packet_time = self.queue[0]

    # Update minimum packet time to be used for deterimining queue head time
    # NOTE: This is an optimization so we do not have to iterate over every queue to update packet
    # times
    def update_min_packet_times(self, time):
        if self.min_packet_time < time:
            self.min_packet_time = time

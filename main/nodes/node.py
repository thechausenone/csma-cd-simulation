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
        return self.queue[0]

    def remove_queue_head_time(self):
        if self.queue:
            self.queue.pop(0)

    # Set each element in queue that's less than `time` to be equal to `time`
    def update_queue_times(self, time):
        for index, item in enumerate(self.queue):
            if item < time:
                self.queue[index] = time
            else:
                break

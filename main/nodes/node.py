from utils.random_variable_generator import RandomVariableGenerator

class Node:
    def __init__(self, node_id, duration, arrival_rate):
        self.num_collisions = 0
        self.num_transmitted = 0
        self.id = node_id
        self.duration = duration
        self.arrival_rate = arrival_rate
        self.queue = self.__generate_packet_times()
        self.total_queue_packets = len(self.queue)

    def __generate_packet_times(self):
        curr_time = 0
        times = []
        while curr_time < self.duration:
            curr_time += RandomVariableGenerator.generate_input(self.arrival_rate)
            times.append(curr_time)
        return times[:-1]

    def reset_collisions(self):
        self.num_collisions = 0

    def get_queue_head_time(self):
        return self.queue[0]

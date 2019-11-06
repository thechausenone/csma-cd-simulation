import random

def generate_backoff_time(counter):
    if counter >= 10:
        return None
    bit_time = random.randrange(0, 2**counter) * 512 # true range is 0 to (2**counter)-1
    bit_time_in_secs = bit_time / 1e6 # 1e6 is the link rate
    return bit_time_in_secs

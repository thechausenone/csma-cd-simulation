import random

# NOTE: Returns integer
def generate_backoff_time(counter):
    if counter > 10:
        return None
    return random.randrange(0, (2**counter)-1) * 512

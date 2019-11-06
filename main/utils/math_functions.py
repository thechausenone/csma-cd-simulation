# Calculate percentage change
def percentage_change(initial, current):
    if initial == 0:
        return None
    result = abs(initial - current)/initial
    return result

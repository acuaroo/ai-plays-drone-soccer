movement = {
    "x": 0,
    "y": 1,
    "z": -1
}

def turn_to_tertiary(x):
    if x == -1:
        return 2
    
    return x

converted_movement = dict(map(lambda x: (x[0], turn_to_tertiary(x[1])), movement.items()))
print(converted_movement)
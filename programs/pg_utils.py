# determine current direction
def get_dir(valence, valence2, random_dir):
    if random_dir <= .25:
        return 180 if valence == -1 else 0
    elif random_dir >= .75:
        return 270 if valence == 1 else 90
    else:
        if valence == 1 and valence2 == -1:
            return 45 
        elif valence == -1 and valence2 == -1:
            return 135 
        elif valence == -1 and valence2 == 1:
            return 225 
        elif valence == 1 and valence2 == 1:
            return 315
        

# ensure direction moved does not reverse
def not_reverse(i, directions, random_dir, valence, valence2):
    import numpy as np
    if i > 0:
        # find the angle opposite of the current angle
        reverse = directions[i] + 180 if directions[i] < 180 else directions[i] - 180
        # keep generating random angles unit the reverse of the current angle does not equal the previous angle
        while directions[i-1] == reverse:
            # generate random numbers to determine direction
            random_dir = np.random.rand()
            valence = np.random.choice([-1, 1])
            valence2 = np.random.choice([-1, 1])
            # get the current direction
            directions[i] = get_dir(valence, valence2, random_dir)
            # find the angle opposite of the current angle
            reverse = directions[i] + 180 if directions[i] < 180 else directions[i] - 180

    return directions, random_dir, valence, valence2


def position_from_dist(target_position, previous_position):
    import numpy as np
    # Calculate the distance between the current position and the target position
    dx = target_position[0] - previous_position[0]
    dy = target_position[1] - previous_position[1]
    distance = np.sqrt(dx**2 + dy**2)

    # Calculate the step size for the animation
    step_size = 10
    if distance < step_size:
        step_size = distance

    # Update the position of the dot
    if distance > 1:
        previous_position = (previous_position[0] + dx/distance*step_size, previous_position[1] + dy/distance*step_size)
    
    return previous_position

# determine current direction
def dir_from_angle(angle):
    # {angle: [random_dir, valence, valence2]}
    direction = {0: [.25, 1, 0], 180: [.25, -1, 0], 90: [.75, -1, 0], 270: [.75, 1, 0], 45: [.5, 1, -1], 135: [.5, -1, -1], 225: [.5, -1, 1], 315: [.5, 1, 1]}
    return direction[angle]
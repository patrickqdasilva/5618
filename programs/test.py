# determine current direction
def dir_from_angle(angle):
    direction = {0: [.25, 1, 0], 180: [.25, -1, 0], 90: [.75, -1, 0], 270: [.75, 1, 0], 45: [.5, 1, -1], 135: [.5, -1, -1], 225: [.5, -1, 1], 315: [.5, 1, 1]}
    return *direction[angle]

output = dir_from_angle(45)
print(output)
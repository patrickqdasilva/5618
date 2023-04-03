import pygame
import numpy as np
import time
from pg_utils import get_dir, not_reverse, position_from_dist, dir_from_angle

def game(generation=False):
    ##### Initializing #####
    pygame.init()

    # window, clock, surface
    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    screen.fill((103,129,101))
    pygame.display.set_caption("Moving Dot")
    clock = pygame.time.Clock()
    dot_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    dot_number_font = pygame.font.SysFont('arial', 25)
    num_moves = 8

    # dot initial position
    dot_position = [size[0] // 2, size[1] // 2]

    # list to store previous positions
    previous_positions = []
    previous_positions.append(tuple(dot_position))

    # list to store directions (angles in degrees)
    directions = np.array([-1] * 8)
    nodes = [(-1,-1)] * 9

    # load in output if not generating input
    if generation is False:
        outputs = np.loadtxt("C:/Users/Patrick/Desktop/5618 project/data/outputs.txt", dtype='int32', delimiter=',')
        num_moves = len(outputs)
        print(num_moves)
    running = True
    # Main game loop
    for i in range(num_moves):
        # stop the game in case ball moves off screen
        if running is False: break
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if generation is True:
            # generate random numbers to determine direction
            random_dir = np.random.rand()
            valence = np.random.choice([-1, 1])
            valence2 = np.random.choice([-1, 1])
            # get the current direction
            directions[i] = get_dir(valence, valence2, random_dir)
            # ensure direction moved does not reverse
            directions, random_dir, valence, valence2 = not_reverse(i, directions, random_dir, valence, valence2)
        elif generation is False:
            directions[i] = outputs[i]
            random_dir, valence, valence2 = dir_from_angle(outputs[i])

        # Move in an x direction
        if random_dir <= .25:
            dot_position[0] += (150 * valence)
            # if the ball moves off the screen stop the game
            if dot_position[0] >= size[0] or dot_position[0] < 0: 
                running = False
                directions[i] = -1
        # move the y direction
        elif random_dir >= .75:
            dot_position[1] += (150 * valence)
            # if the ball moves off the screen stop the game
            if dot_position[1] >= size[1] or dot_position[1] < 0: 
                running = False
                directions[i] = -1
        # move along a diagonal
        else:
            dot_position[0] += (106 * valence)
            dot_position[1] += (106 * valence2)
            # if the ball moves off the screen stop the game
            if dot_position[0] >= size[0] or dot_position[0] < 0 or dot_position[1] >= size[1] or dot_position[1] < 0: 
                running = False
                directions[i] = -1
        
        # debug statement
        print("i:", i+1, "| x:", dot_position[0], "| y:", dot_position[1], "| angle:", directions[i])

        # Add the current position to the list of previous positions
        previous_positions.append(tuple(dot_position))
        
        # time between running each movement
        time.sleep(0.5)
        
        ##### this section prints the ball moving from one direction to another #####
        if running is True:
            # copies the current dot location
            target_position = previous_positions[-1]
            # copies the previous dot location
            previous_position = previous_positions[-2]
            # saves the n-1 position proper coloring
            temp = previous_position

            start = time.time()
            # Animate the dot sliding to the next position
            j = 0
            while previous_position != target_position:
                # get the next dot position based on the distance from the (n-1)th node to the (n)th node
                previous_position = position_from_dist(target_position, previous_position)

                # prevent trailing dots to overwrite nodes by skipping first round
                if j > 0:
                    # display trail of dots
                    pygame.draw.circle(dot_surface, (146,169,142), temp, radius=10)
                # occurs only on first round of every move
                # stores the node points in a list
                else:
                    nodes[i] = temp
                    # draw the first node
                    pygame.draw.circle(dot_surface, (219,246,209), nodes[i], radius=10)

                
                # display the newest dot on the screen
                pygame.draw.circle(dot_surface, (219,246,209), previous_position, radius=10)
                
                temp = previous_position

                # Update the screen
                screen.blit(dot_surface, (0,0))
                pygame.display.flip()
                clock.tick(80)
                j+=1
        ##### End Printing ball to screen #####

        end = time.time()
        print("time:",end-start)

    # set last node, differs if the dot went off the screen or not
    if running is True:
        nodes[i+1] = previous_position
    if running is False:
        nodes[i-1] = previous_position
    print(nodes)
    # print numbers over all the nodes for clean display at the end of trial
    for j, node in enumerate(nodes):
        # only print nodes that have occurred
        if node != (-1,-1):
            pygame.draw.circle(dot_surface, (219,246,209), node, radius=10)
            dot_number = dot_number_font.render(str(j+1), True, (16,21,22))
            dot_surface.blit(dot_number, np.array(node)-[6,14])
            screen.blit(dot_surface, (0,0))

    # Update the screen
    pygame.display.flip()
    clock.tick(80)

    print(directions[directions != -1])
    if generation is True:
        # save directions to a text file to be read by spike generators
        np.savetxt("C:/Users/Patrick/Desktop/5618 project/data/directions.txt", directions[directions != -1], fmt='%u', delimiter=',') 
    
    time.sleep(40)    

if __name__ == "__main__":
    game(generation=False)
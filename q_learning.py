import matplotlib.pyplot as plt
import numpy as np
import random

def main():
    global alpha, gamma, epsilon, x_grid, y_grid, state_num, hole, goal, action_num
    
    alpha = 0.3
    gamma = 0.9
    epsilon = 0.1

    x_grid = 5
    y_grid = 5
    state_num = x_grid * y_grid
    hole = [6, 7, 18, 19, 20]
    goal = 25
    action_num = 4 # up, down, left, right

    q_value = [0, [state_num, action_num]] # action value function
    episode = np.linspace(1,3000) # 2999 trials in total
    s = 1
    
    draw(s)

def locate(s):
    x_pos = np.mod(s+4, x_grid) + 1
    y_pos = np.floor_divide(s-1, y_grid) + 1
    return x_pos, y_pos

def draw(s):
    x_pos, y_pos = locate(s)
    fig, ax = plt.subplots()

    for i in range(x_grid):
        for j in range(y_grid):
            index = j*x_grid + i+1
            if index in hole:
                color = 'black'
            else:
                color = 'white'

            square = plt.Rectangle((i,j), 1, 1, edgecolor='black', facecolor=color)
            ax.add_patch(square)

            center_x = i + 0.5
            center_y = j + 0.5

            if i == (np.mod(goal+4, x_grid)) and j == np.floor_divide(goal, y_grid)-1:
                ax.text(center_x, center_y, 'G', color='gray', ha='center', va='center')

            if i+1 == x_pos and j+1 == y_pos: # plot current position
                ax.plot(center_x, center_y, 'o', color = 'green')
    
    ax.set_xlim(0, x_grid)
    ax.set_ylim(0,y_grid)
    ax.set_aspect('equal')
    # ax.axis('off')

    plt.show()

if __name__ == "__main__":
    main()
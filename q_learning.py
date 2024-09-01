import matplotlib.pyplot as plt
import numpy as np
import random
# import time

def main():
    # set params
    global alpha, gamma, epsilon, x_grid, y_grid, state_num, hole, goal, action_num, q_value
    global goal_reward, drop_reward, move_reward
    
    alpha = 0.3 # learning rate
    gamma = 0.9 # discount factor
    epsilon = 0.1 # exploration rate

    x_grid = 5
    y_grid = 5
    state_num = x_grid * y_grid
    hole = [6, 7, 18, 19, 20]
    goal = 25
    action_num = 4 # up, down, left, right

    q_value = [[0, s, a] for s in list(range(1, state_num+1)) for a in list(range(1, action_num+1))] # action value function
    episode = np.linspace(1, 3000,3000)
    s = 1

    goal_reward = 100
    drop_reward = -10
    move_reward = -1

    #run q-learning argorhythm
    fig, ax = plt.subplots()
    ax.plot()
    
    for episode in episode:
        fig.suptitle(f'episode {int(episode)}')
        draw(s, ax)
        action = select_action(s)
        ss = move(s, action)
        reward = calc_reward(ss)
        q_value[4*(s-1) + action-1][0] += alpha*(reward + gamma*q_value[4*(ss-1) + action-1][0] - q_value[4*(s-1) + action-1][0])
        s = 1 if ss == goal else ss # relocate
        plt.pause(0.2)
        # time.sleep(0.5)
    
    plt.show()

def locate(s):
    x_pos = np.mod(s+4, x_grid) + 1
    y_pos = np.floor_divide(s-1, y_grid) + 1
    # print('locate() called. x, y = {0}, {1}'.format(x_pos, y_pos)) # debug

    return x_pos, y_pos

def draw(s, ax):
    x_pos, y_pos = locate(s)
    ax.clear()

    for i in range(x_grid):
        for j in range(y_grid):
            index = j*y_grid + i+1
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
    plt.draw()

def select_action(s):
    action = random.randint(1, 4)
    while not is_movable(s, action):
        if random.random() < epsilon:
            action = random.randint(1, 4)
        else:
            maxq = max([item for item in q_value if item[1] == s], key=lambda x: x[0])
            minq = min([item for item in q_value if item[1] == s], key=lambda x: x[0])
            if maxq == minq:
                action = random.randint(1, 4)
            else:
                action = maxq[2]
    
    return action

def is_movable(s, action):
    flag = False
    x_pos, y_pos = locate(s)

    if action == 1: # up
        if y_pos+1 <= y_grid:
            flag = True

    elif action == 2: # down
        if y_pos-1 >= 1:
            flag = True
    
    elif action == 3: # left
        if x_pos-1 >= 1:
            flag = True
    
    elif action == 4: # right
        if x_pos+1 <= y_grid:
            flag = True

    return flag

def move(s, action):
    ss = 0
    x_pos, y_pos = locate(s)

    if action == 1: # up
        y_pos += 1
    elif action == 2: # down
        y_pos -= 1
    elif action == 3: # left
        x_pos -= 1
    elif action == 4: # right
        x_pos += 1

    ss = x_pos + (y_pos-1)*y_grid
    return ss

def calc_reward(ss):
    reward = 0
    if ss == goal:
        reward = goal_reward
    elif ss in hole:
        reward = drop_reward
    else:
        reward = move_reward
    
    return reward

if __name__ == "__main__":
    main()
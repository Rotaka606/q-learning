from matplotlib.colors import Normalize
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import random
# import time
import csv

def main():
    ### set params ###
    global alpha, gamma, epsilon
    global x_grid, y_grid, state_num, hole, goal, subgoal, action_num, directions
    global q_value
    global goal_reward, subgoal_reward, drop_reward, move_reward
    global goal_count
    
    alpha = 0.3 # learning rate
    gamma = 0.9 # discount factor
    epsilon = 0.1 # exploration rate

    x_grid = 5
    y_grid = 5
    state_num = x_grid * y_grid
    # hole = []
    hole = [6, 7, 19, 20]
    goal = 25
    subgoal = 13
    action_num = 4 # up, down, left, right
    directions = {
        1: '↑',
        2: '↓',
        3: '←',
        4: '→',
    }

    q_value = [[0, s, a] for s in list(range(1, state_num+1)) for a in list(range(1, action_num+1))] # action value function
    episode = np.linspace(1, 10000, 10000)
    stop_points = [1, 1000, 5000, 10000]
    s = 1

    goal_reward = 100
    subgoal_reward = 20
    drop_reward = -10
    move_reward = -1

    goal_count = 0
    subgoal_count = 0

    path = []
    paths = []

    ### run q-learning argorhythm ###
    fig, ax = plt.subplots()
    # ax.plot() #############################################################
    pause_sec = 3 ###########################################################
    
    for episode in episode:
        path.append(s)
        fig.suptitle('episode {0} (goal: {1}, subgoal: {2})'.format(int(episode), int(goal_count), int(subgoal_count)))
        # draw(s, ax) #######################################################
        action = select_action(s)
        ss = move(s, action)
        reward = calc_reward(ss)
        q_value[4*(s-1) + action-1][0] += alpha*(reward + gamma*q_value[4*(ss-1) + action-1][0] - q_value[4*(s-1) + action-1][0])

        if ss == goal:
            s = 1 # relocate
            goal_count += 1
            ax.plot() #######################################################
            draw(s, ax) #####################################################
            ax.text(1, 1, 'GOAL!', fontsize=20, ha='right', va='top', color='red', transform=ax.transAxes)
            if goal_count in [1, 10, 100]: # for report
                paths.append(path)
                plt.pause(pause_sec)
                # ax.texts.clear()
            path = []

        elif ss == subgoal:
            subgoal_count += 1
        # elif ss in hole:
        #     s = 1

        else:
            s = ss
            if episode in stop_points:
                ax.plot() ##################################################
                draw(s, ax) ################################################
                plt.pause(pause_sec) #######################################
        # plt.pause(0.002)
        # time.sleep(0.5)
        print(f'episode: {episode}')
    
    plt.show()
    save_path(paths)

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
            max_q_value = max([item for item in q_value if item[1] == index])
            maxq = max_q_value[0]
            maxa = int(max_q_value[2])
            color = 'black' if index in hole else 'white'

            square = plt.Rectangle((i,j), 1, 1, edgecolor='black', facecolor=color)
            ax.add_patch(square)

            center_x = i + 0.5
            center_y = j + 0.5

            ax.text(center_x, j, round(maxq, 2), color='gray', ha='center', va='bottom')
            ax.text(center_x, j+0.2, directions[maxa], color='gray', ha='center', va='bottom')
            ax.text(center_x, center_y, 'G', color='black', ha='center', va='center') if index == goal else None
            ax.text(center_x, center_y, 'SG', color='black', ha='center', va='center') if index == subgoal else None

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
    elif ss == subgoal:
        reward = subgoal_reward
    elif ss in hole:
        reward = drop_reward
    else:
        reward = move_reward
        # x_pos, y_pos = locate(ss)
        # x_pos_goal, y_pos_goal = locate(goal)
        # distance = abs(x_pos - x_pos_goal) + abs(y_pos - y_pos_goal)
        # reward = move_reward + 0.1/distance
    
    return reward

def save_path(paths):
    with open('log.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(paths)

if __name__ == "__main__":
    main()
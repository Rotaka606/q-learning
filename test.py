import numpy

# print(numpy.floor_divide(1, 5)) # 0
# print(list(range(5)))

def q_value():
    [situation, action_num] = [list(range(1, 26)), list(range(1, 5))]
    q_value = [[0, s, a] for s in situation for a in action_num]
    q_value[2][0] = 1
    print(q_value[:6])

    s=2
    # maxq = max([item[0] for item in q_value if item[1] == 20])
    maxq = max([item for item in q_value if item[1] == s], key=lambda x: x[0])
    print(maxq)

    action = maxq[2]

def ij():
    for i in range(5):
        for j in range(5):
            index = j*5 + i+1
            print(i, j, index)

if __name__ == "__main__":
    ij()
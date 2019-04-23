'''
    Filename: hw3cs561s2019.py

    Copyright: Yunfan Xue

    Author: Yunfan Xue (yunfanxu@usc.edu)

    Last Update Date: 4/12/2019

    Description: This "hw2cs561s2019.py" file belongs to the 19 spring CS561 Programing Assignment #3.
                 This file can only be read and tested by author, TAs, graders and professor.
'''

import numpy as np
import time

grid = 0
wall_number = 0
terminal_number = 0
transition_model = 0
reward = 0
discount_factor = 0
plate = None
plate_value = None
plate_new = None

theta = 0.001

WALL = 10
TERMINAL = 11


def read_input():
    with open('input0.txt', 'r') as inputFile:
        global  grid, wall_number, terminal_number, transition_model, reward, discount_factor, plate, plate_value, plate_new
        lines = inputFile.readlines()

        # read grid number
        grid = int(lines[0])
        lines.remove(lines[0])

        # build game plate
        plate = np.zeros((grid, grid))
        plate = plate.astype(np.str)


        # read wall number
        wall_number = int(lines[0])
        lines.remove(lines[0])

        # update plate's wall block
        for wall in range(0, wall_number):
            this_wall = lines[0]
            this_wall = this_wall.split(',')
            plate[int(this_wall[0]) - 1, int(this_wall[1]) - 1] = 'N'
            lines.remove(lines[0])

        # read terminal_state number
        terminal_number = int(lines[0])
        lines.remove(lines[0])
        reward = float(lines[terminal_number + 1])
        plate_value = np.full((grid, grid), 0)
        # update terminal into plate
        for wall in range(0, terminal_number):
            this_terminal = lines[0]
            this_terminal = this_terminal.split(',')
            plate[int(this_terminal[0]) - 1, int(this_terminal[1]) - 1] = 'T'
            plate_value[int(this_terminal[0]) - 1, int(this_terminal[1]) - 1] = float(this_terminal[2])
            lines.remove(lines[0])

        transition_model = float(lines[0])
        reward = float(lines[1])
        discount_factor = float(lines[2])
        plate_new = plate_value.copy()



def get_value(x, y, action_x, action_y):
    global reward
    if x + action_x < 0 or x + action_x >= grid or y + action_y < 0 or y + action_y >= grid:
        return plate_value[x, y]
    if plate[x + action_x, y + action_y] == 'N':
        return plate_value[x, y]
    return plate_value[x + action_x, y + action_y]


def update_this_value(x, y):
    if plate[x, y] == 'N' or plate[x, y] == 'T':
        return plate_value[x, y]

    reverse_tran = (1 - transition_model) / 2
    # going up
    go_up = (discount_factor * (
            transition_model * get_value(x, y, -1, 0) +
            reverse_tran * get_value(x, y, -1, -1) +
            reverse_tran * get_value(x, y, -1, 1)))

    # going down
    go_down = (discount_factor * (
            transition_model * get_value(x, y, 1, 0) +
            reverse_tran * get_value(x, y, 1, 1) +
            reverse_tran * get_value(x, y, 1, -1)))

    # going left
    go_left = (discount_factor * (
            transition_model * get_value(x, y, 0, -1) +
            reverse_tran * get_value(x, y, 1, -1) +
            reverse_tran * get_value(x, y, -1, -1)))

    # going right
    go_right = (discount_factor * (
            transition_model * get_value(x, y, 0, 1) +
            reverse_tran * get_value(x, y, -1, 1) +
            reverse_tran * get_value(x, y, 1, 1)))

    return max(go_up, go_down, go_left, go_right)


def do_updating():
    count = 0
    start = time.time()
    finished = False
    ipxl = 0
    global plate, plate_value, plate_new

    while not finished:
        count += 1
        print(str(count))
        end = time.time()
        if end - start >= 25:
            break
        ipxl = 0
        plate_value = plate_new.copy()
        for i in range(0, grid):
            for j in range(0, grid):
                if plate[i, j] == 'T' or plate[i, j] == 'N':
                    continue
                old_value = plate_value[i, j]
                new_value = reward + update_this_value(i, j)
                ipxl = max(ipxl, abs(new_value - old_value))
                plate_new[i, j] = new_value

        if ipxl < theta * (1 - discount_factor) / discount_factor:
            finished = True


def check_operation():
    global plate, plate_value
    reverse_tran = (1 - transition_model) / 2

    for i in range(0, grid):
        for j in range(0, grid):
            if plate[i, j] == 'T':
                plate[i, j] = 'E'
                continue

            if plate[i, j] == 'N':
                continue

            # going up
            up = (reward + discount_factor * (
                    transition_model * get_value(i, j, -1, 0) +
                    reverse_tran * get_value(i, j, -1, -1) +
                    reverse_tran * get_value(i, j, -1, 1)))

            # going down
            down = (reward + discount_factor * (
                    transition_model * get_value(i, j, 1, 0) +
                    reverse_tran * get_value(i, j, 1, 1) +
                    reverse_tran * get_value(i, j, 1, -1)))

            a = get_value(i, j, 0, 1)
            b = get_value(i, j, -1, 1)
            c = get_value(i, j, 1, 1)

            # going left
            left = (reward + discount_factor * (
                    transition_model * get_value(i, j, 0, -1) +
                    reverse_tran * get_value(i, j, 1, -1) +
                    reverse_tran * get_value(i, j, -1, -1)))

            # going right
            right = (reward + discount_factor * (
                    transition_model * get_value(i, j, 0, 1) +
                    reverse_tran * get_value(i, j, -1, 1) +
                    reverse_tran * get_value(i, j, 1, 1)))

            d = get_value(i, j, 1, 0)
            e = get_value(i, j, 1, -1)
            f = get_value(i, j, 1, +1)

            max_val = max(up, down, left, right)

            if max_val == up:
                plate[i, j] = 'U'
            elif max_val == down:
                plate[i, j] = 'D'
            elif max_val == left:
                plate[i, j] = 'L'
            else:
                plate[i, j] = 'R'


def output():
    with open('output0.txt', 'w') as outputFile:
        for i in range(0, grid - 1):
            outputFile.write(str(plate[i, 0]))
            for j in range(1, grid - 1):
                outputFile.write(',' + str(plate[i, j]))
            outputFile.write(str(',' + plate[i, grid - 1] + '\n'))

        outputFile.write(str(plate[grid - 1, 0]))
        for j in range(1, grid - 1):
            outputFile.write(',' + str(plate[grid - 1, j]))
        outputFile.write(str(',' + plate[grid - 1, grid - 1]))


def main():
    tick = time.time()
    # Read input file
    read_input()
    do_updating()
    check_operation()
    output()
    tick2 = time.time()
    print(tick2 - tick)
    print(str(plate_value))


main()

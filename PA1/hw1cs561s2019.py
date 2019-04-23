'''
    Filename: hw1cs561s2019.py
   
    Copyright: Yunfan Xue
   
    Author: Yunfan Xue (yunfanxu@usc.edu)

    Last Update Date: 01/23/2019
    
    Description: This "hw1cs561s2019.py" file belongs to the 19 spring CS561 Programing Assignment #1. 
                 This file is the simulation of Laser Checkmate game.
                 The program will generate one move at a time and use AI technique to win the game.
                 This file can only be read and tested by author, TAs, graders and professor. 
'''

import datetime
import random

my_Emitter_List = []
oppo_Emitter_List = []
wall_List = []
possible_List = []
ideal_step = []
SEARCH_DEPTH = 4
WALL = 3
number_N = 0
color = 1

def doRadarSpreading(plate, emitter_List):
    for point in emitter_List:

        # draw the emitter
        plate[point[0]][point[1]] = color

        # going up
        for j in range(1,4):
            if point[1] - j < 0 or plate[point[0]][point[1]] == 3:
                break
            else:
                plate[point[0]][point[1] - j] = color

        # going down
        for j in range(1,4):
            if point[1] + j >= number_N or plate[point[0]][point[1] + j] == 3:
                break
            else:
                plate[point[0]][point[1] + j] = color

        # going left
        for j in range(1,4):
            if point[0] - j < 0 or plate[point[0] - j][point[1]] == 3:
                break
            else:
                plate[point[0] - j][point[1]] = color
        
        # going right
        for j in range(1,4):
            if point[0] + j >= number_N or plate[point[0] - j][point[1]] == 3:
                break
            else:
                plate[point[0] + j][point[1]] = color

        # going left up
        for j in range(1,4):
            if point[1] - j < 0 or point[0] - j < 0 or plate[point[0] - j][point[1] - j] == 3:
                break
            else:
                plate[point[0] - j][point[1] - j] = color

        # going left down
        for j in range(1,4):
            if point[1] + j >= number_N or point[0] - j < 0 or plate[point[0] - j][point[1] + j] == 3:
                break
            else:
                plate[point[0] - j][point[1] + j] = color

        # going right up
        for j in range(1,4):
            if point[1] - j < 0 or point[0] + j >= number_N or plate[point[0] + j][point[1] - j] == 3:
                break
            else:
                plate[point[0] + j][point[1] - j] = color

        # going right down
        for j in range(1,4):
            if point[1] + j >= number_N or point[0] + j >= number_N or plate[point[0] + j][point[1] + j] == 3:
                break
            else:
                plate[point[0] + j][point[1] + j] = color
    #print(plate)
    return

def calcScore(emitter_List):
    cnt = 0
    plate = [[0 for i in range(number_N)] for j in range(number_N)]
    #print('This is from calcScore', plate)
    for wall in wall_List:
        plate[wall[0]][wall[1]] = 3

    doRadarSpreading(plate, emitter_List)

    for i in range(0, number_N):
        for j in range(0, number_N):
            if plate[i][j] == 1:
                cnt += 1
    return cnt

def determineFunc():
    myScore = calcScore(my_Emitter_List)
    oppoScore = calcScore(oppo_Emitter_List)
    return myScore - oppoScore

def isGameOver():
    global possible_List
    findPossibleMove()
    if len(possible_List) == 0:
        return True
    else:
        return False



def findPossibleMove():
    plate_2 = [[0 for i in range(number_N)] for j in range(number_N)]
    #print('possible path', plate_2)
    list1 = []
    global possible_List
    
    for wall in wall_List:
        plate_2[wall[0]][wall[1]] = 3
    doRadarSpreading(plate_2, my_Emitter_List)
    doRadarSpreading(plate_2,oppo_Emitter_List)

    for i in range(0, number_N):
        for j in range(0, number_N):
            if plate_2[i][j] == 0:
                for k in range(1,4):
                    if i + k < number_N and i - k >= 0 and j + k < number_N and j - k >= 0:
                        if plate_2[i + k][j] != 0 or plate_2[i - k][j] != 0 or plate_2[i][j + k] != 0 or plate_2[i][j - k] != 0:
                            list1.insert(0, [i,j])
                        else:
                            list1.append([i,j])
                    else:
                        list1.append([i,j])
    
    possible_List = list1

def doSearch(is_Me, depth, alpha, beta):
    #print('cur depth = ', depth)
    if isGameOver() or depth == 0:
    #if isGameOver():
        return determineFunc()

    findPossibleMove()
    random.shuffle(possible_List)
    next_move_list = possible_List
    global my_Emitter_List
    global oppo_Emitter_List
    global ideal_step
    if is_Me:
        value = float('-inf')
        for next_move in next_move_list:
            my_Emitter_List.append(next_move)
            value = max(value, doSearch(not is_Me, depth - 1, alpha, beta))
            if value > alpha:
                if depth == SEARCH_DEPTH:
                    ideal_step = next_move
            alpha = max(alpha, value)
            my_Emitter_List.remove(next_move)
            if beta <= alpha:
                break
        return value
    else:
        value = float('inf')
        for next_move in next_move_list:
            oppo_Emitter_List.append(next_move)
            value = min(value, doSearch(not is_Me, depth - 1, alpha, beta))
            if value > alpha:
                if depth == SEARCH_DEPTH:
                    ideal_step = next_move
            beta = min(beta, value)
            oppo_Emitter_List.remove(next_move)
            if beta <= alpha:
                break
        return value

def main():
    # read data from input file
    alpha = float('-inf')
    beta = float('inf')

    doSearch(True, SEARCH_DEPTH, alpha, beta)

    '''
    # write data to the output file
    with open('output.txt', 'w') as outputFile:
        outputFile.write(str(ideal_step[0]) + ' ' + str(ideal_step[1]))
    '''

def pvp():
    global number_N
    global my_Emitter_List
    global oppo_Emitter_List
    global wall_List
    row = 0
    with open('input3.txt', 'r') as inputFile:
        lines = inputFile.readlines()
        tempNum = lines[0]
        lines.remove(tempNum)
        number_N = int(tempNum)
        #print(lines)
        for line in lines:
            for i in range(0, number_N):
                if int(line[i]) == 1:
                    my_Emitter_List.append([row,i])
                if int(line[i]) == 2:
                    oppo_Emitter_List.append([row,i])
                if int(line[i]) == 3:
                    wall_List.append([row,i])

            row = row + 1
    me = True
    count = 1
    print('This is the 1 round\n')
    count += 1
    main()
    my_Emitter_List.append(ideal_step)
    me = not me
    while not isGameOver():
        print('This is the ', count,'round\n')
        count += 1
        main()
        if me:
            my_Emitter_List.append(ideal_step)
        else:
            oppo_Emitter_List.append(ideal_step)
        me = not me
    print('My steps: ', my_Emitter_List)
    print('Oppo steps: ', oppo_Emitter_List)
    print('score: ', determineFunc())


pvp()
#main()
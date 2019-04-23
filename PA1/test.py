number_N = 0
wall_List = []

def calcScore(number_N):
    cnt = 0
    plate = [[0 for i in range(number_N)] for j in range(number_N)]
    print(wall_List)
    print(plate)
    for wall in wall_List:
        print(wall[0] , wall[1])
        plate[wall[0]][wall[1]] = 3

    doRadarSpreading(plate, my_Emitter_List)

    for i in range(0, number_N):
        for j in range(0, number_N):
            if plate[i][j] == 1:
                cnt += 1
    return cnt

def main():
    
    row = 0
    with open('test1.txt', 'r') as inputFile:
        lines = inputFile.readlines()
        number_N = lines[0]
        lines.remove(number_N)
        number_N = int(number_N)
        #print(lines)
        for line in lines:
            for i in range(0, number_N):
                if int(line[i]) == 3:
                    wall_List.append([row,i])
            row += 1

    plate = [[0 for i in range(number_N)] for j in range(number_N)]
    print(plate)
    #print(number_N)
    print(wall_List)
    print(calcScore(number_N))
    
    '''
    with open('output.txt', 'w') as outputFile:
        outputFile.write(str(wall_List[0][0]) + ' ' + str(wall_List[0][1]))
    '''
main()
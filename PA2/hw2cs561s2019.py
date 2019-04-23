'''
    Filename: hw1cs561s2019.py
   
    Copyright: Yunfan Xue
   
    Author: Yunfan Xue (yunfanxu@usc.edu)

    Last Update Date: 02/27/2019
    
    Description: This "hw2cs561s2019.py" file belongs to the 19 spring CS561 Programing Assignment #2. 
                 This file can only be read and tested by author, TAs, graders and professor. 
'''
global_L = 0
global_G = 0
global_T = 0
lax = None

num_plane = 0
list_plane = []
critical_time = [] 
assigned_plane = []

#plane status:
BEFORE_LANDING = 1
LANDING = 2
AT_GATE = 3
TAKING_OFF = 4
AFTER_TAKING_OFF = 5
UNKNOW = -1

weight = 1
weight_2 = 1
solved = False

class flight:

    def __init__(self, R, M, S, O, C, ID):
        self.landing_upper = R
        self.landing_lower = 0
        self.R = R
        self.M = M
        self.S = S
        self.O = O
        self.C = C
        self.ID = ID

        self.assumed_landing_time = 0
        self.assumed_taking_off_time = 0
        self.taking_off_upper = 0
        self.taking_off_lower = 0

        self.landing_domain = []
        for j in range(0, R + 1):
            self.landing_domain.append(j)

        self.taking_off_domain = []

    def set_landing_time(self, time):
        if time < self.landing_lower or time > self.landing_upper:
            return False
        else:
            self.assumed_landing_time = time
            return True

    def set_taking_off_bound(self):
        self.taking_off_domain = []
        self.taking_off_lower = self.assumed_landing_time + self.S + self.M
        self.taking_off_upper = self.assumed_landing_time + self.C + self.M
        for j in range(self.taking_off_lower, self.taking_off_upper + 1):
            self.taking_off_domain.append(j)

    def set_taking_off_time(self, time):
        if time >= self.taking_off_lower and time <= self.taking_off_upper: 
            self.assumed_taking_off_time = time
            return True
        else:
            return False

    def cancel_assign_landing(self):
        self.assumed_landing_time = 0
        #self.assumed_taking_off_time = 0

    def cancel_assign_taking_off(self):
        self.assumed_taking_off_time = 0


    # this functino can only been used after assumed_landing_time and assumed_taking_off_time is initialized
    def get_status(self, time):
        status = UNKNOW
        if time < self.assumed_landing_time:
            status = BEFORE_LANDING
        elif time >= self.assumed_landing_time and time < self.assumed_landing_time + self.M:
            status = LANDING
        elif time >= self.assumed_landing_time + self.M and time < self.assumed_taking_off_time:
            status = AT_GATE
        elif time >= self.assumed_taking_off_time and time < self.assumed_taking_off_time + self.O:
            status = TAKING_OFF
        else:
            status = AFTER_TAKING_OFF

        return status



def key_priority(elem):
    return (elem.R * weight + elem.C * (1 - weight) + elem.M)

def key_id(elem):
    return elem.ID

def key_constraint(elem):
    return elem.landing_domain.len() * weight_2 + elem.taking_off_domain.len() * (1 - weight_2)

def sort_by_priority():
    global list_plane
    list_plane.sort(key = key_priority)

def sort_by_id():
    global assigned_plane
    assigned_plane.sort(key = key_id)


'''
    Unless there is a status change of plane, there is no need to check each 1 min time of status of the plane.
    Only list the time 1 min before the status change.
'''
def calc_critical_time():
    for plane in assigned_plane:
        critical_time.append(plane.assumed_landing_time)
        critical_time.append(plane.assumed_landing_time + plane.M)
        critical_time.append(plane.assumed_taking_off_time)
        critical_time.append(plane.assumed_taking_off_time + plane.O)


'''
    Check each plane's status on each critical time spot
'''
def check_constraints():

    global global_L
    global global_G
    global global_T

    global assigned_plane, critical_time

    critical_time = []
    calc_critical_time()


    for time_spot in critical_time:

        count_L = 0
        count_G = 0
        count_T = 0

        for plane in assigned_plane:
            if plane.get_status(time_spot) == LANDING:
                count_L += 1
            if plane.get_status(time_spot) == AT_GATE:
                count_G += 1
            if plane.get_status(time_spot) == TAKING_OFF:
                count_T += 1
        
        if count_L > global_L or count_G > global_G or count_T > global_T:
            return False

    return True

'''
def update_rest_domain():
    for plane in list_plane:
'''


def back_track():

    global list_plane, assigned_plane
    if len(list_plane) == 0 and check_constraints() == True:
        return True


    plane = list_plane.pop(0)
    for va in plane.landing_domain:
        plane.set_landing_time(va)
        plane.set_taking_off_bound()

        for vb in plane.taking_off_domain:
            plane.set_taking_off_time(vb)

            assigned_plane.append(plane)

            if check_constraints():
                #update_rest_domain()
                result = back_track()

                if result:
                    return result
            
            plane = assigned_plane.pop()


    # unable to find the solution.
    return False



def do_schedule():
    sort_by_priority()

    back_track()

    sort_by_id()



def output():
    with open('output.txt', 'w') as outputFile:
        for plane in assigned_plane:
            outputFile.write(str(plane.assumed_landing_time) + ' ' + str(plane.assumed_taking_off_time) + '\n')


def main():

    # Read input file
    with open('input.txt', 'r') as inputFile:
        lines = inputFile.readlines()
        airport_info = lines[0]

        global num_plane
        num_plane = int(lines[1])

        lines.remove(airport_info)
        lines.remove(lines[0])
        airport_info = airport_info.split()

        global global_L
        global global_G
        global global_T
        global_L = int(airport_info[0])
        global_G = int(airport_info[1])
        global_T = int(airport_info[2])

        i = 1
        for line in lines:
            temp_line = line.split()
            list_plane.append(flight(int(temp_line[0]), int(temp_line[1]), int(temp_line[2]), int(temp_line[3]), int(temp_line[4]), i))
            i += 1

    do_schedule()

    output()

main()
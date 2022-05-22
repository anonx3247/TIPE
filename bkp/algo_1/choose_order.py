import csv
import math
import sys, os

# constants for directions of movement
#pos = 1
#neg = -1
#bidir = 0
#block = 7
addr_col = 5
#directions = (pos, neg, bidir)
right = "r"
left = "l"
up = "u"
down = "d"


# reads csv and retrieves grid data
def get_grid(csv_reader):
    grid = []
    for index, row in enumerate(csv_reader):
        grid.append([])
        for j in row:
            if j == "9" or j == "5":
                grid[index].append(int(j))
            else:
                grid[index].append(0)


    return grid

# retrieves addresses from grid data
def get_addresses(grid):
    L = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == addr_col:
                L.append((j,i))
    return L

# gives order of addresses to visit
def order(start_pos, addresses):
    steps = []
    min = 1000
    next = 0
    if len(addresses) <= 1:
        return addresses
    else:
        for i in range(len(addresses)):
            d = get_dist(start_pos, addresses[i])
            if d < min:
                min = d
                next = i
        steps = [addresses[next]] + order(addresses[next], addresses[:next] + addresses[next+1:])
        return steps

def sort_first(val):
    return val[0]

# returns distance between two points
def get_dist(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.sqrt(dx**2 + dy**2)

# returns angle between two points
def get_angle(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    #print("dx: {}, dy: {}".format(dx,dy))

    if dx == 0:
        theta = 3*math.pi/2
    elif dy == 0:
        theta = 0
    elif dx < 0 and dy  <0:
        theta = math.pi + math.atan(dy/dx)
    else:
        theta = math.atan(dy/dx)
    #print("theta: {}".format(theta/math.pi))
    return theta

def read_sep(grid):
    counter = 1
    for i in grid:
        for j in range(len(i)):
            if j != 0:
                if i[j] == 9:
                    counter += 1
                else:
                    return counter+1

# main execution

path = sys.argv[-1]

if path == "choose_order.py":
    i = 0
    while os.path.exists("grids/grid{:04d}.csv".format(i)):
        i += 1
    path = "grids/grid{:04d}.csv".format(i-1)


print("File: {}".format(path))
# close csv file
# imprt and read just exported csv file
csvimport = open(path, "r")
reader = csv.reader(csvimport, delimiter=',')
grid = get_grid(reader)
csvimport.close()

start = (0,0)
print("Start: ", start)
print("Grid: ", grid)
sep = read_sep(grid)
print("Sep: ", sep)
addresses = get_addresses(grid)
print("Addresses: ", addresses)
order = order(start, addresses)
print("Order: ", order)


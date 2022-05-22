#!/usr/bin/python3.10
import csv
import random
import math
import sys

# constants for directions of movement
bidir = 0
addr_col = 5
sep = 2


# generates city grid data
def gen_city(size, sep, addr):
    grid = []

    gridlines = range(0, size, sep)

   # Initialise grid values
    for i in range(size):
        grid.append([])
        for j in range(size):
            grid[i].append(9)

    addresses_x = random.choices(range(size//sep), k=addr)
    addresses_y = random.choices(range(size//sep), k=addr)

    # make default rows
    for i in gridlines:
        for j in range(size):
            grid[i][j] = bidir

    # make default columns
    for i in gridlines:
        for j in range(size):
            grid[j][i] = bidir

    # insert addresses
    for i in range(addr):
            x, y = addresses_x[i]*sep+1, addresses_y[i]*sep+1
            grid[x][y] = addr_col

    return grid


# writes grid to csv file
def gen_csv(grid, csv_writer):
    for i in grid:
        csv_writer.writerow(i)

# constants for directions of movement
traj = 8

right = "⟶"
left = "⟵"
up = "↑"
down = "↓"


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
                L.append((j, i))
    return L


# gives order of addresses to visit
def order(start_pos, addresses):
    steps = []
    min = math.inf
    next = 0
    if len(addresses) <= 1:
        return addresses
    else:
        for i in range(len(addresses)):
            d = get_dist(start_pos, addresses[i])
            if d < min:
                min = d
                next = i
        steps = [addresses[next]] + order(
            addresses[next], addresses[:next] + addresses[next+1:]
            )
        return steps


def sort_first(val):
    return val[0]


# give trajectory
def trajectory(pos1, pos2, sep):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    lx = abs(dx)//sep
    ly = abs(dy)//sep
    trail = []
    if dx >= 0:
        trail += [right]*lx
    elif dx < 0:
        trail += [left]*lx
    if dy >= 0:
        trail += [down]*ly
    elif dy < 0:
        trail += [up]*ly
    newpos = exec_trail(pos1, trail)
    return trail, newpos


def exec_trail(start_pos, t):
    pos = start_pos
    for i in t:
        x,y = pos
        if i == right:
            pos = (x + sep, y)
        elif i == left:
            pos = (x - sep, y)
        elif i == up:
            pos = (x, y - sep)
        elif i == down:
            pos = (x, y + sep)
    return pos


def draw_trajectory(start, t, grid):
    pos = start
    for i in range(len(t)):
        x,y = pos
        grid[x][y] = traj
        if i == len(t) - 1:
            last = True
        else:
            last = False
        # for some reason again the directions are inverted so down = right and up = left
        if t[i] == down:
            grid = fill("x+", pos, grid, sep, last)
            pos = (x + sep, y)
        elif t[i] == up:
            grid = fill("x-", pos, grid, sep, last)
            pos = (x - sep, y)
        elif t[i] == left:
            grid = fill("y+", pos, grid, sep, last)
            pos = (x, y - sep)
        elif t[i] == right:
            grid = fill("y-", pos, grid, sep, last)
            pos = (x, y + sep)
    return grid


def fill(axis, pos, grid, sep, last):
    x, y = pos
    if axis == "x+":
        for i in range(x, x+sep):
            grid[i][y] = traj
        if last:
            grid[x+sep][y] = traj

    elif axis == "y+":
        for i in range(y-sep, y):
            grid[x][i] = traj
        if last:
            grid[x][y-sep-1] = traj

    elif axis == "x-":
        for i in range(x-sep, x):
            grid[i][y] = traj
        if last:
            grid[x-sep-1][y] = traj

    elif axis == "y-":
        for i in range(y, y+sep):
            grid[x][i] = traj
        if last:
            grid[x][y+sep] = traj
    return grid


def trail(ord, sep):
    t = []
    pos = ord[0]
    for i in range(1, len(ord)):
        traj, pos = trajectory(pos, ord[i], sep)
        t += traj
    return t


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
    elif dx < 0 and dy < 0:
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


def print_trail(t):
    s = "Trail: [ "

    for i in t:
        s += i + " "

    s += "]"
    print(s)


def print_order(o):
    s = "Order: [ "

    for i in o:
        s += "(" + str(i[0]) + " " + str(i[1]) + ") "

    s += "]"
    print(s)


i_path = sys.argv[1]
o_path = sys.argv[2]
grid = []
with open(i_path, "w") as csvfile:
    newgrid = gen_city(50, sep, 25)
    writer = csv.writer(csvfile, delimiter=',')
    gen_csv(newgrid, writer)
    csvfile.close()

with open(i_path, "r") as csvimport:
    reader = csv.reader(csvimport, delimiter=',')
    grid = get_grid(reader)
    csvimport.close()

start = (0, 0)
sep = read_sep(grid)
addresses = get_addresses(grid)
order = order(start, addresses)
print_order(order)
trail = trail([start] + order, sep)
print_trail(trail)

grid = draw_trajectory(start, trail, grid)
with open(o_path, "w") as trajectory_file:
    writer = csv.writer(trajectory_file, delimiter=',')
    gen_csv(grid, writer)
    trajectory_file.close()

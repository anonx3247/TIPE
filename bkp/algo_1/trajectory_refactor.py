import csv
import math
from enum import Enum
from copy import copy


class axis(Enum):
    x = 0
    y = 1


class direction:
    def __init__(self, dir, rep):
        self.dir = dir
        self.string = rep


right = direction((1, 0), "⟶")
left = direction((-1, 0), "⟵")
up = direction((0, -1), "↑")
down = direction((0, 1), "↓")


color = {"traj": 8, "addr": 5, "sep": 9}


class point:
    def __init__(self, x_v, y_v, sep):
        self.x = x_v
        self.y = y_v
        self.sep = sep

    def move(self, dir):
        self.x += dir.dir[0] * self.sep
        self.y += dir.dir[1] * self.sep

    def dist(self, pos):
        return math.sqrt((pos.x - self.x)**2 + (pos.y - self.y)**2)


class matrix:
    def __init__(self, L):
        self.len = len(L)
        self.pts = {}
        for i in range(len(L)):
            for j in range(len(L[i])):
                self.pts[(i, j)] = L[i][j]
        self.sep = read_sep(L)

    def __getitem__(self, p):
        return self.pts[(p.x, p.y)]

    def __setitem__(self, p, d):
        self.pts[(p.x, p.y)] = d

    def addr(self):
        addr = []
        for k, v in self.pts.items():
            if v == color["addr"]:
                addr.append(point(k[0], k[1], self.sep))
        return addr

    def to_list(self):
        L = []
        for i in range(self.len):
            L.append([])
            for j in range(self.len):
                L[i].append(self.pts[(i, j)])
        return L

    def from_csv(csv_reader):
        grid = []
        for index, row in enumerate(csv_reader):
            grid.append([])
            for j in row:
                if j == str(color["sep"]) or j == str(color["addr"]):
                    grid[index].append(int(j))
                else:
                    grid[index].append(0)

        return matrix(grid)


# reads csv and retrieves grid data
def grid_from_csv(csv_reader):
    grid = []
    for index, row in enumerate(csv_reader):
        grid.append([])
        for j in row:
            if j == str(color["sep"]) or j == str(color["addr"]):
                grid[index].append(int(j))
            else:
                grid[index].append(0)

    return matrix(grid)


# gives order of addr to visit
def visit_order(start_pos, addr):
    if len(addr) <= 1:
        return addr
    else:
        distances = [(start_pos.dist(addr[i]), i) for i in range(len(addr))]
        shortest_dist = min(distances)
        next = shortest_dist[1]
        steps = [addr[next]] + visit_order(addr[next],
                                           addr[:next] + addr[next+1:])
        return steps


def trajectory(pos1, pos2):
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    lx = abs(dx)//pos1.sep
    ly = abs(dy)//pos1.sep
    trail = []
    for i in [right, left, up, down]:
        if (dx/abs(dx), 0) == i.dir:
            trail += [i] * lx
        elif (0, dy/abs(dy)) == i.dir:
            trail += [i] * ly

    return trail, move_on_trajectory(pos1, trail)


def move_on_trajectory(start_pos, t):
    pos = copy(start_pos)
    for i in t:
        pos.move(i)
    return pos


def draw_trajectory(start, t, grid):
    pos = copy(start)
    length = len(t)
    for i in range(length):
        grid[pos] = color["traj"]
        grid = fill(t[i], pos, grid, i == length - 1)
        pos.move(t[i])
    return grid


def fill(dir, pos, grid, last):
    pos = copy(pos)
    if dir == right:
        for i in range(pos.x, pos.x+pos.sep):
            pos.x = i
            grid[pos] = color["traj"]
        if last:
            pos.x += pos.sep
            grid[pos] = color["traj"]

    elif dir == up:
        for i in range(pos.y-pos.sep, pos.y):
            pos.y = i
            grid[pos] = color["traj"]
        if last:
            pos.y -= pos.sep + 1
            grid[pos] = color["traj"]

    elif dir == left:
        for i in range(pos.x-pos.sep, pos.x):
            pos.x = i
            grid[pos] = color["traj"]
        if last:
            pos.x -= pos.sep + 1
            grid[pos] = color["traj"]

    elif dir == down:
        for i in range(pos.y, pos.y+pos.sep):
            # grid[pos.x][i] = color["traj"]
            pos.y = i
            grid[pos] = color["traj"]
        if last:
            # grid[pos.x][pos.y+pos.sep] = color["traj"]
            pos.y += pos.sep
            grid[pos] = color["traj"]
    return grid


def trail(ord):
    t = []
    pos = ord[0]
    for i in range(1, len(ord)):
        traj, pos = trajectory(pos, ord[i])
        t += traj
    return t


def read_sep(grid):
    counter = 1
    length = len(grid)
    for i in grid:
        for j in range(length):
            if j != 0:
                if i[j] == color["sep"]:
                    counter += 1
                else:
                    return counter+1


# writes grid to csv file
def grid_to_csv(grid, csv_writer):
    for i in grid.to_list():
        csv_writer.writerow(i)


def set_params(grid):
    sep = grid.sep
    start = point(0, 0, sep)
    addr = grid.addr()
    ord = visit_order(start, addr)
    trails = trail([start] + ord)
    return start, sep, addr, ord, trails


def print_params(start, sep, ord, trail):
    print("Start: ", start)
    print("Sep: ", sep)
    print("Order: ", ord)


path = "grid.csv"
print("File: {}".format(path))
csvimport = open(path, "r")
reader = csv.reader(csvimport, delimiter=',')
grid = matrix.from_csv(reader)
csvimport.close()

start, sep, addr, ord, trails = set_params(grid)
# print_params(start, sep, addr, ord, trails)

print("Drawing trajectory...")
grid = draw_trajectory(start, trails, grid)

trajectory_file = open("T.csv", "w")
writer = csv.writer(trajectory_file, delimiter=',')
grid_to_csv(grid, writer)
trajectory_file.close()


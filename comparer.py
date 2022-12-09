#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:48:51 2022

@author: neosapien
"""

import os
from time import time
from matplotlib import pyplot as plt
import numpy as np


executables = ["execs/one", "execs/two"]
times = []

src = "tests/grid"
dest = "tests/traj"

n = 1000


def execute(ex, n):
    t1 = time()
    for i in range(3):
        # example: ex grid32.csv traj32.csv 32
        os.system(
            "./" + ex + " " + src + str(n) + " " + dest + str(n) + " " + str(n)
        )
    t2 = time()
    return t2 - t1


for executable in executables:
    times.append([])
    for i in range(n):
        times[-1].append(execute(executable, i))

N = np.array([i for i in range(n)])
a, b, c = np.polyfit(N, times[0], 2)
a2, b2, c2 = np.polyfit(N, times[1], 2)
plt.plot(
    N,
    times[0],
    "r",
    N,
    times[1],
    "b",
    N,
    a * N**2 + b * N + c,
    "r--",
    N,
    a2 * N**2 + b2 * N + c2,
    "b--",
)
plt.xlabel("n")
plt.ylabel("temps")

import math
from itertools import combinations, chain
import re
import time

import numpy as np
import numba as nb


# @nb.njit(nb.void(nb.int64[:, :], nb.int64), fastmath=True)
def compiledVStep(simArray, height):
    # for every combination of rows
    for i in range(height - 1):
        for j in range(i + 1, height):
            for k in range(3):
                if simArray[i, k] > simArray[j, k]:
                    simArray[i, k] -= 1
                    simArray[j, k] += 1
                elif simArray[i, k] < simArray[j, k]:
                    simArray[i, k] += 1
                    simArray[j, k] -= 1


# @nb.njit(nb.void(nb.int64[:, :]))
def compiledPStep(simArray):
    # for i in range(height):
    #     simArray[i, :3] += simArray[i, 3:]
    simArray[:, :3] += simArray[:, 3:]


# @nb.njit(nb.boolean(nb.int16[:, :], nb.int16[:, :]))
def checkOneSame(simArray, initCond):
    for i in range(4):
        for j in range(6):
            if simArray[i, j] != initCond[i, j]:
                return False
    return True


# @nb.njit(nb.boolean(nb.int16[:, :], nb.int16[:, :, :], nb.int64), parallel=True)
def checkDiff(simArray, initConds, length):
    # for every set of conditions, if one is precisely the same, then return false
    for i in range(length):
        same = checkOneSame(simArray, initConds[..., i])
        if same:  # if this condition is the same, return false
            return False
    return True  # if no conditions returned true, return True


# New Plan:
# Since every axis is independant, calculate the number of positions until full reset.  Start by assuming that there is
# no other repetition.  The
@nb.jit()
def compiledSim(simArray):
    # each line will be a body, columns 0-2 will be x, y, and z positions, and columns 3-5 will be x, y,
    # and z velocities
    simArray = simArray.astype(np.int16)
    initCond = np.zeros((4, 6, 1000000), dtype=np.int16)
    initCond[..., 0] = simArray
    height, width = simArray.shape

    # for each of x, y, and z
    idxs = [0, 0, 0]
    for pos, vel in [(0, 3), (1, 4), (2, 5)]:
        # Slice new sim array
        axPos = simArray[:, pos]
        axVel = simArray[:, vel]

        while True:
            pass
            # update velocity
            for i in range(4):
                axVel[i] += (axPos[i] < axPos).sum() - (axPos[i] > axPos).sum()

            # update position
            axPos += axVel

            # if position and velocity are identical to the first, continue
            idxs[pos] += 1
            if (initCond[:, pos, 0] == axPos).all() and (initCond[:, vel, 0] == axVel).all():
                break

            # otherwise, move the correct index up, and add to the conditions array
            initCond[:, pos, idxs[pos]] = axPos
            initCond[:, vel, idxs[pos]] = axVel

    return np.lcm.reduce(idxs, dtype=np.int64)


class Body(object):
    def __init__(self, position, velocity=None):
        self.position = np.array(position, dtype=np.int64)

        if velocity is not None:
            self.velocity = np.array(velocity, dtype=np.int64)
        else:
            self.velocity = np.array([0, 0, 0], dtype=np.int64)

    def __repr__(self):
        return "<Body pos=[%d, %d, %d], vel=[%d, %d, %d]>" % tuple(chain(self.position, self.velocity))

    def v_step(self, other):
        diff = np.sign(self.position - other.position)
        self.velocity -= diff
        other.velocity += diff

    def p_step(self):
        self.position += self.velocity

    @property
    def potential(self):
        return np.abs(self.position).sum()

    @property
    def kinetic(self):
        return np.abs(self.velocity).sum()

    @property
    def energy(self):
        return self.potential*self.kinetic


class Simulation(object):
    def __init__(self, bodies):
        self.bodies = bodies
        self.time = 0
        self.initPositions = tuple(body.position.copy() for body in bodies)

    def v_step(self):
        for a, b in combinations(self.bodies, 2):
            a.v_step(b)

    def p_step(self):
        for x in self.bodies:
            x.p_step()

    def step(self, n_steps=1):
        for x in range(n_steps):
            self.v_step()
            self.p_step()

    @property
    def energy(self):
        return sum([x.energy for x in self.bodies])

    def positionsReset(self):
        for init, body in zip(self.initPositions, self.bodies):
            for iCoord, bCoord in zip(init, body.position):
                if iCoord != bCoord:
                    return False
        return

    def reset(self):
        for init, body in zip(self.initPositions, self.bodies):
            body.position = init.copy()
            body.velocity = np.array([0, 0, 0], np.int64)

    def stepToReset(self):
        self.step(1)
        i = 1
        while not self.positionsReset():
            i += 1
            self.step(1)
            if i % 100000 == 0:
                print(i)
                print(self.posDiff())

    def posDiff(self):
        lines = ["<%d, %d, %d>" % tuple(x - y) for x, y in zip(self.initPositions, [x.position for x in self.bodies])]
        return "\r\n".join(lines)


if __name__ == "__main__":

    # Read and initialize stuff, simulation and moons to start
    with open("./input.txt") as f:
        inputLines = f.readlines()
    bodies = []
    coordPattern = re.compile("<x=(.+), y=(.+), z=(.+)>")
    for line in inputLines:
        bodies.append(Body([int(x) for x in coordPattern.findall(line)[0]]))
    sim = Simulation(bodies)

    # run for a thousand steps
    sim.step(1000)

    # print energy
    print(sim.energy)

    # reset
    sim.reset()

    # run to completion
    simArray = np.stack([np.append(x.position, x.velocity) for x in sim.bodies])
    result = compiledSim(simArray)
    print(result)

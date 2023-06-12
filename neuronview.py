import numpy as np
from sdf import *
import sys
import os

IDX_X = 0
IDX_Y = 1
IDX_Z = 2
IDX_R = 3
IDX_PID = 4

points = {}
rootIdx = None

def makePart(firstIDX, stride, dir):
    lastIDX = firstIDX + stride
    lastIDX = min(lastIDX, maxID)
    print('making part from', firstIDX, 'to', lastIDX)
    
    for i in range(firstIDX, lastIDX):
        if (i == firstIDX):
            cell = sphere(points[i][IDX_R], (points[i][IDX_X], points[i][IDX_Y], points[i][IDX_Z]))
        else:    
            if (points[i][IDX_PID] == -1):
                continue
            parent = points[points[i][IDX_PID]]
            start = (points[i][IDX_X], points[i][IDX_Y], points[i][IDX_Z])
            end = (parent[IDX_X], parent[IDX_Y], parent[IDX_Z])
            r1 = points[i][IDX_R]
            r2 = parent[IDX_R]
            cell |= capsule2(start, end, r1, r2)

    outname = dir + "/cell_" + str(firstIDX) + "_" + str(lastIDX) + ".stl"

    cell.save(outname, step=(minRadius))


if __name__ == "__main__":    
    maxID = -1
    minRadius = 1000000

    sourcefile = sys.argv[1]
    stride = int(sys.argv[2])

    filename = os.path.basename(sourcefile)
    name = filename.split('.')[0]
    print('processing', name)

    if not os.path.exists('./output'):
        os.makedirs('./output')

    if not os.path.exists('./output/' + name):
        os.makedirs('./output/' + name)

    # process each line of the file
    with open(sourcefile) as f:
        for line in f:
            if (line.startswith('#')):
                continue
            parts = line.lstrip().split(' ')
            id, type, x, y, z, r, pid = parts
            id = int(id)
            pid = int(pid)
            points[id] = (float(x), float(y), float(z), float(r), pid)
            if (pid == -1):
                rootIdx = id

            if (maxID < id):
                maxID = id

            if (minRadius > float(r)):
                minRadius = float(r)

    root = points[rootIdx]

    curr = 1
    while (curr < maxID):
        makePart(curr, stride, './output/' + name)
        curr += stride

    print('DONE!')
import numpy as np
from sdf import *

sourcefile = "./swcs/AX3_scaled.swc"

points = {}
rootIdx = None

IDX_X = 0
IDX_Y = 1
IDX_Z = 2
IDX_R = 3
IDX_PID = 4

maxID = -1

minRadius = 1000000

# process each line of the file
with open(sourcefile) as f:
    for line in f:
        if (line.startswith('#')):
            continue
        parts = line.split(' ')
        # id,type,x,y,z,r,pid
        id, type, x, y, z, r, pid = parts
        id = int(id)
        pid = int(pid)
        points[id] = (float(x), float(y), float(z), float(r), pid)
        # print(id, points[id])
        if (pid == -1):
            rootIdx = id

        if (maxID < id):
            maxID = id

        if (minRadius > float(r)):
            minRadius = float(r)


root = points[rootIdx]
# print(root)
# cell = sphere(root[IDX_R], (root[IDX_X], root[IDX_Y], root[IDX_Z]))

stride = 325

def makePart(firstIDX):
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

    outname = "output/cell_" + str(firstIDX) + "_" + str(lastIDX) + ".stl"

    cell.save(outname, step=(minRadius / 2))

makePart(50)

curr = 50
while (curr < maxID):
    # makePart(curr)
    curr += stride

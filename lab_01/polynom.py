import numpy as numpy
from Point_class import Point
from itertools import product
from file_funcs import *


def getIndex(points, x):
    dif = abs(points[0].x - x)
    index = 0
    for i in range(len(points)):
        if abs(points[i].x - x) < dif:
            dif = abs(points[i].x - x)
            index = i
    return index


def getWorkingPoints(points, index, n):
    left = index
    right = index
    for i in range(n - 1):
        if i % 2 == 0:
            if left == 0:
                right += 1
            else:
                left -= 1
        else:
            if right == len(points) - 1:
                left -= 1
            else:
                right += 1

    return points[left:right + 1]

def NewtoneTableCreate(table, n):
    newtoneTable = []

    # copy point in newtoneTable as just floats
    for row in range(len(table)):
        new_row = []
        new_row.append(table[row].x)
        new_row.append(table[row].y)
        newtoneTable.append(new_row)

    for i in range(1, n + 1):
        for j in range(0, n + 1 - i):
            raznost = (newtoneTable[j][len(newtoneTable[j]) - 1] - newtoneTable[j + 1][len(newtoneTable[j]) - 1]) / \
                      (newtoneTable[j][0] - newtoneTable[j + i][0])
            newtoneTable[j].append(raznost)

    return newtoneTable

def print_newtoneTable(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(table[i][j], end=" ")
        print("\n")

def NewtonePolyCount(table, x):
    poly = table[0][1]
    tmp = 1
    for i in range(len(table[0]) - 2):
        tmp *= (x - table[i][0])
        poly += table[0][i + 2] * tmp

    return poly

def HermitTableCreate(table, n):
    hermitTable = []

    for row in range(len(table)):
        new_row = []
        new_row.append(table[row].x)
        new_row.append(table[row].y)
        new_row.append(table[row].derivative)
        hermitTable.append(new_row)
        tmp = []
        tmp.append(table[row].x)
        tmp.append(table[row].y)
        tmp.append(table[row].derivative)
        hermitTable.append(tmp)

    # for row_new, row_old in product(range(0, len(hermitTable), 2), range(0, len(table))):
    #     hermitTable[row_new].append(table[row_old].derivative)

    i = 0
    for row in range(0, len(hermitTable) - 1, 2):
        hermitTable[row].append(table[i].derivative)
        i += 1


    for row in range(1, len(hermitTable) - 1, 2):
        hermitTable[row].append((hermitTable[row][1] - hermitTable[row + 1][1]) /\
                              (hermitTable[row][0] - hermitTable[row + 1][0]))


    for i in range(2, (n + 1) * 2 + 1):
        for j in range(0, (n + 1) * 2 - i):
            # if abs(hermitTable[j][0] - hermitTable[j+1][0]) < 1e-8:
            #     raznost = hermitTable[j][2]
            #
            # else:
            #     raznost = (hermitTable[j][len(hermitTable[j]) - 1] - hermitTable[j + 1][len(hermitTable[j]) - 1]) / \
            #           (hermitTable[j][0] - hermitTable[j + i][0])

            raznost = (hermitTable[j][len(hermitTable[j]) - 1] - hermitTable[j + 1][len(hermitTable[j]) - 1]) / \
                      (hermitTable[j][0] - hermitTable[j + i][0])
            hermitTable[j].append(raznost)

    return hermitTable



def print_hermitTable(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(table[i][j], end="\t")
        print("\n")

def HermitPolyCount(table, n, x):
    poly = table[0][1]
    tmp = 1
    for i in range(n):
        tmp *= (x - table[i][0])
        poly += table[0][i + 3] * tmp

    return poly

def printSubTable(subTable):
    countArray = len(subTable[0])
    maxLen = len(subTable)
    print(("+" + "─" * 22) * countArray + "+")
    print("│ {:^20s} │ {:^20s}".format("X", "Y"), end=' ')
    for k in range(2, countArray):
        print("│ {:^20s}".format("Y" + "\'" * (k - 1)), end=' ')
    print("│")
    print(("+" + "─" * 22) * countArray + "+")

    for i in range(maxLen):
        for j in range(countArray):
            if j >= countArray - i:
                print("│ {:^20s}".format(" "), end=' ')
            else:
                print("│ {:^20.10f}".format(subTable[i][j]), end=' ')
        print("│")

    print(("+" + "─" * 22) * countArray + "+")

def is_Monotone(pointTable):
    isIncreasing = True
    isDecreasing = True
    for i in range(len(pointTable) - 1):
        if (pointTable[i].x < pointTable[i + 1].x and pointTable[i].y >= pointTable[i].y):
            isIncreasing = False

    for i in range(len(pointTable) - 1):
        if (pointTable[i].x > pointTable[i + 1].x and pointTable[i].y <= pointTable[i].y):
            isDecreasing = False

    if isIncreasing or isDecreasing:
        return 1
    else:
        return 0

def rootNewton(table, n):
    # if is_Monotone(table) == 0:
    #     newtonTable = NewtoneTableCreate(table, n)
    #     r = table[-1].x
    #     l = table[0].x
    #     while r - l > 1e-8:
    #         m = (r + l) / 2
    #         y = NewtonePolyCount(newtonTable, m)
    #         if y < 0:
    #             l = m
    #         else:
    #             r = m
    #     return l

    newTable = []
    for point in table:
        newTable.append(Point(point.y, point.x, 0))

    newTable.sort(key=lambda point: point.x)
    index = getIndex(newTable, 0)
    newPointTable = getWorkingPoints(newTable, index, n + 1)
    newtonTable = NewtoneTableCreate(newPointTable, n)

    return NewtonePolyCount(newtonTable, 0)

def rootHermit(table, n):
    newTable = []
    for point in table:
        if point.derivative != 0:
            newTable.append(Point(point.y, point.x, 1 / point.derivative))

    newTable.sort(key=lambda point: point.x)
    hermitTable = HermitTableCreate(newTable, n)

    return HermitPolyCount(hermitTable, (n + 1) * 2 - 1, 0)

def find_system_root():
    table1 = readTable('./data/data_2.txt')
    table2 = readTable('./data/data_3.txt')

    n = 3

    difTable = []
    for point in table1:
        difTable.append(Point(point.y, point.x, 0))

    newtonTable = NewtoneTableCreate(difTable, len(table1) - 1)

    newTable = []

    for i in range(len(table2)):
        newTable.append(Point(table2[i].x, table2[i].y - NewtonePolyCount(newtonTable, table2[i].x), 0))
        # tmp = []
        # tmp.append(table2[i].x)
        # tmp.append(table2[i].y - NewtonePolyCount(newtonTable, table2[i].x))
        # tmp.append(None)
        # newTable.append(tmp)

    print("Новая таблица")
    #printNewTable(newTable)
    printTableRoot(newTable)


    newnewtable = newTable[0:9]



    root = rootNewton(newnewtable, n)

    index = getIndex(table2, root)
    newPointTable = getWorkingPoints(table2, index, n + 1)

    newtoneTable2 = NewtoneTableCreate(newPointTable, n)
    root_y = NewtonePolyCount(newtoneTable2, root)
    print("x: {}". format(root))
    print("y: {}".format(root_y))


def printTableRoot(table):
    print("┌───────┬────────────┬────────────┐")
    print("│ {:^5s} │ {:^10s} │ {:^10s} │".format("№", "X", "Y"))
    print("├───────┼────────────┼────────────┤")
    for i in range(len(table)):
        print("│ {:^5d} │ {:^10.3f} │ {:^10.3f} │".format(i, table[i].x, table[i].y))
    print("└───────┴────────────┴────────────┘")

def printNewTable(table):
    print("┌───────┬────────────┬────────────┐")
    print("│ {:^5s} │ {:^10s} │ {:^10s} │".format("№", "X", "Y1 -Y2"))
    print("├───────┼────────────┼────────────┤")
    for i in range(len(table)):
        print("│ {:^5d} │ {:^10.3f} │ {:^10.3f} │".format(i, table[i][0], table[i][1]))
    print("└───────┴────────────┴────────────┘")

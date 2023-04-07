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

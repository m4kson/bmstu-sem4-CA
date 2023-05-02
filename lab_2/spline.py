from point_class import Point
from NewtonePolynom import *

def read_table(filename):
    file = open(filename, "r")
    if file == None:
        return -1

    table = []
    for line in file:
        line = line.split()
        table.append(Point(float(line[0]), float(line[1])))

    return table

def print_pointTable(table):
    print("┌───────┬────────────┬────────────┐")
    print("│ {:^5s} │ {:^10s} │ {:^10s} │".format("№", "X", "Y"))
    print("├───────┼────────────┼────────────┤")

    for i in range(len(table)):
        print("│ {:^5d} │ {:^10.3f} │ {:^10.3f} │".format(i, table[i].x, table[i].y,))

    print("└───────┴────────────┴────────────┘")

def spline(table, x, start, end):
    xValues = [i.getX() for i in table]
    yValues = [i.getY() for i in table]

    #находим коэффициенты для Ф(x) = a + b * (x - x_0) + c * (x - x_0)^2 + d * (x - x_0)^3
    coeffs = calculateCoefs(xValues, yValues, start, end)

    #находим индекс табличного икса ближайшего к заданному иксу
    index = finedIndex(xValues, x)

    #Вычисляем апроксимированную ф-цию
    y = countPolynom(x, xValues, index, coeffs)

    return y

def calculateCoefs(xValues, yValues, start, end):
    aValues = findAVAlues(yValues)
    cValues = findCValues(xValues, yValues, start, end)
    bValues = findBValues(xValues, yValues, cValues)
    dValues = findDValues(xValues, cValues)

    return aValues, bValues, cValues, dValues

def findAVAlues(yValues):
    AValues = []
    for i in range(len(yValues) - 1):
        AValues.append(A(yValues[i]))
    return AValues

def A(x):
    return x

def findCValues(xValues, yValues, start, end):
    sizeX = len(xValues)

    cValues = [0] * (sizeX - 1)
    cValues[0] = start / 2
    cValues[-1] = end / 2
    if start == 0 and end == 0:
        ksiValues = [0, 0]
        tetaValues = [0, 0]
    elif end == 0:
        ksiValues = [0, start / 2]
        tetaValues = [0, start / 2]
    else:
        ksiValues = [start / 2, start / 2]
        tetaValues = [start / 2, start / 2]

    for i in range(2, sizeX):
        h2 = xValues[i] - xValues[i - 1]
        h1 = xValues[i - 1] - xValues[i - 2]

        fiCur = fi(yValues[i - 2], yValues[i - 1], yValues[i], h1, h2)
        ksiCur = ksi(ksiValues[i - 1], h1, h2)
        tetaCur = teta(fiCur, tetaValues[i - 1], ksiValues[i - 1], h1, h2)

        ksiValues.append(ksiCur)
        tetaValues.append(tetaCur)

    for i in range(sizeX - 2, 0, -1):
        cValues[i - 1] = C(cValues[i], ksiValues[i], tetaValues[i])

    return cValues

# y1 = y_i-1
# y2 = y_i
# hi
# c1 = c_i+1
# c2 = c_i

def C(c_i, ksi_i, teta_i):
    return ksi_i * c_i + teta_i

# y1 = yi-2
# y2 = yi-1
# y3 = yi
# h1 = hi-1
# h2 = hi
def fi(y1, y2, y3, h1, h2):
    return 3 * ((y3 - y2) / h2 - (y2 - y1) / h1)


# функция ksi - расcчтывает значение ksi i-го элемента
# ksi_i+1 = -h_i / (h_i-1  * ksi_i-1 * (h_i - h_i-1))
# ksi_i = -h_i-1 / (h_i  * ksi_i + 2 * (h_i-1 - h_i))
# ksi1 = ksi_i-1
# h1 = h_i-1
# h2 = h_i
def ksi(ksi1, h1, h2):
    return - h1 / (h2 * ksi1 + 2 * (h2 + h1))


# fi - значение из функции fi()
# teta - teta_i-1
# ksi - ksi_i-1
# h1 - h_i-1
# h2 - h_i
def teta(fi, teta_i, ksi_i, h1, h2):
    return (fi - h1 * teta_i) / (h1 * ksi_i + 2 * (h2 + h1))

def findBValues(xValues, yValues, cValues):
    bValues = list()
    for i in range(1, len(xValues) - 1):
        hi = xValues[i] - xValues[i - 1]
        bValues.append(B(yValues[i - 1], yValues[i], cValues[i - 1], cValues[i], hi))

    hi = xValues[-1] - xValues[-2]
    bValues.append(B(yValues[-2], yValues[-1], 0, cValues[-1], hi))

    return bValues


def findDValues(xValues, cValues):
    dValues = []

    size = len(xValues)

    for i in range(1, size - 1):
        hi = xValues[i] - xValues[i - 1]
        dValues.append(D(cValues[i], cValues[i - 1], hi))

    hi = xValues[-1] - xValues[-2]
    dValues.append(D(0, cValues[-1], hi))

    return dValues

def D(c1, c2, hi):
    return (c1 - c2) / (3 * hi)

# y1 = y_i-1
# y2 = y_i
# hi
# c1 = c_i+1
# c2 = c_i
def B(y1, y2, c1, c2, hi):
    return (y2 - y1) / hi - (hi * (c2 + 2 * c1) / 3)

def countPolynom(x, xValues, index, coefs):
    h = x - xValues[index]
    y = 0

    for i in range(4):
        y += coefs[i][index] * (h ** i)

    return y

def finedIndex(xValues, x):
    size = len(xValues)
    index = 1

    while index < size and xValues[index] < x:
        index += 1

    return index - 1

def derivativeNewtonePolynom(pointTable, n, x):
    index = getIndex(pointTable, x)
    newPointTable = getWorkingPoints(pointTable, index, n + 1)
    newtoneTable = NewtoneTableCreate(newPointTable, n)

    derivative = 2 * newtoneTable[0][3] + newtoneTable[0][4] * (6 * x - 2 * (newPointTable[0].x + newPointTable[1].x + newPointTable[2].x))

    return derivative

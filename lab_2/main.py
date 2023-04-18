import spline as sp
from scipy import interpolate
import matplotlib.pyplot as plt
from numpy import arange
from NewtonePolynom import *
import matplotlib as mpl

def print_menu():
    print("\n\t\t===menu==="
          "\n1. count approximate"
          "\n2. print graphs"
          "\n0. quit")

if __name__ == "__main__":
    print_menu()
    menu_step = -1
    while menu_step != 0:
        menu_step = int(input("Enter menu number: "))
        if menu_step == 1:
            pointTable = sp.read_table("./data/test_1.txt")
            sp.print_pointTable(pointTable)

            x = float(input("Enter x: "))
            n = 3

            # when x_0 and x_N == 0
            start1 = 0
            end1 = 0

            # when x_0 == P'' x_N == 0
            start2 = 0
            end2 = 0

            # when x_0 and x_N == P''
            start3 = 0
            end3 = 0

            if len(pointTable) > n:
                start2 = sp.derivativeNewtonePolynom(pointTable, n, pointTable[0].x)
                start3 = sp.derivativeNewtonePolynom(pointTable, n, pointTable[0].x)
                end3 = sp.derivativeNewtonePolynom(pointTable, n, pointTable[-1].x)

            else:
                print("невозможо вычислить полином Ньютона для данной таблицы")



            print("Cплайн 0 and 0:          {:>10}".format(sp.spline(pointTable, x, start1, end1)))
            print("Cплайн P'' and 0:        {:>10}".format(sp.spline(pointTable, x, start2, end2)))
            print("Cплайн P'' and P'':      {:>10}".format(sp.spline(pointTable, x, start3, end3)))

            x_s = [i.getX() for i in pointTable]
            y_s = [i.getY() for i in pointTable]
            tck = interpolate.splrep(x_s, y_s)

            print("Spline with sci py:      {:>10}".format(interpolate.splev(x, tck), 3))

            index = getIndex(pointTable, x)
            newPointTable = getWorkingPoints(pointTable, index, n + 1)
            newtoneTable = NewtoneTableCreate(newPointTable, n)

            print("Полином Ньютона:         {:>10}".format(NewtonePolyCount(newtoneTable, x)))

        if menu_step == 2:
            pointTable = sp.read_table("./data/test_1.txt")
            sp.print_pointTable(pointTable)

            n = 3
            # when x_0 and x_N == 0
            start1 = 0
            end1 = 0

            # when x_0 == P'' x_N == 0
            start2 = 0
            end2 = 0

            # when x_0 and x_N == P''
            start3 = 0
            end3 = 0

            if len(pointTable) > n:
                start2 = sp.derivativeNewtonePolynom(pointTable, n, pointTable[0].x)
                start3 = sp.derivativeNewtonePolynom(pointTable, n, pointTable[0].x)
                end3 = sp.derivativeNewtonePolynom(pointTable, n, pointTable[-1].x)

            else:
                print("невозможо вычислить полином Ньютона для данной таблицы")

            #x_s = [i for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.1)]
            x_s = []
            y_s = []
            y_sss = []

            for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.01):
                x_s.append(i)
                y_s.append(sp.spline(pointTable, i, start1, end1))

            fig, ax = plt.subplots()
            ax.plot(x_s, y_s, color='green')

            y_s.clear()

            for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.01):
                y_s.append(sp.spline(pointTable, i, start2, end2))

            ax.plot(x_s, y_s, color='red')

            y_s.clear()
            for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.01):
                y_s.append(sp.spline(pointTable, i, start3, end3))

            ax.plot(x_s, y_s, color='blue')

            x_ss = [i.getX() for i in pointTable]
            y_ss = [i.getY() for i in pointTable]
            tck = interpolate.splrep(x_ss, y_ss)

            for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.01):
                y_sss.append(interpolate.splev(i, tck))

            y_s.clear()
            pointTable.sort(key=lambda point: point.x)
            for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.01):
                index = getIndex(pointTable, i)
                newPointTable = getWorkingPoints(pointTable, index, n + 1)
                newtoneTable = NewtoneTableCreate(newPointTable, n)
                y_s.append(NewtonePolyCount(newtoneTable, i))

            ax.plot(x_s, y_s, ':', color='purple')

            ax.plot(x_s, y_sss, color='black')
            plt.legend()
            plt.show()




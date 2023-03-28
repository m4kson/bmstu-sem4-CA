import spline as sp
from scipy import interpolate
import matplotlib.pyplot as plt
from numpy import arange

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
            start1 = 0
            end1 = 0
            print("Cплайн 0 and 0:             ", sp.spline(pointTable, x, start1, end1))

            x_s = [i.getX() for i in pointTable]
            y_s = [i.getY() for i in pointTable]
            tck = interpolate.splrep(x_s, y_s)

            print("Spline with scipy:             ", interpolate.splev(x, tck))

        if menu_step == 2:
            pointTable = sp.read_table("./data/test_1.txt")
            sp.print_pointTable(pointTable)

            #x_s = [i for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.1)]
            x_s = []
            y_s = []
            y_sss = []

            for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.1):
                x_s.append(i)
                y_s.append(sp.spline(pointTable, i, 0, 0))

            x_ss = [i.getX() for i in pointTable]
            y_ss = [i.getY() for i in pointTable]
            tck = interpolate.splrep(x_ss, y_ss)

            for i in arange(pointTable[0].getX(), pointTable[len(pointTable) - 1].getX(), 0.1):
                y_sss.append(interpolate.splev(i, tck))


            fig, ax = plt.subplots()
            ax.plot(x_s, y_s)


            ax.plot(x_s, y_sss)
            plt.show()




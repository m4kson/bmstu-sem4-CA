from Point_class import Point
from file_funcs import readTable, printTable
from polynom import *

def print_menu():
    print("\n\t\t===menu===")
    print("1. Проверить работу алгоритмов")
    print("2. Сравнить полиномы Ньютона и Эрмита при разных степенях для x = 0.675")
    print("3. Найти корень заданной табличной функции")
    print("4. Решить систему нелинейных уравнений, основываясь на идее обратной интерполяции")
    print("0. exit")

if __name__ == '__main__':

    menu_step = -1

    while menu_step != 0:
        print_menu()
        menu_step = int(input("Введите пункт меню: "))

        if menu_step == 1:
            table = readTable('./data/data.txt')
            table.sort(key=lambda point: point.x)
            printTable(table)

            x = float(input("Введите x: "))
            n = int(input("Введите n: "))

            index = getIndex(table, x)
            newPointTable = getWorkingPoints(table, index, n + 1)
            print("Рабочие точки")
            printTable(newPointTable)

            newtoneTable = NewtoneTableCreate(newPointTable, n)
            #print_newtoneTable(newtoneTable)
            print("Ньютон")
            printSubTable(newtoneTable)

            NewtonePoly = NewtonePolyCount(newtoneTable, x)

            hermitTable = HermitTableCreate(newPointTable, n)
            #print_newtoneTable(hermitTable)
            print("Эрмит")
            printSubTable(hermitTable)

            HermitPoly = HermitPolyCount(hermitTable, (n + 1) * 2 - 1, x)

            print("Newton: y({:}) = {}".format(x, NewtonePoly))
            print("Hermit: y({:}) = {}".format(x, HermitPoly))

        if menu_step == 2:
            table = readTable('./data/data.txt')
            table.sort(key=lambda point: point.x)
            printTable(table)

            x = 0.675

            print("┌───────┬──────────────┬──────────────┐")
            print("│ {:^5s} │ {:^12s} │ {:^12s} │".format("n", "Newton", "Hermit"))
            print("├───────┼──────────────┼──────────────┤")

            for n in range(1, 6):
                index = getIndex(table, x)
                newPointTable = getWorkingPoints(table, index, n + 1)

                newtoneTable = NewtoneTableCreate(newPointTable, n)
                NewtonePoly = NewtonePolyCount(newtoneTable, x)

                hermitTable = HermitTableCreate(newPointTable, n)
                HermitPoly = HermitPolyCount(hermitTable, (n + 1) * 2 - 1, x)

                print("│ {:^5d} │ {:^3.10f} │ {:^3.10f} │".format(n, NewtonePoly, HermitPoly))

            print("└───────┴──────────────┴──────────────┘")

        if menu_step == 3:
            table = readTable('./data/data.txt')
            printTable(table)
            n = int(input("enter n: "))
            print("root Newton: {}".format(rootNewton(table, n)))
            print("root Hermit: {}".format(rootHermit(table, n)))

        if menu_step == 4:
            find_system_root()




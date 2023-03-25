import spline as sp

def print_menu():
    print("\n\t\t===menu==="
          "\n1. print hello")

if __name__ == "__main__":
    print_menu()
    menu_step = -1
    while menu_step != 0:
        menu_step = int(input("Enter menu number: "))
        if menu_step == 1:
            pointTable = sp.read_table("./data/test_2.txt")
            sp.print_pointTable(pointTable)
            x = float(input("Enter x: "))
            start1 = 0
            end1 = 0
            print("Cплайн 0 and 0:             ", sp.spline(pointTable, x, start1, end1))



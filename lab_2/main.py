def print_menu():
    print("\n\t\t===menu==="
          "\n1. print hello")

if __name__ == "__main__":
    print_menu()
    menu_step = -1
    while menu_step != 0:
        menu_step = int(input("Enter: "))
        if menu_step == 1:
            print("hello")
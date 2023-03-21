from point_class import Point

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


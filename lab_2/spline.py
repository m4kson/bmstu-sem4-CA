from point_class import Point

def read_table(filename):
    file = open(filename, "r")
    if file == None:
        return -1

    table = []
    for line in file:
        line = line.split()
        table.append(Point(line[0], line[1]))

    return table

def print_pointTable(table):

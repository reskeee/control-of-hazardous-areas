from sympy import Point, Polygon


def get_coords(filename):
    with open(filename, encoding='utf-8', mode='rt') as coords:
        coords = coords.read()
        polys = list(map(lambda x: x.replace('\n', '').split(', '), coords.split(';')))
        polys = list(map(lambda x: list(map(lambda y: y.replace('(', '').replace(')', ''), x)), polys))
        polys = list(map(lambda x: list(map(lambda y: tuple(map(int, y.split(' : '))), x)), polys))
        return polys


def create_dots_array(A: tuple, B: tuple, C: tuple, D: tuple):
    X_min = min(A[0], B[0], C[0], D[0])
    X_max = max(A[0], B[0], C[0], D[0])
    Y_min = min(A[1], B[1], C[1], D[1])
    Y_max = max(A[1], B[1], C[1], D[1])

    rect = Polygon(A, B, C, D)

    points = []

    for x in range(X_min, X_max + 1):
        for y in range(Y_min, Y_max + 1):
            if rect.encloses_point(Point(x, y)):
                points.append([x, y])
    return points


A = (0, 100)
B = (100, 100)
C = (0, 0)
D = (100, 0)

print(get_coords('poly_vertex'))
# print(create_dots_array(A, B, C, D))

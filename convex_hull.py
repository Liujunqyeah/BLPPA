import sys
import math
import time
import random
import matplotlib.pyplot as plt
from geopy import distance


def get_LeftBottomPoint(points):
    k = 0
    for i in range(1, len(points)):
        if points[i][1] < points[k][1] or (points[i][1] == points[k][1] and points[i][0] < points[k][0]):
            k = i
    return k


def multiply(p1, p2, p0):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


def get_arctan(point_base, point):
    if (point[0] - point_base[0]) == 0:
        if point[1] - point_base[1] == 0:
            return -1
        else:
            return math.pi / 2
    tan = float((point[1] - point_base[1])) / float((point[0] - point_base[0]))
    arctan = math.atan(tan)
    if arctan >= 0:
        return arctan
    else:
        return math.pi + arctan


def sort_points_tan(points, point_base):
    p2 = []
    for i in range(0, len(points)):
        p2.append({"index": i, "arctan": get_arctan(point_base, points[i])})
    p2.sort(key=lambda k: (k.get('arctan')))
    p_out = []
    for i in range(0, len(p2)):
        p_out.append(points[p2[i]["index"]])
    return p_out


def get_convex_hull_points(points):
    points = list(set(points))
    base_index = get_LeftBottomPoint(points)
    point_base = points[base_index]
    points.remove(points[base_index])
    point_sort = sort_points_tan(points, point_base)
    point_result = [point_base, point_sort[0]]

    top = 2
    for i in range(1, len(point_sort)):
        while multiply(point_result[-2], point_sort[i], point_result[-1]) > 0:
            point_result.pop()
        point_result.append(point_sort[i])
    return point_result


def get_triangle_area(points):
    a = math.sqrt((points[1][0] - points[2][0]) * (points[1][0] - points[2][0])
                  + (points[1][1] - points[2][1]) * (points[1][1] - points[2][1]))
    b = math.sqrt((points[0][0] - points[2][0]) * (points[0][0] - points[2][0])
                  + (points[0][1] - points[2][1]) * (points[0][1] - points[2][1]))
    c = math.sqrt((points[0][0] - points[1][0]) * (points[0][0] - points[1][0])
                  + (points[0][1] - points[1][1]) * (points[0][1] - points[1][1]))
    s = (a + b + c) / 2.0
    S = ((s * (s - a) * (s - b) * (s - c)) ** 0.5) * (111000 ** 2)
    return S
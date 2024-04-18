import datetime
import math

from matplotlib import pyplot as plt

from balance.convex_hull import get_convex_hull_points, get_triangle_area


def distance_p2p(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def twoCircleIntersectPoints(p1, p2, radius):
    d = distance_p2p(p1, p2)
    r1 = radius
    r2 = radius
    if (d >= (r1 + r2)) or (d <= abs(r1 - r2)):
        return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    x0 = p1[0] + a * (p2[0] - p1[0]) / d
    y0 = p1[1] + a * (p2[1] - p1[1]) / d
    rx = -(p2[1] - p1[1]) * (h / d)
    ry = -(p2[0] - p1[0]) * (h / d)
    return [{0: x0 + rx, 1: y0 - ry}, {0: x0 - rx, 1: y0 + ry}]
    # return [(x0 + rx, y0 - ry), (x0 - rx, y0 + ry)]


def getIntersectionPoints(circles, radius):
    ret = []
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            intersect = twoCircleIntersectPoints(circles[i], circles[j], radius)
            for k in range(len(intersect)):
                p = intersect[k]
                ret.append(p)
    return ret


def containedInCircles(point, circles, radius):
    SMALL = 1e-10
    for i in range(len(circles)):
        if distance_p2p(point, circles[i]) > radius + SMALL:
            return False
    return True


def get_sorted_convex_hull_points(circles, radius):
    points = getIntersectionPoints(circles, radius)
    list_one_sub = []
    for point in points:
        if containedInCircles(point, circles, radius):
            list_one_sub.append((point[0], point[1]))
    convex_hull_points = get_convex_hull_points(list_one_sub)
    return convex_hull_points


def get_convexHull_area(circles, radius):
    convex_hull_points = get_sorted_convex_hull_points(circles, radius)
    area_convex_hull = 0
    for len_c_h_p in range(1, len(convex_hull_points) - 1):
        lists = [convex_hull_points[0], convex_hull_points[len_c_h_p], convex_hull_points[len_c_h_p + 1]]
        area_convex_hull = area_convex_hull + get_triangle_area(lists)
    return area_convex_hull


def get_intersection_area(circles, radius):
    convex_hull_points = get_sorted_convex_hull_points(circles, radius)
    arch_area = get_arch_area(convex_hull_points, radius)
    convexHull_area = get_convexHull_area(circles, radius)
    return convexHull_area + arch_area


def get_arch_area(points, radius):
    arch_area = 0
    list_points = []
    for i in range(len(points) - 1):
        list_points.append([points[i], points[i + 1]])
    list_points.append([points[0], points[len(points) - 1]])
    for twoPoint in list_points:
        d = math.sqrt((twoPoint[0][0] - twoPoint[1][0]) ** 2
                      + (twoPoint[0][1] - twoPoint[1][1]) ** 2)
        angle_theta = math.asin(d / (2 * radius))
        sector_area = (radius ** 2) * angle_theta
        triangle_area = math.sqrt(radius ** 2 - (d / 2) ** 2) * d / 2
        arch_area = arch_area + (sector_area - triangle_area) * (111000 ** 2)
    return arch_area


def get_max_intersection_area(list_all_hub, radius):
    temp = 0
    temp_list = []
    for circles in list_all_hub:
        convex_hull_points = get_sorted_convex_hull_points(circles, radius)
        arch_area = get_arch_area(convex_hull_points, radius)
        area_convex_hull = 0
        for len_c_h_p in range(1, len(convex_hull_points) - 1):
            lists = [convex_hull_points[0], convex_hull_points[len_c_h_p], convex_hull_points[len_c_h_p + 1]]
            area_convex_hull = area_convex_hull + get_triangle_area(lists)
        area_convex_hull = area_convex_hull
        intersection_area = area_convex_hull + arch_area
        if intersection_area > temp:
            temp = intersection_area
            temp_list = circles
    return [temp, temp_list]


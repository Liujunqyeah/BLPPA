# -*- coding:utf-8 -*-
from datetime import datetime
import random
import numpy as np
from matplotlib import pyplot as plt
from balance.circleIntersection import get_intersection_area, get_max_intersection_area
from balance.convex_hull import get_convex_hull_points, get_triangle_area
from commonFiles.normalFunctions import get_dis_point2point, get_sub_list_all


def get_max_convexHull_area(list_sub):
    temp = 0
    temp_list = []
    for list_one_sub in list_sub:
        convex_hull_points = get_convex_hull_points(list_one_sub)
        area_convex_hull = 0
        for len_c_h_p in range(1, len(convex_hull_points) - 1):
            lists = [convex_hull_points[0], convex_hull_points[len_c_h_p], convex_hull_points[len_c_h_p + 1]]
            area_convex_hull = area_convex_hull + get_triangle_area(lists)
        area_convex_hull = area_convex_hull
        if area_convex_hull > temp:
            temp = area_convex_hull
            temp_list = list_one_sub
    return [temp, temp_list]


def get_min_average_distance(x_center, y_center, list_half_sub, k):
    temp = 100000
    temp_list = []
    for list_one_sub in list_half_sub:
        sum = 0
        for num_sub in list_one_sub:
            sum += get_dis_point2point(x_center, y_center, num_sub[0], num_sub[1])
        average = sum / len(list_one_sub) * 111000
        if average < temp:
            temp = average
            temp_list = list_one_sub
    return [temp, temp_list]


def get_average_distance(x_center, y_center, list_one_sub):
    sum = 0
    for num_sub in list_one_sub:
        sum += get_dis_point2point(x_center, y_center, num_sub[0], num_sub[1])
    return sum / len(list_one_sub) * 111000


def get_convexHull_area(list_one_sub):
    convex_hull_points = get_convex_hull_points(list_one_sub)
    area_convex_hull = 0
    for index in range(1, len(convex_hull_points) - 1):
        lists = [convex_hull_points[0], convex_hull_points[index], convex_hull_points[index + 1]]
        area_convex_hull = area_convex_hull + get_triangle_area(lists)
    return area_convex_hull


def supply_points(x_center, y_center, radius, total):
    count = 0
    x = np.zeros(total)
    y = np.zeros(total)
    while count < total:
        theta = np.random.random() * 2 * np.pi
        r = np.random.random() ** 0.5 * radius
        x[count] = x_center + r * np.cos(theta)
        y[count] = y_center + r * np.sin(theta)
        count += 1
    array = [x, y]
    return array


def anonymous_area(x, y, radius, color, lineWidth):
    _t = np.arange(0, 7, 0.1)
    _x = x + np.cos(_t) * radius
    _y = y + np.sin(_t) * radius
    plt.plot(_x, _y, color, linewidth=lineWidth)


def List(nodeID, List_without_InitNewNodes):
    cooperateAllList = findCooperateUserByID(nodeID)
    cooperateNodesMap = cooperateAllList["cooperateNodes"]
    list_reqUNodeOther = []
    for reqUNodes in List_without_InitNewNodes:
        if reqUNodes.ID in cooperateNodesMap:
            list_reqUNodeOther.append(reqUNodes.ID)
    return list_reqUNodeOther


def circle(k):
    n = 1

    plt.figure(figsize=(10, 8.5), dpi=150)

    find_results = findCooperateUsersConditional()
    total = findCooperateUsersConditionalCount()

    requestUser = [RequestUser("", 0, 0, 0, 0, 0, 0, []) for _ in range(n)]
    requestUser_true = [RequestUser("", 0, 0, 0, 0, 0, 0, []) for _ in range(n)]
    requestUser_CList = [RequestUser("", 0, 0, 0, 0, 0, 0, []) for _ in range(n)]
    cooperateUsers = [CooperateUser("", 0, 0, 0, 0, 0, {}) for _ in range(total)]

    point_x = []
    point_y = []
    w = 0
    for result in find_results:
        point_x.append(result["x"])
        point_y.append(result["y"])
        cooperateUsers[w].ID = result["ID"]
        cooperateUsers[w].x = result["x"]
        cooperateUsers[w].y = result["y"]
        cooperateUsers[w].trustValue = result["trustValue"]
        cooperateUsers[w].recommendedReliability = result["recommendedReliability"]
        plt.plot(cooperateUsers[w].x, cooperateUsers[w].y, 'y.')
        w = w + 1

    for i in range(n):
        list_temp = []

        requestUser[i].x = 116.3065
        requestUser[i].y = 39.9805

        requestUser[i].radius = 0.00225
        requestUser_true[i].cooperateList = [CooperateUser("", 0, 0, 0, 0, 0, {}) for _ in range(k)]

        plt.plot(requestUser[i].x, requestUser[i].y, '*m')
        anonymous_area(requestUser[i].x, requestUser[i].y, requestUser[i].radius, ":g", 2)

        rand_center = random.uniform(-requestUser[i].radius / 2, requestUser[i].radius / 2)
        x_center_true = requestUser[i].x
        y_center_true = requestUser[i].y
        requestUser_true[i].x = x_center_true
        requestUser_true[i].y = y_center_true
        requestUser_true[i].radius = requestUser[i].radius

        requestUser_CList[i].x = x_center_true
        requestUser_CList[i].y = y_center_true
        requestUser_CList[i].radius = requestUser[i].radius
        requestUser_CList[i].cooperateList = []

        for j in range(total):
            distance = get_dis_point2point(cooperateUsers[j].x, cooperateUsers[j].y, requestUser[i].x,
                                           requestUser[i].y)
            if distance <= requestUser_true[i].radius:
                list_temp.append(cooperateUsers[j])

        requestUser_true[i].cooperateList = random.sample(list_temp, k)
        for user in requestUser_true[i].cooperateList:
            plt.plot(user.x, user.y, "b.")

        requestUser_CList[i] = requestUser_true[i]

        dis = requestUser[i].radius

        list_honestUsers = []
        for honestUsers in requestUser_CList[i].cooperateList:
            tup = (honestUsers.x, honestUsers.y)
            list_honestUsers.append(tup)

        list_all_sub_honestUser = get_sub_list_all(list_honestUsers)  # length=1023

        list_all_sub = []
        for sub_ in list_all_sub_honestUser:
            if len(sub_) > 2:
                list_all_sub.append(sub_)

        MAX_intersection_area = get_max_intersection_area(list_all_sub, dis)[0]
        MAX_average_dist = get_min_average_distance(requestUser[i].x, requestUser[i].y, list_all_sub, k)[0]
        MAX_convexHull_area = get_max_convexHull_area(list_all_sub)[0]

        # BLPPA-AIP
        temp_ppawa = 0
        temp_users = []
        temp_intersection_area = 0
        temp_average_dist = 0
        temp_convexHull_area = 0
        maxPPAWA_startTime = datetime.now()
        for item_sub in list_all_sub:
            intersection_area = get_intersection_area(item_sub, dis)
            average_dist = get_average_distance(requestUser[i].x, requestUser[i].y, item_sub)
            convexHull_area = get_convexHull_area(item_sub)
            ppawa = (
                              intersection_area / MAX_intersection_area + MAX_average_dist / average_dist + convexHull_area / MAX_convexHull_area) / 3
            if ppawa > temp_ppawa:
                temp_users = item_sub
                temp_ppawa = ppawa
                temp_intersection_area = intersection_area
                temp_average_dist = average_dist
                temp_convexHull_area = convexHull_area

        maxPPAWA_endTime = datetime.now()

        # APA
        minD_startTime = datetime.now()
        D_result = get_min_average_distance(requestUser[i].x, requestUser[i].y, list_all_sub, k)
        maxAED_average_dist = D_result[0]
        list_max_average_dist = D_result[1]
        maxAED_intersection_area = get_intersection_area(list_max_average_dist, dis)
        maxAED_convexHull_area = get_convexHull_area(list_max_average_dist)
        PPAWA_AED = (maxAED_intersection_area / MAX_intersection_area + MAX_average_dist / maxAED_average_dist +
                   maxAED_convexHull_area / MAX_convexHull_area) / 3
        minD_endTime = datetime.now()

        # IPA
        maxIA_startTime = datetime.now()
        IA_result = get_max_intersection_area(list_all_sub, dis)
        maxIA_intersection_area = IA_result[0]
        list_max_intersection_area = IA_result[1]
        maxIA_average_dist = get_average_distance(requestUser[i].x, requestUser[i].y, list_max_intersection_area)
        maxIA_convexHull_area = get_convexHull_area(list_max_intersection_area)
        PPAWA_IA = (maxIA_intersection_area / MAX_intersection_area + MAX_average_dist / maxIA_average_dist +
                  maxIA_convexHull_area / MAX_convexHull_area) / 3

        maxIA_endTime = datetime.now()

        # PA
        maxCHA_startTime = datetime.now()
        CHA_result = get_max_convexHull_area(list_all_sub)
        maxCHA_convexHull_area = CHA_result[0]
        list_max_convexHull_area = CHA_result[1]
        maxCHA_intersection_area = get_intersection_area(list_max_convexHull_area, dis)
        maxCHA_average_dist = get_average_distance(requestUser[i].x, requestUser[i].y, list_max_convexHull_area)
        PPAWA_CHA = (maxCHA_intersection_area / MAX_intersection_area + MAX_average_dist / maxCHA_average_dist +
                   maxCHA_convexHull_area / MAX_convexHull_area) / 3
        maxCHA_endTime = datetime.now()

        # GREEDY
        greedy_startTime = datetime.now()
        list_max_sub = list_all_sub[len(list_all_sub) - 1]
        maxSub_intersection_area = get_intersection_area(list_max_sub, dis)
        maxSub_average_dist = get_average_distance(requestUser[i].x, requestUser[i].y, list_max_sub)
        maxSub_convexHull_area = get_convexHull_area(list_max_sub)
        PPAWA_greedy = (maxSub_intersection_area / MAX_intersection_area + MAX_average_dist / maxSub_average_dist +
                      maxSub_convexHull_area / MAX_convexHull_area) / 3
        greedy_endTime = datetime.now()

        # RANDOM
        random_startTime = datetime.now()
        randomNumber = random.randint(0, len(list_all_sub) - 1)
        list_rand_sub = list_all_sub[randomNumber]
        randSub_intersection_area = get_intersection_area(list_rand_sub, dis)
        randSub_average_dist = get_average_distance(requestUser[i].x, requestUser[i].y, list_rand_sub)
        randSub_convexHull_area = get_convexHull_area(list_rand_sub)
        PPAWA_random = (randSub_intersection_area / MAX_intersection_area + MAX_average_dist / randSub_average_dist +
                      randSub_convexHull_area / MAX_convexHull_area) / 3
        random_endTime = datetime.now()

        print("BLPPA-AIP:", maxPPAWA_endTime - maxPPAWA_startTime)
        print("APA:", minD_endTime - minD_startTime)
        print("IPA:", maxIA_endTime - maxIA_startTime)
        print("PA:", maxCHA_endTime - maxCHA_startTime)
        print("GREEDY:", greedy_endTime - greedy_startTime)
        print("RANDOM:", random_endTime - random_startTime)

        print("*************************************************************")
        print("BLPPA-AIP:    \t%.4f, %.4f, %.4f, %.4f" % (
        temp_ppawa, temp_average_dist, temp_intersection_area, temp_convexHull_area))
        print("APA:     \t%.4f, %.4f, %.4f, %.4f" % (
        PPAWA_AED, MAX_average_dist, maxAED_intersection_area, maxAED_convexHull_area))
        print("IPA:     \t%.4f, %.4f, %.4f, %.4f" % (
        PPAWA_IA, maxIA_average_dist, MAX_intersection_area, maxIA_convexHull_area))
        print("PA:      \t%.4f, %.4f, %.4f, %.4f" % (
        PPAWA_CHA, maxCHA_average_dist, maxCHA_intersection_area, MAX_convexHull_area))
        print("GREEDY:  \t%.4f, %.4f, %.4f, %.4f" % (
        PPAWA_greedy, maxSub_average_dist, maxSub_intersection_area, maxSub_convexHull_area))
        print("RANDOM:  \t%.4f, %.4f, %.4f, %.4f" % (
        PPAWA_random, randSub_average_dist, randSub_intersection_area, randSub_convexHull_area))
        print("\n")
        for user in temp_users:
            plt.plot(user[0], user[1], linestyle=' ', marker='*', color="c")
            anonymous_area(user[0], user[1], dis, ":c", 1)

    plt.title('')
    plt.tick_params(labelsize=15)
    plt.xlabel("Longitude", fontdict={'weight': 'normal', 'size': 16})
    plt.ylabel("Latitude", fontdict={'weight': 'normal', 'size': 16})
    plt.show()


def single():
    circle(10)


if __name__ == '__main__':
    single()

#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""
import math
import random
import time
import pickle


def SA(facilityCount, customorCount, capacity, openCost, assignCost, demand,
       init_temperature=100, factor=0.999, stop_temperature=10):
    """
    模拟退火实现
    :param facilityCount:int
    :param customorCount:int
    :param capacity:[int]
    :param openCost:[int]
    :param assignCost:[[int]]
    :param demand:[int]
    :param init_temperature:int
    :param factor:float
    :param stop_temperature:int
    :return:
    """

    def assignInit():
        """
        初始化解
        :return:
        """
        assign = [facilityCount] * customorCount

        leaveCapacity = capacity.copy()
        order = list(range(customorCount))
        try:
            random.shuffle(order)
        except RecursionError as e:
            # print(order)
            raise (e)
        for customor in order:
            bestSuit = facilityCount
            minLeave = 5000000
            for fac in range(facilityCount):
                leave = leaveCapacity[fac]
                if leave >= demand[customor] and leave < minLeave:
                    bestSuit = fac
                    minLeave = leave
            if bestSuit == facilityCount:
                # 不能放下,另起炉灶
                return assignInit()
            assign[customor] = bestSuit
            leaveCapacity[bestSuit] -= demand[customor]
        return assign

    def cost(assign: [int]):
        """
        fitness function
        :param assign:
        :return:
        """
        isOpen = [False] * facilityCount
        for i in range(customorCount):
            isOpen[assign[i]] = True

        _cost = 0
        for i in range(customorCount):
            _cost += assignCost[i][assign[i]]
        for i in range(facilityCount):
            if isOpen[i]:
                _cost += openCost[i]
        return _cost

    def assignNeighbor(assign: [float]):
        """
        局部搜索
        :param assign:
        :return:
        """
        # 工厂被分配的用户数
        facilities = [0] * facilityCount

        for i in range(customorCount):
            facilities[assign[i]] += 1

        res = assign.copy()

        for i in range(customorCount):
            if random.random() < 2 / facilities[assign[i]]:
                res[i] = random.randint(0, facilityCount - 1)

        return res

    def assignRepair(assign: [float]):
        """
        修复不可行解
        :param assign:
        :return:
        """
        # 工厂的负载
        load = [0] * facilityCount
        # 被分配到某工厂的用户
        assigned = [[] for _ in range(facilityCount)]
        # 超载的工厂序号
        overload = set()
        for c in range(customorCount):
            fac = assign[c]
            assigned[fac].append(c)
            load[fac] += demand[c]
            if load[fac] > capacity[fac]:
                # 过载
                overload.add(fac)
        while (len(overload) != 0):
            facility = random.sample(overload, 1)[0]
            customor = random.choice(assigned[facility])
            # 移出
            assert (assign[customor] == facility)
            oldFac = assign[customor]
            assigned[oldFac].remove(customor)
            load[oldFac] -= demand[customor]
            if load[oldFac] <= capacity[oldFac]:
                overload.remove(oldFac)

            # 重新分配
            newFac = random.randint(0, facilityCount - 1)
            assigned[newFac].append(customor)
            load[newFac] += demand[customor]
            if load[newFac] > capacity[newFac]:
                overload.add(newFac)
            assign[customor] = newFac

        return assign

    start_time = time.time()
    T = init_temperature
    assign = assignInit()
    argmin = assign
    value = cost(argmin)

    record = []

    while (T > stop_temperature):
        for _ in range(facilityCount ** 2):
            neigh = assignNeighbor(assign)
            neigh = assignRepair(neigh)
            newValue = cost(neigh)
            if newValue < value:
                value = newValue
                assign = neigh
            elif (math.exp(-(newValue - value) / T) >= random.random()):
                assign = neigh
        T *= factor
        record.append(value)

    def recordResult(record):
        # print('正在写入数据')
        fileName = '.drawData'
        result = None
        with open(fileName, 'r+b') as f:
            try:
                result = pickle.load(f)
            except EOFError:
                result = []
            result.append(record)
            f.seek(0, 0)
            f.truncate()
            pickle.dump(result, f)
        # print('写入完成')

    # recordResult({
    #     'type': 'SA',
    #     'date': time.time(),
    #     'changeProp': changeProp,
    #     'init_temperature': init_temperature,
    #     'factor': factor,
    #     'stop_temperature': stop_temperature,
    #     'x-axis': [i for i in range(len(record))],
    #     'y-axis': record,
    # })

    """
    写数据
    """
    end_time = time.time()
    isOpen = [0] * facilityCount
    for i in range(customorCount):
        isOpen[argmin[i]] = 1

    result = {
        "algorithm": "simulated_annealing",
        "input": {
            "facilityCount": facilityCount,
            "customorCount": customorCount,
            "capacity": capacity,
            "openCost": openCost,
            "assignCost": assignCost,
            "demand": demand,
        },
        "output": {
            "objVal": value,
            "isOpen": isOpen,
            "assignment": argmin
        },
        "excutTime": end_time - start_time
    }
    return result

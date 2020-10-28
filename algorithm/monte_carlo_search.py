#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""
import time
import random
import decorator


@decorator.logPrint
def MCS(facilityCount, customorCount, capacity, openCost, assignCost, demand, times=10000):
    """
    蒙特卡洛搜索
    :param facilityCount:
    :param customorCount:
    :param capacity:
    :param openCost:
    :param assignCost:
    :param demand:
    :param times:
    :return:
    """

    def produce_randan_solution():
        factory_open = [0] * facilityCount
        customer_assign = []
        total_openCost = 0
        total_assignCost = 0
        demand_customer_copy = demand.copy()
        capacity_copy = capacity.copy()

        for i in range(customorCount):
            # 判断是否继续为此工厂挑选随机解
            flag = True
            fac_num = -1
            while (flag):
                # 生成随机数
                fac_num = random.randint(0, facilityCount - 1)

                # 如果容量符合要求则选择该工厂
                if (demand_customer_copy[i] <= capacity_copy[fac_num]):
                    # 如果工厂没开 则开工厂
                    if (factory_open[fac_num] == 0):
                        factory_open[fac_num] = 1
                        total_openCost += openCost[fac_num]
                    # 写入到安排计划数组里
                    customer_assign.append(fac_num)
                    # 减去相应容量
                    capacity_copy[fac_num] -= demand_customer_copy[i]
                    # 更新总共total_assignCost
                    total_assignCost += assignCost[i][fac_num]
                    # 更新flag
                    flag = False
        return total_openCost + total_assignCost, factory_open, customer_assign

    start_time = time.time()
    bestValue = 2 ** 31 - 1
    bestFactoryOpen = []
    bestValueAssign = []
    for i in range(times):

        tmp = produce_randan_solution()

        if (tmp[0] < bestValue):
            bestValue = tmp[0]
            bestFactoryOpen = tmp[1]
            bestValueAssign = tmp[2]

    end_time = time.time()
    result = {
        "algorithm": "monte_carlo",
        "input": {
            "facilityCount": facilityCount,
            "customorCount": customorCount,
            "capacity": capacity,
            "openCost": openCost,
            "assignCost": assignCost,
            "demand": demand,
            "times": times
        },
        "output": {
            "objVal": bestValue,
            "isOpen": bestFactoryOpen,
            "assignment": bestValueAssign
        },
        "excutTime": end_time - start_time
    }
    return result

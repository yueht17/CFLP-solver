#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""
import time
import random


def LS(facilityCount, customorCount, capacity, openCost, assignCost, demand):
    """
    先用贪心的策略生成一个可行解然后局部搜索
    :param facilityCount:
    :param customorCount:
    :param capacity:
    :param openCost:
    :param assignCost:
    :param demand:
    :return:
    """

    def get_assign_rank(assign):
        """
        顾客到工厂的cost 由小到大进行排序
        :param assign:
        :return:
        """
        rank_array = []

        for item in assignCost:

            # for x in range(n):
            #     item[x] = item[x] + openCost[x]

            tmp = sorted(item)
            addArr = []

            for i in range(facilityCount):
                addArr.append(tmp.index(item[i]))

            rank_array.append(addArr)

        return rank_array

    def greedSingle():
        """
        应用贪心的策略生成一个可行解
        :return:
        """
        customer_assign = []
        # 此解的 工厂开放费用和客户安排费用
        total_assign_cost = 0
        total_open_cost = 0

        # 获取 每个客户的 对于每个工厂的排名矩阵
        # 每一行对应第i个矩阵
        # 没一列对于此工厂的在所有工厂的assign费用排名  优先选最小
        assignment_cost_rank = get_assign_rank(customer_assign)

        open_flag = []
        # 初始化 工厂开放情况
        for x in range(facilityCount):
            open_flag.append(0)
        #
        for i in range(customorCount):
            # 对于每一个用户
            for j in range(facilityCount):
                # 找到当前 想要加入的工厂的下标
                try:
                    # 从排名为0 的工厂开始 把此工厂定义为 此用户要被安排进的工厂
                    fac_num = assignment_cost_rank[i].index(j)
                except:
                    fac_num = assignment_cost_rank[i].index(j + 1)
                # 如果此工厂能装得下
                if demand[i] < capacity[fac_num]:

                    if open_flag[fac_num] == 0:
                        open_flag[fac_num] = 1
                        total_open_cost += openCost[fac_num]

                    # 则表示将当前用户安排给自工厂， 更新相应数据
                    customer_assign.append(fac_num)
                    total_assign_cost += assignCost[i][j]
                    capacity[fac_num] = capacity[fac_num] - demand[i]
                    break
                else:
                    pass


        return total_open_cost + total_assign_cost, open_flag, customer_assign

    def produce_local_search_solution(bestFactoryOpen, bestValueAssign, capacity_copy):
        """
        局部搜索的主程序
        :param bestFactoryOpen:
        :param bestValueAssign:
        :param capacity_copy:
        :return:
        """
        flag = True
        fac_num = -1
        # 选择的随机顾客标号为i
        i = random.randint(0, customorCount - 1)

        while (flag):
            # 生成被安排的随机工厂
            fac_num = random.randint(0, facilityCount - 1)
            # 如果生成的随机工厂就是原来的工厂则继续生成
            if (fac_num == bestValueAssign[i]):
                continue

            # 如果容量符合要求则选择该工厂
            if (demand[i] <= capacity_copy[fac_num]):
                # 如果工厂没开 则开工厂
                if (bestFactoryOpen[fac_num] == 0):
                    bestFactoryOpen[fac_num] = 1

                # 给离开的工厂加上相应的容量
                capacity_copy[bestValueAssign[i]] += demand[i]
                # 同时减去相应的assign消耗

                # 如果离开的工厂的容量变为初始容量， 则把工厂设置为关闭
                if (capacity_copy[bestValueAssign[i]] == capacity[bestValueAssign[i]]):
                    bestFactoryOpen[bestValueAssign[i]] = 0

                # 更新安排表
                bestValueAssign[i] = fac_num
                # 减去相应容量
                capacity_copy[fac_num] -= demand[i]
                # 更新总共total_assignCost

                # 更新flag
                flag = False

            # 计算此解的cost 当做参数传出去
            bestCost = 0
            for s in range(customorCount):
                bestCost += assignCost[i][bestValueAssign[s]]

            for d in range(facilityCount):
                bestCost += bestFactoryOpen[d] * openCost[d]

        # return bestCost, bestFactoryOpen, bestValueAssign, capacity_copy
        return bestCost, bestFactoryOpen, bestValueAssign, capacity_copy

    start_time = time.time()
    tmp = greedSingle()
    bestCost = tmp[0]
    bestFactoryOpen = tmp[1]
    bestValueAssign = tmp[2]
    capacity_copy = capacity.copy()

    # 因为进行贪心算法之后 全局数据发送了污染 所以要重新读取数据

    for x in range(100000):
        # 生成局部新解
        tmp1 = produce_local_search_solution(bestFactoryOpen, bestValueAssign, capacity_copy)

        # 如果新解优于原先解 则进行更新

        if tmp1[0] < bestCost:
            bestCost = tmp1[0]
            bestFactoryOpen = tmp1[1]
            bestValueAssign = tmp1[2]
            capacity_copy = tmp1[3]

    end_time = time.time()
    result = {
        "algorithm": "local_search",
        "input": {
            "facilityCount": facilityCount,
            "customorCount": customorCount,
            "capacity": capacity,
            "openCost": openCost,
            "assignCost": assignCost,
            "demand": demand,
        },
        "output": {
            "objVal": bestCost,
            "isOpen": bestFactoryOpen,
            "assignment": bestValueAssign
        },
        "excutTime": end_time - start_time
    }
    return result

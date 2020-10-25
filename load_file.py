#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""


def loadFile(instancePath):
    """
    解析构造的问题实例
    :param instancePath:str
    :return:dict
    """
    with open(instancePath, 'r') as f:
        line = f.readline()
        facilityCount, customorCount = [int(p) for p in line.split()]
        capacity = [0] * facilityCount
        openCost = [0] * facilityCount
        for i in range(facilityCount):
            line = f.readline()
            capacity[i], openCost[i] = [float(p) for p in line.split()]
        # 处理空格和换行
        buffer = [float(p) for p in ''.join(f.readlines()).split() if p[0] != '\x00']
        assert (len(buffer) == facilityCount * customorCount + customorCount)

        # 客户需要
        demand = buffer[:customorCount]
        # 分配花费
        assignCost = [[0] * facilityCount for _ in range(customorCount)]
        for i in range(customorCount):
            assignCost[i] = buffer[ \
                            customorCount + i * facilityCount \
                            :customorCount + (i + 1) * facilityCount \
                            ]
    assert (len(assignCost) == customorCount)
    assert (len(assignCost[0]) == facilityCount)
    instance = {
        "facilityCount": facilityCount,
        "customorCount": customorCount,
        "capacity": capacity,
        "openCost": openCost,
        "assignCost": assignCost,
        "demand": demand
    }
    return instance

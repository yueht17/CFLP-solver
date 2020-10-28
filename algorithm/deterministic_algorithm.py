#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""

import time
from gurobipy import *
import decorator


@decorator.logPrint
def deterministic(facilityCount, customorCount, capacity, openCost, assignCost, demand):
    """
    调用Gurobi工具箱对此MIP问题进行确定性的算法
    :param facilityCount:int
    :param customorCount:int
    :param capacity:[int]
    :param openCost:[int]
    :param assignCost:[[int]]
    :param demand:[int]
    :return:None
    """
    start_time = time.time()

    # 确保输入参数的维度正确性
    assert facilityCount == capacity.__len__()
    assert customorCount == demand.__len__()

    # Range of plants and warehouses
    plants = range(len(capacity))
    warehouses = range(len(demand))

    # Model
    m = Model("facility")
    m.Params.LogToConsole = False

    # Plant open decision variables: open[p] == 1 if plant p is open.
    open = m.addVars(plants,
                     vtype=GRB.BINARY,
                     obj=openCost,
                     name="open")

    # Transportation decision variables: transport[w,p] captures the
    # optimal quantity to transport to warehouse w from plant p
    transport = m.addVars(warehouses, plants, obj=assignCost, name="trans")

    # The objective is to minimize the total fixed and variable costs
    m.modelSense = GRB.MINIMIZE

    # Production constraints
    # Note that the right-hand limit sets the production to zero if the plant
    # is closed
    m.addConstrs(
        (transport.sum('*', p) <= capacity[p] * open[p] for p in plants),
        "Capacity")

    # Demand constraints
    m.addConstrs(
        (transport.sum(w) == demand[w] for w in warehouses),
        "Demand")

    # ... and the preceding would be ...
    # for w in warehouses:
    #  m.addConstr(sum(transport[w][p] for p in plants) == demand[w], "Demand[%d]" % w)

    # Save model
    m.write('facilityPY.lp')

    # Guess at the starting point: close the plant with the highest fixed costs;
    # open all others

    # First, open all plants
    for p in plants:
        open[p].start = 1.0

    # Use barrier to solve root relaxation
    m.Params.method = 2

    # Solve
    m.optimize()

    # Print solution
    # print('\nTOTAL COSTS: %g' % m.objVal)
    # print('SOLUTION:')
    # for p in plants:
    #     if open[p].x > 0.99:
    #         print('Plant %s open' % p)
    #         for w in warehouses:
    #             if transport[w, p].x > 0:
    #                 print('  Transport %g units to warehouse %s' % \
    #                       (transport[w, p].x, w))
    #     else:
    #         print('Plant %s closed!' % p)

    """
    写数据
    """
    end_time = time.time()
    result = {
        "algorithm": "deterministic",
        "input": {
            "facilityCount": facilityCount,
            "customorCount": customorCount,
            "capacity": capacity,
            "openCost": openCost,
            "assignCost": assignCost,
            "demand": demand,
        },
        "output": {
            "objVal": m.objVal,
            "isOpen": [int(1) if open[_].x > 0.99 else 0 for _ in plants],
            # "assignment": [[transport[i, j].x for j in range(facilityCount)] for i in range(customorCount)]
        },
        "excutTime": end_time - start_time
    }

    return result

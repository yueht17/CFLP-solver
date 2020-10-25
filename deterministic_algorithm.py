#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""

from gurobipy import *


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

    # 确保输入参数的维度正确性
    assert facilityCount == capacity.__len__()
    assert customorCount == demand.__len__()

    # Range of plants and warehouses
    plants = range(len(capacity))
    warehouses = range(len(demand))

    # Model
    m = Model("facility")

    # Plant open decision variables: open[p] == 1 if plant p is open.
    open = m.addVars(plants,
                     vtype=GRB.BINARY,
                     obj=openCost,
                     name="open")

    # Transportation decision variables: transport[w,p] captures the
    # optimal quantity to transport to warehouse w from plant p
    transport = m.addVars(warehouses, plants, obj=assignCost, name="trans")

    # You could use Python looping constructs and m.addVar() to create
    # these decision variables instead.  The following would be equivalent
    # to the preceding two statements...
    #
    # open = []
    # for p in plants:
    #  open.append(m.addVar(vtype=GRB.BINARY,
    #                       obj=openCost[p],
    #                       name="open[%d]" % p))
    #
    # transport = []
    # for w in warehouses:
    #  transport.append([])
    #  for p in plants:
    #    transport[w].append(m.addVar(obj=assignCost[w][p],
    #                                 name="trans[%d,%d]" % (w, p)))

    # The objective is to minimize the total fixed and variable costs
    m.modelSense = GRB.MINIMIZE

    # Production constraints
    # Note that the right-hand limit sets the production to zero if the plant
    # is closed
    m.addConstrs(
        (transport.sum('*', p) <= capacity[p] * open[p] for p in plants),
        "Capacity")

    # Using Python looping constructs, the preceding would be...
    #
    # for p in plants:
    #  m.addConstr(sum(transport[w][p] for w in warehouses) <= capacity[p] * open[p],
    #              "Capacity[%d]" % p)

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

    # Now close the plant with the highest fixed cost
    print('Initial guess:')
    maxFixed = max(openCost)
    for p in plants:
        if openCost[p] == maxFixed:
            open[p].start = 0.0
            print('Closing plant %s' % p)
            break
    print('')

    # Use barrier to solve root relaxation
    m.Params.method = 2

    # Solve
    m.optimize()

    # Print solution
    print('\nTOTAL COSTS: %g' % m.objVal)
    print('SOLUTION:')
    for p in plants:
        if open[p].x > 0.99:
            print('Plant %s open' % p)
            for w in warehouses:
                if transport[w, p].x > 0:
                    print('  Transport %g units to warehouse %s' % \
                          (transport[w, p].x, w))
        else:
            print('Plant %s closed!' % p)

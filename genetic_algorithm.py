#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""
import math
import random
import time
import pickle


def GA(facilityCount, customorCount, capacity, openCost, assignCost, demand,
       population_size=400, inheritanceProp=0.5, k_tournament=10, reproduceProp=0.5, changeProp=0.1):
    """
    遗传算法实现
    :param facilityCount:int
    :param customorCount:int
    :param capacity:[int]
    :param openCost:[int]
    :param assignCost:[[int]]
    :param demand:[int]
    :param population_size:int
    :param inheritanceProp:float
    :param k_tournament:int
    :param reproduceProp:float
    :param changeProp:float
    :return:
    """

    def assignInit():
        """
        初始化种群
        :return:
        """
        assign = [facilityCount] * customorCount

        leaveCapacity = capacity.copy()
        order = list(range(customorCount))
        try:
            random.shuffle(order)
        except RecursionError as e:
            print(order)
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

    def assignRepair(assign: [float]):
        """
        修复不可性的解
        :param assign:[float]
        :return:[float]
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

    def crossover(parent1: [float], parent2: [float]):
        """
        遗传交叉算子
        :param parent1:[float]
        :param parent2:[float]
        :return:[float][float]
        """
        # 随机交叉
        # customorCount = len(parent1)
        # changeCount = math.ceil(customorCount*changeProp)
        # o1, o2 = parent1.copy(), parent2.copy()
        # for i in random.choices(range(customorCount), k=changeCount):
        #   o1[i], o2[i] = o2[i], o1[i]
        # return o1, o2

        # ==========================================================
        # 按块遗传
        # 被分配到对应工厂的用户列表
        facilities_1 = [[] for _ in range(facilityCount)]
        facilities_2 = [[] for _ in range(facilityCount)]

        # 有被分配的工厂序号
        wasAssign_1 = set()
        wasAssign_2 = set()
        for i in range(customorCount):
            facilities_1[parent1[i]].append(i)
            wasAssign_1.add(parent1[i])
            facilities_2[parent2[i]].append(i)
            wasAssign_2.add(parent2[i])

        # 抽出几个有被分配用户的工厂
        chromosomes_1 \
            = random.sample(wasAssign_1, k=math.ceil(len(wasAssign_1) * inheritanceProp))
        chromosomes_2 \
            = random.sample(wasAssign_2, k=math.ceil(len(wasAssign_2) * inheritanceProp))
        # 子代1
        o1 = [facilityCount] * customorCount
        o2 = [facilityCount] * customorCount
        for fac in chromosomes_1:
            for cus in facilities_1[fac]:
                o1[cus] = fac
        for fac in chromosomes_2:
            for cus in facilities_2[fac]:
                o2[cus] = fac
        # 补全未被分配的维度
        for i in range(customorCount):
            if o1[i] == facilityCount:
                o1[i] = parent2[i]
        for i in range(customorCount):
            if o2[i] == facilityCount:
                o2[i] = parent1[i]
        return o1, o2

    def mutation(individual):
        """
        遗传变异算子
        :param individual:[float]
        :return:[float]
        """
        res = individual.copy()
        # 随机改变一段
        changeCount = math.ceil(len(individual) * changeProp)
        end = random.randint(0, len(individual) - 1)
        for i in range(end, end - changeCount, -1):
            res[i] = random.randint(0, facilityCount - 1)
        return res

    def mutation2(assign: [float]):
        """
        定义第二种变异算子
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

    def naturalSelection(population, newIndividuals):
        """
        自然选择
        :param population:[[float]]
        :param newIndividuals:[float]
        :return:None
        """
        # k-锦标赛
        for individual in newIndividuals:
            population.append(individual)
            competitors = random.choices(range(len(population)), k=k_tournament)
            loser = max(competitors, key=lambda i: cost(population[i]))
            population.pop(loser)

    def recordResult(record):
        print('正在写入数据')
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
        print('写入完成')

    record = []

    population = \
        [assignInit() for _ in range(population_size)]
    population = [assignRepair(e) for e in population]

    argmin = min(population, key=cost)
    value = cost(argmin)

    GENERATION = 80
    reproduceCount = math.ceil(population_size * reproduceProp)

    for _ in range(GENERATION):
        newOffspring = []
        for _ in range(reproduceCount):
            p1, p2 = random.choices(population, k=2)
            offspring1, offspring2 = crossover(p1, p2)

            offspring3 = mutation(offspring1)
            offspring4 = mutation(offspring2)
            offspring5 = mutation2(offspring1)
            offspring6 = mutation2(offspring2)

            newOffspring.append(offspring1)
            newOffspring.append(offspring2)
            newOffspring.append(offspring3)
            newOffspring.append(offspring4)
            newOffspring.append(offspring5)
            newOffspring.append(offspring6)
        # 修正非法解
        newOffspring = [assignRepair(o) for o in newOffspring]

        naturalSelection(population, newOffspring)

        newAssign = min(newOffspring, key=cost)
        newValue = cost(newAssign)
        if newValue < value:
            value = newValue
            argmin = newAssign
        record.append(value)
    recordResult({
        'type': 'GA',
        'date': time.time(),
        'population': population_size,
        'genaration': GENERATION,
        'k_tournament': k_tournament,
        'changeProp': changeProp,
        'inheritanceProp': inheritanceProp,
        'reproduceProp': reproduceProp,
        'x-axis': [i for i in range(len(record))],
        'y-axis': record,
    })
    return argmin

#! usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created by Haitao Yue at 2020/10/25
"""
import numpy as np
import os
import json
from load_file import loadFile
from algorithm.deterministic_algorithm import deterministic
from algorithm.monte_carlo_search import MCS as monte_carlo
from algorithm.local_search import LS as local_search
from algorithm.genetic_algorithm import GA as genetic
from algorithm.simulated_annealing_algorithm import SA as simulated_annealing

if __name__ == '__main__':
    input_instance = loadFile("./testInstances/easy/p1")

    if not os.path.isfile("./results.json"):
        f = open("./results.json", "w", encoding='utf-8')
        f.close()

    with open("./results.json", "r+") as f:
        try:
            results = json.load(f)
        except json.decoder.JSONDecodeError:
            results = []

    # res = deterministic(facilityCount=input_instance["facilityCount"],
    #                     customorCount=input_instance["customorCount"],
    #                     capacity=input_instance["capacity"],
    #                     openCost=input_instance["openCost"],
    #                     assignCost=input_instance["assignCost"],
    #                     demand=input_instance["demand"])
    # results.append(res)
    #
    # res = genetic(facilityCount=input_instance["facilityCount"],
    #               customorCount=input_instance["customorCount"],
    #               capacity=input_instance["capacity"],
    #               openCost=input_instance["openCost"],
    #               assignCost=input_instance["assignCost"],
    #               demand=input_instance["demand"],
    #               generation=80,
    #               population_size=20,
    #               inheritanceProp=0.5,
    #               k_tournament=10,
    #               reproduceProp=0.5,
    #               changeProp=0.1)
    # results.append(res)

    res = simulated_annealing(facilityCount=input_instance["facilityCount"],
                              customorCount=input_instance["customorCount"],
                              capacity=input_instance["capacity"],
                              openCost=input_instance["openCost"],
                              assignCost=input_instance["assignCost"],
                              demand=input_instance["demand"])
    results.append(res)

    # res = monte_carlo(facilityCount=input_instance["facilityCount"],
    #                   customorCount=input_instance["customorCount"],
    #                   capacity=input_instance["capacity"],
    #                   openCost=input_instance["openCost"],
    #                   assignCost=input_instance["assignCost"],
    #                   demand=input_instance["demand"])
    # results.append(res)

    # res = local_search(facilityCount=input_instance["facilityCount"],
    #                    customorCount=input_instance["customorCount"],
    #                    capacity=input_instance["capacity"],
    #                    openCost=input_instance["openCost"],
    #                    assignCost=input_instance["assignCost"],
    #                    demand=input_instance["demand"])
    # results.append(res)

    with open('results.json', 'w') as f:
        json.dump(results, f)

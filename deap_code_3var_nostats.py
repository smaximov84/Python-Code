# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 17:31:35 2019

@author: smaximov
"""

import os
os.chdir('C:\TRNSYS18\MyProjects\Script to run TRNSYS from python')
from objective_function import obj_funct
import random
from deap import algorithms, base, creator, tools
from multiprocessing import Pool
import time

#%%
NUM_VAR = 3
POP_SIZE = 2
MUT_PROB = 0.2
CX_PROB = 0.7
NGEN = 1
NGENpar = 1 #number of generations after which a pareto front will be produced

#%%
#OBJECTIVE FUNCTION
def evaluate(individual):
    x = obj_funct(individual,'DLSC_Temuco_multiobj',[797,798,799],[[6,8],[6,9]])
    return x

#%%
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)   

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=NUM_VAR)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=0.5, low=0, up=1, indpb=0.05)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluate)

#%%

def main():
    random.seed(6)
    pool = Pool(processes=4)                       # MULTIPLE PROCESSING
    toolbox.register("map", pool.map)
    pop = toolbox.population(POP_SIZE)
    #hof = tools.HallOfFame(80)
    hof = tools.ParetoFront()
    #stats_cost = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    #stats_emissions = tools.Statistics(key=lambda ind: ind.fitness.values[1])
    #mstats = tools.MultiStatistics(Cost=stats_cost,Emissions=stats_emissions)
    #mstats.register("min", np.min, axis=0)
    #mstats.register("mean", np.mean)
    #mstats.register("max", np.max)
    
    #%%
    for i in range(NGEN//NGENpar):
        pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CX_PROB, mutpb=MUT_PROB, ngen=NGENpar, halloffame=hof, verbose=True)
        
        #gen = logbook.select("gen")
        Solar_area_hof=[]
        Storage_size_hof=[]
        Boiler_size_hof=[]
        hof_fit_cost=[]
        hof_fit_emission=[]
        
        for ind in range(0,len(hof)): 
            print("%i %s, %s" % (ind,hof[ind], hof[ind].fitness.values))
    
            hof_fit_cost.append(hof[ind].fitness.values[0])
            hof_fit_emission.append(hof[ind].fitness.values[1])
            Solar_area_hof.append(hof[ind][0])
            Storage_size_hof.append(hof[ind][1])
            Boiler_size_hof.append(hof[ind][2])
            
        with open('DLSC_Temuco_multiobj_hof_'+str((i+1)*NGENpar)+'.csv','a') as writer:
            writer.writelines(map("{},{},{},{},{}\n".format, Solar_area_hof, Storage_size_hof, Boiler_size_hof, hof_fit_cost, hof_fit_emission))     
    return pop, hof

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
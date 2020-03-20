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
import json
import csv

#%%
NUM_VAR = 2
POP_SIZE = 50
MUT_PROB = 0.3
CX_PROB = 0.7
NGEN = 40
NGENpar = 10 #number of generations after which a pareto front will be produced

#%%
#OBJECTIVE FUNCTION
def evaluate(individual):
    x = obj_funct(individual,'DLSC_Temuco_multiobj_noLTS',[601,604],[[4,11],[4,12]])
    return x

#%%
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)   

def initIndividual(icls, content):
    return icls(content)

def initPopulation(pcls, ind_init, filename):
    with open(filename, "r") as pop_file:
        contents = json.load(pop_file)
    return pcls(ind_init(c) for c in contents)

toolbox = base.Toolbox()

#these 2 lines are used to start from an existing population
#toolbox.register("individual_guess", initIndividual, creator.Individual)
#toolbox.register("population_guess", initPopulation, list, toolbox.individual_guess, "population100.json")

#these 3 lines are used to start from a random guess
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=NUM_VAR)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=0.5, low=0, up=1, indpb=0.1)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluate)

#%%

def main():
    random.seed(4)   # if random
    pool = Pool(processes=6)                       # MULTIPLE PROCESSING
    toolbox.register("map", pool.map)
    #pop = toolbox.population_guess()  # if starting from existing population
    pop = toolbox.population(POP_SIZE) # if random
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
        #LTS_size_hof=[]
        #Boiler_size_hof=[]
        #STS_size_hof=[]
        Solar_angle_hof=[]
        hof_fit_cost=[]
        hof_fit_emission=[]
        
        
        #next lines are in case of starting an optimisation from a pareto from a previous run
        #with open('Solar_hof.csv', newline='') as inputfile:
        #    for row in csv.reader(inputfile):
        #        Solar_area_hof.append(float(row[0]))
        #with open('LTS_hof.csv', newline='') as inputfile:
        #    for row in csv.reader(inputfile):
        #        LTS_size_hof.append(float(row[0]))
        #with open('Angle_hof.csv', newline='') as inputfile:
        #    for row in csv.reader(inputfile):
        #        Solar_angle_hof.append(float(row[0]))   
        #with open('Costs_hof.csv', newline='') as inputfile:
        #    for row in csv.reader(inputfile):
        #        hof_fit_cost.append(float(row[0]))       
        #with open('Emissions_hof.csv', newline='') as inputfile:
        #    for row in csv.reader(inputfile):
        #         hof_fit_emission.append(float(row[0]))
        
        for ind in range(0,len(hof)): 
            print("%i %s, %s" % (ind,hof[ind], hof[ind].fitness.values))
    
            hof_fit_cost.append(hof[ind].fitness.values[0])
            hof_fit_emission.append(hof[ind].fitness.values[1])
            Solar_area_hof.append(hof[ind][0])
            #LTS_size_hof.append(hof[ind][1])
            #Boiler_size_hof.append(hof[ind][2])
            #STS_size_hof.append(hof[ind][1])
            Solar_angle_hof.append(hof[ind][1])
            
            
        with open('DLSC_Temuco_multiobj_hof_'+str((i+1)*NGENpar)+'.csv','a') as writer:
            writer.writelines(map("{},{},{},{}\n".format, hof_fit_cost, hof_fit_emission, Solar_area_hof, Solar_angle_hof))     
    return pop, hof

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
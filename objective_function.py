# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 17:17:24 2019

@author: smaximov
"""

import os
import shutil
import random
import time
import logging
import inspect
os.chdir('C:\TRNSYS18\MyProjects\Script to run TRNSYS from python')
from run_trnsys import RunCmd
from modify_dck import Modify_dck

def obj_funct(x, file_name, lines_modify, obj_out_position): 
    #x is a [list] with the initial values to evaluate the function
    #file_name is the name of the file without extension
    #lines_modify is a [list] with the lines to modify in the TRNSYS .dck file 
    #obj_out_poistion is a [list] of [lists] with length = 2 that shows the 
    #location of the result of the function evaluation in the output file
    #process_worker is an identifier of the worker that is performing the process
    
    new_name = file_name+'_'+str(random.randrange(99999))
    while True:
        if os.path.isfile(new_name+'.dck'): #checks if the file exists to not repeat file names
            new_name = file_name+'_'+str(random.randrange(99999))
        else:
            break
    
    shutil.copyfile(file_name+'.dck', new_name+'.dck') #creates a copy of the dck file with random number appended and works on that copy
    Modify_dck(new_name, 'dck', lines_modify, x) #modifies some rows of the original dck file to try the new population suggested by the genetic algorithm
    #pos = file_name.find('__')
    #version_lenght = len(file_name) - (pos+2)
    #version = int(file_name[-version_lenght:])
    #file_name = file_name[:-version_lenght]+str(version+1)
    max_run_time = 300      # In seconds
    Trnsys = os.path.join("C:/", "TRNSYS18", "Exe", "TrnEXE64.exe")
    RunCmd([Trnsys, new_name + '.dck', '/N'], max_run_time).Run() #runs TRNSYS with the information in the modified dck file (individual from the new population)
               
    cost_not_suplied = [] #remove for more general cases. It is here to keep a track of the not supplied energy of each run
    objective = []
    with open_file_with_log(new_name + '.ecn', inspect.getframeinfo(inspect.currentframe()).lineno, 'r') as reader:  #sometimes there was an "[Errno 13] The process cannot access the file because it is being used by another process:" so this function was added to make the program wait before attempting opening again the file.  
        pair_outputs = 0 
        for j in obj_out_position: #looks in every objective function result
            i=0
            reader.seek(0) #for every objective function has to start reading from the begining
            for i, line in enumerate(reader):
                if i+1 == obj_out_position[pair_outputs][0]: #finds the correct row, performs some cleaning and separates columns
                    line = line.replace('\n','')
                    line = line.replace(' ','')
                    columns = line.split('\t')
                    objective.append(columns[obj_out_position[pair_outputs][1]-1]) #appends the string of the columns with the objective function's value
                    cost_not_suplied = columns[9] #appends the string of the columns with the value of energy not supplied
                    break #stops reading if finds the value and starts looking for the next objective function
            pair_outputs += 1
          
    objective_float = [float(z) for z in objective] #converts the objective functions values from string to floats
    if len(objective_float) < len(obj_out_position): #checks if the tuple has the amount of elements according of the number of objectives. If it does not, then it creates a tuple with two very large numbers
        objective_float = (9999999999999999999,9999999999999999999) #it has to be changed manually to add more elements if there are more objectives. Could be automated.
    with open(file_name + '_opti' + '.csv','a') as append: #writes a file with the values of the variables and objective functions for each iteration
        values = ''
        k = 0
        for i in x:
            values = values + str(x[k]) + ',' 
            k += 1
        k = 0
        for i in objective:
            values = values + str(objective[k]) + ','
            k += 1
        values = values + str(cost_not_suplied)
        append.write(values+ '\n')
    remove_file_with_log(new_name+'.dck', inspect.getframeinfo(inspect.currentframe()).lineno) #sometimes there was an "[Errno 13] The process cannot access the file because it is being used by another process:" so this function was added to make the program wait before attempting opening again the file.
    remove_file_with_log(new_name+'.ecn', inspect.getframeinfo(inspect.currentframe()).lineno) #deletes the files that have been created by TRNSYS
    remove_file_with_log(new_name+'.log', inspect.getframeinfo(inspect.currentframe()).lineno)
    remove_file_with_log(new_name+'.lst', inspect.getframeinfo(inspect.currentframe()).lineno)
    return tuple(objective_float)


def open_file_with_log(file_name, called_from, open_type):
    failCount = 0
    try:
        return open(file_name, open_type)
    except IOError as error:
        logging.error("Failed to read file {0} in try number {1} called from {2}:\n {3}\n".format(str(file_name), str(failCount), str(called_from) ,str(error)))
        #creates a logging file
        #writes name of the file that generates the error and the line.
        time.sleep(2) #waits for 2 seconds and then repeats all the process again.
        if failCount < 20:
            failCount+=1
            open_file_with_log(file_name, called_from)
        else: 
    	    raise error

def remove_file_with_log(file_name, called_from):
    failCount = 0
    try:
        return os.remove(file_name)
    except IOError as error:
        logging.error("Failed to remove file {0} in try number {1} called from {2}:\n {3}\n".format(str(file_name), str(failCount), str(called_from) ,str(error)))
        #creates a logging file
        #writes name of the file that generates the error and the line.
        time.sleep(2) #waits for 2 seconds and then repeats all the process again.
        if failCount < 20:
            failCount+=1
            remove_file_with_log(file_name, called_from)
        else: 
    	    raise error
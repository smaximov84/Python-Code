# -*- coding: utf-8 -*-
"""
Script to replace information in text file

Created on Wed Sep 18 2019

@author: smaximov
"""

import os
import shutil
import logging
import inspect
import time
os.chdir('C:\TRNSYS18\MyProjects\Script to run TRNSYS from python')


#%%
class Modify_dck:
    """Opens text file and generates a new file with one modified line. 
    It only modifies the value in the first column of the line (before the \t).
    The new file has the same name as the original with the verison increades by 1.

    Parameters
    ----------
    file_name : string
        String with the name of the file without exension.
        The format must be 'name__version', with 'version' an int and double '_'.
    file_extension : string
        Extension of the file.
    line_numbers : list of integers 
        The number of the lines to modify, starting from 1.
    new_values : list of floats (also accepts strings)
        The new values of the parameters to replace. It has to have the same
        number of elements that line_numbers.
    keep_version: integer
        If this parameter is equal to 1, the method does not modifies the version
        and re-writes the original file.
    """
    def __init__(self, file_name, file_extension, line_numbers, new_values):
        self.file_name = file_name
        self.file_extension = file_extension
        self.new_name = self.file_name + '_b'
        self.line_numbers = line_numbers
        self.new_values = new_values
        j = 0
        with open_file_with_log(self.file_name + '.' + self.file_extension, inspect.getframeinfo(inspect.currentframe()).lineno, 'r') as reader:
            with open_file_with_log(self.new_name + '.' + self.file_extension,inspect.getframeinfo(inspect.currentframe()).lineno, 'w') as writer:
                for line in reader:
                    i = 0
                    for l_n in self.line_numbers:
                        if j+1 == l_n:
                            length = line.find(' = ') + 3
                            line = line[:length]
                            line = line + str(self.new_values[i]) + '\n'
                           # length = line.find('\t')      #This code changed the first columns value. It worked for parameters in normal types, but not for equations defined parameters.
                           # line = line[length:]
                           # line = str(self.new_values[i]) + line
                        i += 1
                    j += 1
                    writer.write(line)
        shutil.copyfile(self.new_name + '.' + self.file_extension, self.file_name + '.' + self.file_extension)
        remove_file_with_log(self.new_name + '.' + self.file_extension, inspect.getframeinfo(inspect.currentframe()).lineno)
   

#%%

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
        if failCount < 10:
            failCount+=1
            remove_file_with_log(file_name, called_from)
        else: 
    	    raise error                   


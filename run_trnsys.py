# -*- coding: utf-8 -*-
"""
Script to run Trnsys from Python

Created on Fri Aug 30 14:02:34 2019

@author: dfriedri
"""

import sys
import os
import subprocess
import threading



class RunCmd(threading.Thread):
    """Run command and terminate if it runs too long.

    Support class to run a command and terminate it if it is still running
    after a given time. This will prevent the whole optimisation from stalling
    in the case on simulation is stuck for some reason, e.g. CySim is stuck for
    the particular parameters.

    Parameters
    ----------
    cmd : string
        String with the command to run.
    timeout : float
        Time in seconds after which the command is terminated.

    Returns
    -------
    ret_value : int
        Return value; 0 indicates successful run of the command.
    """
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        with open("Output.dat", 'w', encoding="utf8") as filehandle:
            self.process = subprocess.Popen(self.cmd, stdout=filehandle)
            self.process.wait()

    def Run(self):
        """
        Run the cmd.
        """
        self.start()
        self.join(self.timeout)

        return_value = self.process.poll()

        if self.is_alive():
            self.process.terminate()
            self.join()
            return_value = -1
            print("Run not finished.")

        return return_value


def is_number(s):
    """Test if the variable s is a number

    Examples
    --------
    >>> string = is_number('red')
    >>> (string == False)
    True
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def _test():
    """Define the doctest"""
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    # Run doctest
    _test()

    max_run_time = 400      # In seconds

    Trnsys = os.path.join("C:/", "TRNSYS18", "Exe", "TrnEXE64.exe")
    deck_file = "Begin_imported.dck"
    
    
    # Run Trnsys
    return_value = RunCmd([Trnsys, deck_file], max_run_time).Run()

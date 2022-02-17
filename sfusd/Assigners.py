import numpy as np
import pandas as pd



class SchoolAssigner:
    def __init__ ( self, population ):
        self.population = population
        self.generatePriorities()



    def generatePriorities ( self ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method generatePriorities().' )



    def runAssignment ( self ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method runAssignment().' )





class DistrictWideAssigner ( SchoolAssigner ):
    def generatePriotites ( self ):
        pass



    def runAssignment ( self ):
        pass

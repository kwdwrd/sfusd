import numpy as np
import pandas as pd



class PopulationSimulator:
    def __init__ ( self ):
        pass



    def loadPopulation ( self, filename ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method loadPopulation().' )



    def savePopulation ( self, filename ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method savePopulation().' )



    def simulate ( self, estimator, sample_size ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method simulate().' )





class UniformSimulation ( PopulationSimulation ):
    def __init__ ( self ):
        self.population = []



    def loadPopulation ( self, filename ):
        pass



    def savePopulation ( self, filename ):
        pass



    def simulate ( self, estimator, sample_size ):
        for i in range( sample_size ):
            self.population.append( None )

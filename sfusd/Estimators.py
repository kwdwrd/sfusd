class PreferenceEstimator:
    def __init__ ( self ):
        pass



    def estimate ( self, data ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method estimate().' )



    def loadResults ( self, filename ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method loadResults().' )



    def saveResults ( self, filename ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method saveResults().' )



    def simulate ( self, demographics ):
        raise NotImplementedError( f'Class {self.__class__.__name__} does not implement method simulate().' )





class LogitEstimator ( PreferenceEstimator ):
    def __init__ ( self ):
        self.params = []



    def estimate ( self, data ):
        pass



    def loadResult ( self, filename ):
        pass



    def saveResults ( self, filename ):
        pass



    def simulate ( self, demographics ):
        pass

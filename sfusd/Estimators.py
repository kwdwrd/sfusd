import numpy as np





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
        #
        # Temporarily, this is just copy-pasted from the estimation notebook
        # These params are [ distance, score_ela, score_math, outside_option ]
        #
        self.params = [ -0.29594153, 0.04482865, -0.00461972, 2.12372021 ]



    def distance( school, student ):
        #
        # This is an approximation, based on the same approximation used in estimation
        #
        deg_to_km = 110.25

        dx = ( student.loc.lng - school.loc.lng ) * math.cos( school.loc.lng )
        dy = student.loc.lat - school.loc.lat

        return deg_to_km * math.sqrt( dx ** 2 + dy ** 2 )



    def estimate ( self, data ):
        pass



    def loadResult ( self, filename ):
        pass



    def saveResults ( self, filename ):
        pass



    def simulate ( self, schools, students ):
        #
        # Ignore demographics for now, as we haven't estimated them
        #
        for student in students:
            logit_errors = np.random.gumbel( 0, 1, len( schools )
            prefs        = [
                {
                    'school': school,
                    'u':      self.params[0] * LogitEstimator.distance( school, student ) + self.params[1] * schools[i].score_ela + self.params[2] * schools[i].score_math
                } for i in range( len( schools ) )
            ] + [ self.params[3] + np.random.gumbel( 0, 1, 1 ) ]

            student.prefs( prefs )

import pandas as pd





class School:
    DISTRICT_DATA_FILE = './sfusd-schools-filtered.json'



    #
    # Consider what we might expand this to
    #
    def __init__ ( self, name, loc, scores ):
        self.name   = name
        self.loc    = loc
        self.scores = scores



    #
    # Should we keep the dataframe around?
    # Should we do better OO? Or is using a dict just fine for now? (tip: it *is* fine, FOR NOW; not great long-term)
    #
    def loadSchools ( filename = None ):
        if filename is None:
            filename = School.DISTRICT_DATA_FILE

        schools_df = pd.read_json( filename )
        schools    = []

        for school in schools_df:
            schools.append( School( school['name'], { 'lat': school['latitude'], 'lng': school['longitude'] }, { 'ela': school['SELA_Y1'], 'math': 'SMATH_Y1' } ) )

        return schools

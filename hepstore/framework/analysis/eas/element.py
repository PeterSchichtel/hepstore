
## mass dictionary
mass_dict = {
    'proton' : 1.0,
    'carbon' : 12.0,
    'iron'   : 56.0,
    }

nucleon_dict = {
    'proton' : [1,0],
    'carbon' : [6,6],
    'iron'   : [26,30],
    }

class Element(object):

    def __init__(self,element):
        self.name     = element
        self.mass     = mass_dict[element]
        self.nucleons = nucleon_dict[element][0] + nucleon_dict[element][1]
        self.protons  = nucleon_dict[element][0]
        self.neutrons = nucleon_dict[element][1]
        pass

    pass

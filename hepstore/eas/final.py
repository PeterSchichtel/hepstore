
h7_dict = {
    'lightquark'    : ' j j ',
    'chargedlepton' : ' l+ l- ',
    }

class Final(object):

    def __init__(self,final):
        self.final = final
        pass

    def h7(self):
        return h7_dict[self.final]

    pass

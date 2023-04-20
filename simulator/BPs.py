from MarkerBP import MarkerBP
from twoBitHistBP import twoBitHistBP, LastBP

class MarkerBP_defaultT:
    def __init__(self, patterns, length):
        self.BP = MarkerBP(patterns, length, True)

    def pred(self):
        _, pred = self.BP.pred()
        return pred
    
    def update(self, marker):
        self.BP.update(marker)


class MarkerBP_defaultNT:
    def __init__(self, patterns, length):
        self.BP = MarkerBP(patterns, length, False)

    def pred(self):
        _, pred = self.BP.pred()
        return pred
    
    def update(self, marker):
        self.BP.update(marker)

class MarkerBP_Last:
    def __init__(self, patterns, length):
        self.BP = MarkerBP(patterns, length, False)
        self.last = False

    def pred(self):
        valid, pred = self.BP.pred()
        if valid:
            return pred
        else:
            return self.last
    
    def update(self, marker):
        self.BP.update(marker)
    
    def updateBranch(self, taken):
        self.last = taken

class MarkerBP_Hist:
    def __init__(self, patterns, length):
        self.BP1 = MarkerBP(patterns, length, False)
        self.BP2 = twoBitHistBP()

    def pred(self):
        valid, pred = self.BP1.pred()
        if valid:
            return pred
        else:
            return self.BP2.pred()
    
    def update(self, marker):
        self.BP1.update(marker)
    
    def updateBranch(self, taken):
        self.BP2.update(taken)

class BP_Hist:
    def __init__(self):
        self.BP = twoBitHistBP()

    def pred(self):
        return self.BP.pred()
    
    def updateBranch(self, taken):
        self.BP.update(taken)

class BP_Last:
    def __init__(self):
        self.BP = LastBP()

    def pred(self):
        return self.BP.pred()
    
    def updateBranch(self, taken):
        self.BP.update(taken)

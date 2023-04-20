from copy import deepcopy

NO_PATTERN = "NO_PATTERN"

class MarkerBP:
    def __init__(self, patterns, length, default):
        self.FIFO = [-1 for i in range(length)]  # This is the marker FIFO, -1 is represents null value
        self.TCAM = {}
        self.default = default
        self.length = length

        for pat in patterns:
            full_pattern = [-1 for i in range(length - len(pat))] + list(pat)
            pred = patterns[pat]
            self.TCAM[tuple(full_pattern)] = pred
        # print(self.TCAM)

    def get_match(self, pat):
        # print("Called match with", pat)

        # Create a local copy of the pattern
        copy = deepcopy(pat)
        if copy == NO_PATTERN:    # Called for the first time
            copy = deepcopy(self.FIFO)

        # Check if we have exuasted the FIFO
        all_null = True
        for val in copy:
            if val != -1:
                all_null = False
                break
        if all_null:
            return None
        
        # Check if the pattern exists in the TCAM
        if tuple(copy) in self.TCAM:
            # print("Returning", tuple(copy))
            return tuple(copy)
        else:
            first_not_null = -1
            for idx, val in enumerate(copy):
                if val != -1:
                    first_not_null = idx
                    break
            copy[first_not_null] = -1
            return self.get_match(copy) 
    
    def pred(self):
        # print("================== Called pred, FIFO:", self.FIFO, "=======================================")
        predicted = False
        prediction = False
        
        match = self.get_match(NO_PATTERN)
        if match != None:
            prediction = self.TCAM[match]
            predicted = True
        else:
            prediction = self.default
            predicted = False
       
        # print("=========== Predicted:", predicted, "Prediction", prediction, "=============================")
        return predicted, prediction

    def update(self, marker):
        self.FIFO += [marker]
        if len(self.FIFO) > self.length:
            self.FIFO = self.FIFO[-self.length:]
        # print("Returning from update, FIFO:", self.FIFO)

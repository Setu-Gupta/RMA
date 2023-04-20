class twoBitHistBP:
    count = 2
    def __int__(self):
        # Count has 4 values: 0, 1, 2, 3 which represent the strongly NT, weakly NT, weakly T, and strongly T states
        self.count = 2  # Start at weakly taken state

    def pred(self):
        if self.count > 1:  # state is 2 or 3, i.e. weakly T or weakly NT
            return True
        else:
            return False

    def update(self, taken):
        if taken:
            self.count += 1
        else:
            self.count -= 1
        
        # Bound the counter
        if self.count > 3:
            self.count = 3
        elif self.count < 0:
            self.count = 0

class LastBP:
    last = True
    def __int__(self):
        self.last = True  # Start at taken state

    def pred(self):
        return self.last

    def update(self, taken):
        self.taken = taken

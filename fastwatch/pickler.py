import pickle 
from os.path import exists


class Pickler:
    def __init__(self):
        self.path = "save.p"
        if not exists(self.path):
            self.reset()
        with open(self.path, "rb") as f:
            self.ids, self.last = pickle.load(f)
            
    def reset(self):
        with open(self.path, "wb") as f:
            pickle.dump([{}, None], f)
            
    def update(self):
        with open(self.path, "wb") as f:
            pickle.dump([self.ids, self.last], f)
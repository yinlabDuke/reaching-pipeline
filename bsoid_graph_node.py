import nex
import numpy as np

class bsoid_node():
    def __init__(self):
        self.hand = []
        self.nose = []


    def average(self):
        self.hand_v = np.mean(self.hand)
        self.hand_sd = np.std(self.hand)
        self.nose_v = np.mean(self.nose)
        self.nose_sd = np.std(self.nose)

                

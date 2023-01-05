from plante import *

class Potager :
    def __init__(self, list_plants):
        self.list_plants = list_plants
        self.rendement = 0.0
        self.total = 0.0


    def calc_productivity(self):
        rendement = 0.0
        for plant in self.list_plants:
            rendement += plant.rendement

        self.rendement = rendement / len(self.list_plants)
        return self.rendement

    def calc_twso_total(self):
        for plant in self.list_plants:
            self.total += plant.twso

        return self.total
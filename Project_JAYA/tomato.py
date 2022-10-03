from plante import Plante

class Tomato:
  def __init__(self, name):
    super().__init__(name)
    self.name = name
    self.listWater = [10, 20, 30]
    self.listSun = [5, 10, 15]
    self.listPH = [5, 6, 7]

  def myfunc(self):
    print("Hello je suis une tomate qui s'appelle " + self.name)

  def printListWater(self):
    for param in self.listWater:
      print(param)

  def printListSun(self):
    for param in self.listSun:
      print(param)

  def printListPH(self):
    for param in self.listPH:
      print(param)

  def growing_water(self, water):
    isWater = False
    if water >= 20-5 and water <= 20+5:
      isWater = True
    else:
      isWater = False

    if isWater == True:
      return True
    else:
      return False


def calculate_yield_function_water(self):
  if self.my_water < self.listWater[0]:
    return 0
  if self.my_water >= self.listWater[0] and self.my_water <= self.listWater[1]:
    yield = self.my_water / (self.listWater[1]-self.listWater[0]) - 1
    return yield
  if self.my_water >= self.listWater[1] and self.my_water <= self.listWater[2]:
    yield = self.my_water / (self.listWater[1]-self.listWater[0]) - 3





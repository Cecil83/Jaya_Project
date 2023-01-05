import csv
class Plante:
    def __init__(self, name, type_plant, position_x, position_y, rayon, color):
        self.name = name
        self.type_plant = type_plant
        self.position_x = position_x
        self.position_y = position_y
        self.rayon = rayon
        self.color = color
        self.twso = 0.0
        self.max_twso = 0.0
        self.min_twso = 0.0
        self.rendement = 0.0

    def identify_me(self):
        print("""""""""""")
        print("Bonjour moi c'est : " + self.name)
        print("Je suis une " + self.type_plant)
        print("Position en : " + self.position_x + " ; " + self.position_y)
        print("Mon reayon est de : " + self.rayon)
        print("Ma couleur est : " + self.color)

    def calc_max_min_twso_sun(self):
        list_data = []
        # reading csv file to get previous values
        csvfile = "./TWSO_" + self.type_plant + "_irrad.csv"
        #print(csvfile)
        with open(csvfile, 'r') as file:
            csvreader = csv.reader(file, delimiter='\n')
            for row in csvreader:
                if len(row) != 0:
                    #print(row)
                    list_data.append(row)

        #Calc max :
        x = str(list_data[9]).split("'")
        #print(x[1])
        y = str(x[1]).split(",")

        self.max_twso = float(y[1])

        #Calc min :
        x = str(list_data[0]).split("'")
        # print(x[1])
        y = str(x[1]).split(",")

        self.min_twso = float(y[1])

    def calc_productivity(self, twso):
        self.calc_max_min_twso_sun()

        if self.max_twso != 0.0 :
            self.rendement = (twso * 100) / self.max_twso
            return self.rendement
        else :
            print("**ERREUR : LE TWSO MAX EST EGAL A 0 !!!")


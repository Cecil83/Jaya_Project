from tomato import Tomato
#import matplotlib.pyplot as plt
#plt.plot([1, 2, 3, 4])
#plt.ylabel('some numbers')
#plt.show()

p1 = Tomato("John")
toto = p1.growing_water(20)

if toto==True:
    print("Yes ma tomate est bien arrosée")
else:
    print("Un peu d'eau s'il-te-plait")


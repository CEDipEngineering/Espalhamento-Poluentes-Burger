import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd

size = 10
k = 0.23e3
p = 2.7e3
Cp = 897
alpha =  k/(p*Cp)
print(f"Alpha: {alpha}")
barra = [[0. for e in range(size)] for i in range(size)]
dt = 1e-3
t = 0
tMax = 120
L = 0.4/size
F=alpha*dt/(L**2)
print(f"F: {F}")

for i in range(len(barra)):
    for j in range(len(barra)):
        if(i==j or (i==0 and j == (size-1))):
            barra[i][j] = 0
            continue
        if(i==0):
            barra[i][j] = 150
        if(i==(size-1)):
            barra[i][j] = 0
        if(j==(size-1)):
            barra[i][j] = 50
barra[0][0] = 150

print(f"Barra Inicial: {barra}\n")
nextBarra = np.copy(barra)
while t < tMax:
    for i in range(size):
        for j in range(size):
            #print(i,j)
            if(i == 0):
                if (j != 0) and (j!=size-1):
                    #print(f"Entrei if 1, i,j={i,j}")
                    nextBarra[j][i] = barra[j][i] + F*(barra[j][i+1] + barra[j][i+1] + barra[j+1][i] + barra[j-1][i] -4*barra[j][i])   #F*(2*barra[j+1][i] + barra[j][i+1] + barra[j][i-1]) + (1 - 4*F)*barra[j][i]
                continue
            if(i == (size-1) or j == 0 or j == (size-1)):
                continue
            nextBarra[j][i] = F*(barra[j][i+1] + barra[j][i-1] + barra[j+1][i] + barra[j-1][i]) + (1 - 4*F)*barra[j][i]

   
    # if(abs(1 - nextBarra[2][2]/barra[2][2]) <= 1e-4):
    #     barra = np.copy(nextBarra)
    #     break
    barra = np.copy(nextBarra)
    t += dt

# print(f"Tempo de convergencia: {t}\n")

a = pd.DataFrame(barra)
print(a)

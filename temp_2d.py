import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

size = 5

k = 0.23e3
p = 2.7e3
Cp = 897

alpha =  k/(p*Cp)
print(f"Alpha: {alpha}")
barra = [[0. for e in range(size)] for i in range(size)]
dt = 1e-3
t = 0
tMax = 10
L = 0.4/size
F=alpha*dt/(L**2)
print(f"F: {F}")


# Começa na esquerda, CW
limits = [None, 150, 50, 0]

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
        if i == 0 and j ==0:
            barra[i][j] = 150
print(f"Barra Inicial: {barra}\n")
nextBarra = np.copy(barra)
while t < tMax:
    for i in range(size):
        for j in range(size):
            if(j == 0):
                if (i != 0) and (i!=size-1):
                    nextBarra[i][j] = F*(2*barra[i+1][j] + barra[i][j+1] + barra[i][j-1]) + (1 - 4*F)*barra[i][j]
                continue
            if(j == (size-1)):
                continue
            if(i == 0):
                continue
            if(i == (size-1)): 
                continue
            nextBarra[i][j] = F*(barra[i+1][j] + barra[i-1][j] + barra[i][j+1] + barra[i][j-1]) + (1 - 4*F)*barra[i][j]

    
    # if(abs(1 - nextBarra[2][2]/barra[2][2]) <= 1e-4):
    #     barra = np.copy(nextBarra)
    #     break
    barra = np.copy(nextBarra)
    t += dt

# plt.figure(figsize=(18,11))
# plt.title("Distribuição de temperaturas na barra")
# plt.plot([i*L for i in range(11)], barra)
# plt.xlabel("Posição(m)")
# plt.ylabel("Temperatura (°C)")
# plt.grid(True)
# plt.show()
print(f"Tempo de convergencia: {t}\n")
print(f"Barra Final: \n{barra}\n")
print(f"Soma: {np.sum(barra)}")

plt.figure(figsize=(10, 10))
plt.imshow(barra, cmap='viridis', extent=(0, size, 0, size))
plt.colorbar()
plt.savefig("temp.png")
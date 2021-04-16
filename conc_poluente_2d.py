import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import math
import multiprocessing
import time

def main(Lx, Ly, dm, K, dQ, a, b, alpha, t, td, tMax, pipe=None):
    print(f"Starting computation for dump at {(a, b)} for {td}s\n")
    def zera_negativo(a):
        if a < 0:
            a = 0
        return a

    barra = np.zeros((int(Ly/dm), int(Lx/dm)), dtype=np.float64)
    nextBarra = np.copy(barra)
    pi_over_5 = math.pi/5
    u = 2
    a = a/dm  # Converte posição em metros pra indíce na matriz
    b = b/dm  # ..
    dt = dm**2/(8*K)  # dt < dx**2/4K --> dt < 0.0625 / Coloquei metade disso
    bateu_na_borda = False
    while t < tMax:
        for i in range(int(Lx/dm)):
            for j in range(int(Ly/dm)):
                # u é constante
                v = 0
                tresh=0.2
                # Lidando com casos de bordas
                if(i == 0):
                    if (j != 0) and (j != int(Ly/dm)-1):
                        nextBarra[j][i] = barra[j][i+1]
                        nextBarra[j][i] = zera_negativo(nextBarra[j][i])
                        if nextBarra[j][i]>tresh and not bateu_na_borda and not pipe:
                            bateu_na_borda = True
                            print(f"Bateu na borda i==0 com a conc={barra[j][i]} em t = {t+dt}")
                    continue
                if(i == int(Lx/dm)-1):
                    if (j != 0) and (j != int(Ly/dm)-1):
                        nextBarra[j][i] = barra[j][i-1]
                        nextBarra[j][i] = zera_negativo(nextBarra[j][i])
                        if nextBarra[j][i]>tresh and not bateu_na_borda and not pipe:
                            bateu_na_borda = True
                            print(f"Bateu na borda i==n com a conc={barra[j][i]} em t = {t+dt}")
                    continue
                if(j == 0):
                    if (i != 0) and (i != int(Lx/dm)-1):
                        nextBarra[j][i] = barra[j+1][i]
                        nextBarra[j][i] = zera_negativo(nextBarra[j][i])
                        if nextBarra[j][i]>tresh and not bateu_na_borda and not pipe:
                            bateu_na_borda = True
                            print(f"Bateu na borda j==0 com a conc={barra[j][i]} em t = {t+dt}")
                    continue
                if(j == int(Ly/dm)-1):
                    if (i != 0) and (i != int(Lx/dm)-1):
                        nextBarra[j][i] = barra[j-1][i]
                        nextBarra[j][i] = zera_negativo(nextBarra[j][i])
                        if nextBarra[j][i]>tresh and not bateu_na_borda and not pipe:
                            bateu_na_borda = True
                            print(f"Bateu na borda j==n com a conc={barra[j][i]} em t = {t+dt}")
                    continue

                # Derivadas direcionais de primeira e segunda ordem (e fluxo de poluentes)
                delx = -u*(barra[j][i+1] - barra[j][i-1])/(2*dm)
                dely = -v*(barra[j+1][i] - barra[j-1][i])/(2*dm)
                del2x = K*(barra[j][i+1] - 2*barra[j][i] + barra[j][i-1])/dm**2
                del2y = K*(barra[j+1][i] - 2*barra[j][i] + barra[j-1][i])/dm**2
                qdot = dQ/dm**2
                # print(f"concentracao: {nextBarra[j][i]} e isso?: {dt*(delx + dely + del2x + del2y)}")

                # Se estivermos despejando poluente (t<td) colocamos o termo do fluxo (qdot)
                if t < td:
                    if i == a and j == b:
                        nextBarra[j][i] = barra[j][i] + dt * \
                            (delx + dely + del2x + del2y + qdot)

                        nextBarra[j][i] = zera_negativo(nextBarra[j][i])

                        # nextBarra[j][i] += dQ*dt
                        # print(f"tempo: {t}  concentracao:{nextBarra[j][i]}  delta: {[dt, delx , dely , del2x , del2y, qdot]}    e isso??:{dt*(delx + dely + del2x + del2y)}")
                        continue

                # Tratamento do caso genérico, diferente de a e b
                nextBarra[j][i] = barra[j][i] + \
                    dt*(delx + dely + del2x + del2y)

                nextBarra[j][i] = zera_negativo(nextBarra[j][i])

        # print(nextBarra[a][b])

        # if(abs(1 - nextBarra[2][2]/barra[2][2]) <= 1e-4):
        #     barra = np.copy(nextBarra)
        #     break
        barra = np.copy(nextBarra)
        t += dt
        # if bateu_na_borda:
        #     return barra
    print(np.max(barra))
    barra = barra[::-1]
    try:
        pipe.send(barra)
        pipe.close()
    except Exception as e:
        return np.copy(barra)

if __name__ == '__main__':
    Lx = 30
    Ly = 20
    dm = 0.5
    K = 1
    dQ = 150
    alpha = 1
    t = 0
    td = 2
    tMax = 6
    if True:
        pipes = []
        processes = []
        args = [1]
        num_exp = len(args)
        output = [0]*num_exp
        print(f"Starting process:\n")
        start = time.perf_counter()
        for i in range(num_exp):
            pipes.append(multiprocessing.Pipe())
            processes.append(multiprocessing.Process(target=main, args=(Lx, Ly, dm, args[i], dQ, 3, 3, alpha, t, td, tMax, pipes[i][1]), daemon=True))
            processes[i].start()
        
        for i in range(num_exp):
            output[i] = pipes[i][0].recv()
            processes[i].join() 
        print(f"Process done with time of {time.perf_counter()-start}.")
    
    # output = [0]
    # output[0] = main(Lx, Ly, dm, 1, dQ, 5, 5, alpha, t, td, tMax)
    # args=[1]
    for index, i in enumerate(output):
        plt.figure(figsize=(10, 10))
        plt.imshow(i, cmap='viridis', vmin=0, vmax=1, extent=(0, Lx, 0, Ly))
        plt.colorbar()
        plt.title(f"K={args[index]} e (a,b)={(i[int(5/dm)][int(5/dm)]):.03}")
        plt.savefig("K="+str(args[index])+".png")
    
    # start2 = time.perf_counter()
    # for i in range(num_exp):
    #     main(Lx, Ly, dm, args[i], dQ, 5, 5, alpha, t, td, tMax, None)
    # print(f"Tempo sem paralelização: {time.perf_counter() - start2}") # No teste: 55.3s versus 210.7s
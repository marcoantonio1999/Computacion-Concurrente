import threading
from random import randint
import time
from typing import final

from torch import rand

dimension = int(input("introduce el numero de la dimendion de la matriz"))
numHilos = int(input("escribe el numero de hilos"))

matrix1 = [[randint(0,100) for x in range(dimension)] for y in range(dimension)]
matrix2 = [[randint(0,100) for x in range(dimension)] for y in range(dimension)]
respuestaHilos = []
for i in range(dimension):
    respuestaHilos.append(0)

def mulSecuencial():
    """
    Funcion para calcular la multiplicacion de matrices de manera secuencial
    """
    res = [[0 for x in range(dimension)] for y in range(dimension)]  

    for i in range(len(matrix1)): 
        for j in range(len(matrix2[0])): 
            for k in range(len(matrix2)): 
                res[i][j] += matrix1[i][k] * matrix2[k][j] 

def aplicaMatriz(numHilo, **datos):
    """
    Funcion para calcular la multiplicacion de matrices de manera multihilo
    """
    for k in range(len(matrix1)):
        if (k+1)%numHilos == numHilo:
            res = [0 for i in range(dimension)]  
            for i in range(len(matrix2[0])):
                for j in range(len(matrix2)):
                    res[i] +=  matrix1[k][j] * matrix2[j][i]
            respuestaHilos[k] = res





def mulHilo():
    """
    Funcion para crear los hilos y mandar a llamar la funcion
    """
    for numHilo in range(numHilos):
        hilo = threading.Thread(target = aplicaMatriz,
        args=(numHilo,),
        kwargs={
           }
        )
        hilo.start()
        hilo.join()

def pruebas():
    """
    Funcion para hacer las pruebas
    """
    inicioH = time.time()
    for i in range(10):
        mulHilo()
    finH = time.time()

    print("tiempo promedio MultiHilo:", ( finH-inicioH)/10 )

    inicioS = time.time()
    for i in range(10):
        mulSecuencial()
    finS = time.time()
    print("tiempo promedio Secuencial", ( finS-inicioS )/10 )

pruebas()
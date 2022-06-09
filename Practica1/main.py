from mimetypes import init
from tracemalloc import start
import cv2
from matplotlib import image
import numpy as np
import threading
import math
import time

__author__ = "Marco Antonio Orduna Avila"
__license__ = "ninguna"
__version__ = "1.0.1"


def escalaGrises(imagen):
    """
    Filtro que nos da la escala de grises promedio de los valores rgb
    imagen: array
        la imagen a la que le vamos aplicar el filtro

    returns
    -------

    imagen
        la imagen con el filtro aplicado


    """
    y,x,d = imagen.shape
    for j in range(y):
        for i in range(x):
            b = int(imagen[j,i,0])
            g = int(imagen[j,i,1])
            r = int(imagen[j,i,2])
            prom = (b+g+r )/3
            imagen[j,i] = [prom,prom,prom]
    return imagen

def luma(imagen):
    """
    filtro escala de grises luma
    imagen: array
        la imagen a la que le vamos aplicar el filtro

    returns
    -------

    imagen
        la imagen con el filtro aplicado

    """
    y,x,d = imagen.shape
    for j in range(y):
        for i in range(x):
            r = imagen[j,i,2]
            g = imagen[j,i,1]
            b = imagen[j,i,0]
            gray = r*0.03 + g*0.59 + b*0.11
            imagen[j,i] = [gray,gray,gray]
    return imagen

def luma2(imagen):
    """
    filtro escala de grises luma 2
    
    paramtetros
    ----------
    imagen: array
        la imagen a la que le vamos aplicar el filtro
    
    returns
    -------

    imagen
        la imagen con el filtro aplicado
    """
    y,x,d = imagen.shape
    for j in range(y):
        for i in range(x):
            r = imagen[j,i,2]
            g = imagen[j,i,1]
            b = imagen[j,i,0]
            gray = r*0.2126 + g*0.7152 + b*0.0722
            imagen[j,i] = [gray,gray,gray]
            
    return imagen

def grisSingle(imagen, color):
    """
    filtro escala de grises single

    parametros
    ----------

    imagen: array
        la imagen a la que le vamos aplicar el filtro
    
    returns
    -------

    imagen
        la imagen con el filtro aplicado
    """
    y,x,d = imagen.shape
    for j in range(y):
        for i in range(x):
            if color == 1:
                imagen[j,i] = [imagen[j,i,2],imagen[j,i,2],imagen[j,i,2]]
            if color == 2:
                imagen[j,i] = [imagen[j,i,1],imagen[j,i,1],imagen[j,i,1]]
            if color == 3:
                imagen[j,i] = [imagen[j,i,0],imagen[j,i,0],imagen[j,i,0]]
    return imagen



def calculaSuma(matriz):
    """
    Calcula la suma de los valores rgb

    Parametros
    ----------

    matriz: array
        una matirz de 3 dimensiones, el alto, el ancho y los valores rgb

    returns
    -------

    tupla
        los valores de la suma
    
    """
    sb,sg,sr = 0,0,0

    for i in matriz:
        for j in i:
            sb += j[0]
            sg += j[1]
            sr += j[2]

    return sb,sg,sr

def blurEquinas(imagen):
    """
    Aplica el fitlro de blur solamente a las esquinas de la imagen

    parametros
    ----------
    imagen: array
        la imagen a la que le vamos aplicar el filtro a sus lados

    returns
    -------

    imagen
        la imagen con el filtro ya aplicado
    """

    y,x,d = imagen.shape
    imagen[0,0] = (imagen[1,0])*0.333 + (imagen[0,0])*0.333 + (imagen[0,1])*0.333
    imagen[0,x-1] = (imagen[0,x-2])*0.333 + (imagen[0,x-2])*0.333 + (imagen[1,x-2])*0.333
    imagen[y-1,0] = (imagen[y-1,0])*0.333 + (imagen[y-2,0])*0.333 + (imagen[y-1,1])*0.333
    imagen[y-1,x-1] = (imagen[y-1,x-1])*0.333 + (imagen[y-1,x-2])*0.333 + (imagen[y-2,x-1])*0.333
    return imagen

def blurLados(imagen):
    """
    Aplica el fitlro de blur solamente a los lados de la imagen

    parametros
    ----------
    imagen: array
        la imagen a la que le vamos aplicar el filtro a sus lados

    returns
    -------

    imagen
        la imagen con el filtro ya aplicado
    """
    y,x,d = imagen.shape
    for i in range(x):
        if i ==0 or i+1 == x:
            continue 
        imagen[0,i] = (imagen[0,i])*0.25 + (imagen[0,i-1])*0.25 + (imagen[0,i+1])*0.25 +(imagen[1,i])*0.25
    for i in range(x):
        if i ==0 or i+1 ==x:
            continue
        imagen[y-1,i] = (imagen[y-1,i])*0.25 + (imagen[y-1,i-1])*0.25 + (imagen[y-1,i+1])*0.25 +(imagen[y-2,i])*0.25
    for j in range(y):
        if j ==0 or j+1 ==y:
            continue
        imagen[j,0] = (imagen[j,0])*0.25 + (imagen[j-1,0])*0.25 + (imagen[j+1,0])*0.25 +(imagen[j,1])*0.25
    for j in range(y):
        if j ==0 or j+1 ==y:
            continue
        imagen[j,x-1] = (imagen[j,x-1])*0.25 + (imagen[j-1,x-1])*0.25 + (imagen[j+1,x-1])*0.25 +(imagen[j,x-1])*0.25

    return imagen

def blur(imagen):
    """
    Filtro Blur

    parametros
    ---------

    imagen: array
        imagen a cual le vamos aplicar el filtro

    returns
    -------

    imagen
        la imagen con el filtro ya aplicado
    """
    y,x,d = imagen.shape
    matriz = [
        [[0,0,0],[.2,.2,.2],[0,0,0]],
        [[.2,.2,.2],[.2,.2,.2],[.2,.2,.2]],
        [[0,0,0],[.2,.2,.2],[0,0,0]]
    ]
    matrizNp = np.array(matriz)
    for j in range(y):
        for i in range(x):
            if i-(3//2) < 0 or i+(3//2)+1>x:
                        continue   
            if j-(3//2) < 0 or j+(3//2)+1>y:
                        continue
            porcion = imagen[j-(3//2) : j+(3//2)+1, i-(3//2): i+(3//2)+1]
            imagen[j,i]  = calculaSuma(matrizNp * porcion)
    imagen = blurEquinas(imagen)
    imagen = blurLados(imagen)
    return imagen

def blur2(imagen):
    """
    Segunda version del filtro blur

    Parametros
    ----------

    iamgen: array
        la imagen a la cual le aplicaremos el filtro

    returns
    -------

    imagen
        la imagen con el filtro ya aplicado
    """
    y,x,d = imagen.shape
    matrizS = [
        [[0,0,0],[0,0,0],[1,1,1],[0,0,0],[0,0,0]],
        [[0,0,0],[1,1,1],[1,1,1],[1,1,1],[0,0,0]],
        [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
        [[0,0,0],[1,1,1],[1,1,1],[1,1,1],[0,0,0]],
        [[0,0,0],[0,0,0],[1,1,1],[0,0,0],[0,0,0]]
    ]
    matriz = np.array(matrizS)

    matriz3 = [

        [[0,0,0],[.2,.2,.2],[0,0,0]],
        [[.2,.2,.2],[.2,.2,.2],[.2,.2,.2]],
        [[0,0,0],[.2,.2,.2],[0,0,0]]
    ]

    matrizNp3 = np.array(matriz3)
  
    for j in range(y):
        for i in range(x):
            if i-(5//2) < 0 or i+(5//2)+1>x:
                if i-(3//2) < 0 or i+(3//2)+1>x:
                    continue
                if j-(3//2) < 0 or j+(3//2)+1>y:
                    continue   
                porcion = imagen[j-(3//2) : j+(3//2)+1, i-(3//2): i+(3//2)+1]
                imagen[j,i]  = calculaSuma(matrizNp3 * porcion)         
                continue
            
            if j-(5//2) < 0 or j+(5//2)+1>y:
                if i-(3//2) < 0 or i+(3//2)+1>x:
                    continue
                if j-(3//2) < 0 or j+(3//2)+1>y:
                    continue   
                porcion = imagen[j-(3//2) : j+(3//2)+1, i-(3//2): i+(3//2)+1]
                imagen[j,i]  = calculaSuma(matrizNp3 * porcion)
                continue
            porcion = imagen[j-(5//2) : j+(5//2)+1, i-(5//2): i+(5//2)+1]
            imagen[j,i]  = calculaSuma((1/13)*(matriz * porcion))

    imagen = blurEquinas(imagen)
    imagen = blurLados(imagen)
    return imagen

def getMatriz(k):
    """
    funcion que nos da la matriz indentidad de tamanio kxk

    parametros
    ----------

    k: integer
        la dimension de la matriz
    
    returns
    -------

    matriz
        la matriz identidad

    """
    matrizS = []
    for i in range(k):
        matrizS.append([])
        for j in range(k):
            matrizS[i].append([])
    
    
    for i in range(k):
        for j in range(k):
            if i == j:
                matrizS[i][j] =  [1,1,1]
                continue
            matrizS[i][j] = [0,0,0]
    return matrizS


def motionBlur(imagen):
    """
    filtro motion blur

    parametros
    ----------

    imagen: array
        la imagen a la cual le aplicaremos el filtro

    returns
    -------

    imagen
        la imagen con el filtro ya aplicado
    """

    y,x,d = imagen.shape
    
    

    for j in range(y):
        for i in range(x):
            
            try:
                porcion = imagen[j-(9//2) : j+(9//2)+1, i-(9//2): i+(9//2)+1]
                imagen[j,i]  = calculaSuma((1/9)*(getMatriz(9) * porcion))
                continue
            except:
                try:
                    porcion = imagen[j-(5//2) : j+(5//2)+1, i-(5//2): i+(5//2)+1]
                    imagen[j,i]  = calculaSuma((1/5)*(getMatriz(5) * porcion))
                except:
                    try:
                        porcion = imagen[j-(3//2) : j+(3//2)+1, i-(3//2): i+(3//2)+1]
                        imagen[j,i]  = calculaSuma((1/3)*(getMatriz(3) * porcion))
                    except:
                        porcion = imagen[j-(1//2) : j+(1//2)+1, i-(1//2): i+(1//2)+1]
                        imagen[j,i]  = calculaSuma((1/1)*(getMatriz(1) * porcion))
            
    return imagen

def sharpenEsquinas(imagen):
    """
    Funcion para aplicar e filtro de sharpen solamente en las esquinas

    parametros
    ----------

    imagen: array
        la imagen para aplicar el filtro
    
    returns
    -------

    imagen
        la imagen con el fitlro ya aplicado

    """
    y,x,d = imagen.shape
    imagen[0,0] = (imagen[1,0])*3 + (imagen[0,0])*-1 + (imagen[0,1])*-1
    imagen[0,x-1] = (imagen[0,x-2])*3 + (imagen[0,x-2])*-1 + (imagen[1,x-2])*-1
    imagen[y-1,0] = (imagen[y-1,0])*3 + (imagen[y-2,0])*-1 + (imagen[y-1,1])*-1
    imagen[y-1,x-1] = (imagen[y-1,x-1])*3 + (imagen[y-1,x-2])*-1 + (imagen[y-2,x-1])*-1
    return imagen


def sharpenLados(imagen):
    """
    Funcion para aplicar e filtro de sharpen solamente en las esquinas

    parametros
    ----------

    imagen: array
        la imagen para aplicar el filtro
    
    returns
    -------

    imagen
        la imagen con el fitlro ya aplicado

    """
    y,x,d = imagen.shape

    for i in range(x):
        if i ==0 or i+1 == x:
            continue
        
        imagen[0,i] = (imagen[0,i])*4 + (imagen[0,i-1])*0.25 + (imagen[0,i+1])*0.25 +(imagen[1,i])*0.25
    for i in range(x):
        if i ==0 or i+1 ==x:
            continue
        imagen[y-1,i] = (imagen[y-1,i])*4 + (imagen[y-1,i-1])*0.25 + (imagen[y-1,i+1])*0.25 +(imagen[y-2,i])*0.25
    for j in range(y):
        if j ==0 or j+1 ==y:
            continue
        imagen[j,0] = (imagen[j,0])*4 + (imagen[j-1,0])*0.25 + (imagen[j+1,0])*0.25 +(imagen[j,1])*0.25
    for j in range(y):
        if j ==0 or j+1 ==y:
            continue
        imagen[j,x-1] = (imagen[j,x-1])*4 + (imagen[j-1,x-1])*0.25 + (imagen[j+1,x-1])*0.25 +(imagen[j,x-1])*0.25        
    return imagen

def sharpen(imagen):
    """
    Funcion para aplicar e filtro de sharpen

    parametros
    ----------

    imagen: array
        la imagen para aplicar el filtro
    
    returns
    -------

    imagen
        la imagen con el fitlro ya aplicado

    """
    y,x,d = imagen.shape
    copia = imagen.copy()
    matrizS =[]
    for i in range(3):
        matrizS.append([])
        for j in range(3):
            matrizS[i].append([])
    for i in range(3):
        for j in range(3):
            if i == 1 and j ==1:
                matrizS[i][j] = [9,9,9]
            else:
                matrizS[i][j] = [-1,-1,-1]

    matriz = np.array(matrizS)

    for j in range(y):
        for i in range(x):
            if i-(3//2) < 0 or i+(3//2)+1>x:
                        continue   
            if j-(3//2) < 0 or j+(3//2)+1>y:
                        continue
            porcion = imagen[j-(3//2):j+(3//2)+1,   i-(3//2):i+(3//2)+1 ]
            mul = matriz*porcion
            
            b,g,r = calculaSuma(mul)

            minimo = min(b,g,r)
            maximo = max(b,g,r)
            if  minimo<0:
                diferencia = -1 * minimo
                b = b+diferencia
                g = g+diferencia
                r = r+diferencia

            if  maximo>255:
                diferencia = maximo -255
                b = b-diferencia
                g = g-diferencia
                r = r-diferencia

            copia.itemset((j,i,0),b)
            copia.itemset((j,i,1),g)
            copia.itemset((j,i,2),r)
    return copia


def componenteRGB(imagen,r,g,b):
    """
    Funcion para aplicar e filtro de componente rgb

    parametros
    ----------

    imagen: array
        la imagen para aplicar el filtro
    r: integer
        el rojo para aplicar
    g: integer
        el verde para aplicar
    b: integer
        el azul para alicar

    returns
    -------

    imagen
        la imagen con el fitlro ya aplicado

    """
    y,x,d = imagen.shape
    for j in range(y):
        for i in range(x):

            nb = imagen[j,i,0]+b
            if nb > 255:
                nb = 255
            if nb < 0:
                nb = 0
            ng = imagen[j,i,1]+g
            if ng > 255:
                ng = 255
            if ng < 0:
                ng = 0
            nr = imagen[j,i,2]+r
            if nr > 255:
                nr = 255
            if nr < 0:
                nb = 0
                        
            imagen[j,i,0] = nb
            imagen[j,i,1] = ng
            imagen[j,i,2] = nr
    return imagen

def altoContraste(imagen):
    """
    Funcion para aplicar e filtro de alto contraste

    parametros
    ----------

    imagen: array
        la imagen para aplicar el filtro
    
    returns
    -------

    imagen
        la imagen con el fitlro ya aplicado

    """
    y,x,d = imagen.shape
    imgGris = escalaGrises(imagen)
    
    for j in range(y):
        for i in range(x):
            if imgGris[j,i,0] > 127: 
                imagen[j,i] = [255,255,255]
            else:
                imagen[j,i] = [0,0,0]
    return imagen

def aplicaHilo(numHilo, **datos):
    """
    Funcion que aplica el filtro dado en los parametros del hilo

    parametros
    --------

    numHilo: integer
        el numero de hilos que estamos ejecutando
    **datos: multiple
        los datos que llevan vada hilo para poder ejecutar su tarea
    """

    fun = datos['funcion']
    b,g,r = datos['RGB']
    colorH = datos['col']
    
    y,x,d = img.shape
    
    ancho = math.floor(x/numHilos)
    porciones = []
    
    for i in range(numHilos):
        porcion = img[ 0:y-1  , i*ancho:(i+1)*ancho]
        porciones.append(porcion)

    if fun == 1:
        resh[numHilo] = escalaGrises(porciones[numHilo])
    if fun == 2:
        resh[numHilo] = luma(porciones[numHilo])
    if fun == 3:
        resh[numHilo] = luma2(porciones[numHilo])
    if fun == 4:
        resh[numHilo] = grisSingle(porciones[numHilo], colorH)
    if fun == 5:
        resh[numHilo] = blur(porciones[numHilo])
    if fun == 6:
        resh[numHilo] = blur2(porciones[numHilo])
    if fun == 7:
        resh[numHilo] = motionBlur(porciones[numHilo])
    if fun == 8:
        resh[numHilo] = sharpen(porciones[numHilo])
    if fun == 9:
        resh[numHilo] = componenteRGB(porciones[numHilo], b,g,r)
    if fun == 10:
        resh[numHilo] = escalaGrises(porciones[numHilo])


    
    


if __name__ == "__main__":
    """
    main del archivo
    """
    
    img = input("introduce el nombre del archivo a aplicar el filtro con la extension\n")
    img = cv2.imread("photo.jpg")
    resh = []


    numHilos = int(input("introduce el numero de hilos\n"))

    print("Bienvenidos al programa que calcula los siguientes filtros")
    print("1. promedio")
    print("2, correctud ")
    print("3. correctud 2")
    print("4. single color")
    print("5. Blur")
    print("6. Blur 2")
    print("7. Motion Blur")
    print("8, Sharppen")
    print("9. Componenet RGB")
    print("10. Alto contraste")

    funcion = int(input("Introuce el numero dela funcion que deseas aplicar"))

    r=0
    g=0
    b=0

    if funcion == 9:
        r = int(input("valor R"))
        g = int(input("valor G"))
        b = int(input("valor B"))
    col = ''
    if funcion == 4:
        print("elige el color sobre el que deseas hacer el filtro") 
        print("1. rojo")
        print("2, verde")
        print("3. azul")
        col=int(input())

    for i in range(numHilos):
        resh.append(0)
    incio = time.time()
    for numHilo in range(numHilos):
        hilo = threading.Thread(target = aplicaHilo,
        args=(numHilo,),
        kwargs={'funcion' : funcion, 
                "RGB":(b,g,r),
                "col" : col
            }
        )
        hilo.start()
    hilo.join()

    fin = time.time()

    print("multihilo", fin-incio )

    inicioS = time.time()
    if funcion == 1:
        filtro= escalaGrises(img)
    if funcion == 2:
        filtro = luma(img)
    if funcion == 3:
        filtro = luma2(img)
    if funcion == 4:
        filtro = grisSingle(img)
    if funcion == 5:
        filtro = blur(img)
    if funcion == 6:
        filtro = blur2(img)
    if funcion == 7:
        filtro = motionBlur(img)
    if funcion == 8:
        filtro = sharpen(img)
    if funcion == 9:
        filtro = componenteRGB(img)
    if funcion == 10:
        filtro = escalaGrises(img)
    finS = time.time()
    print("Secuencial", finS-inicioS)    
    imgNueva = cv2.hconcat(resh)
    cv2.imwrite("final2.jpg",imgNueva)
import cv2
from cv2 import imwrite, imread
import numpy as np
import sys

def reflexaoLinhas(pathFileName):
    img = imread(pathFileName, 0)
    tam = len(img)/2
    list1 = img[:int(tam):]
    list2 = list1[::-1]
    result = [None]*(len(list1)+len(list2))
    result[0:int(tam):1] = list1
    result[int(tam):int(len(result)):1] = list2
    imgOut = np.array(result)
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('ReflectionLinesOutputs/reflexao_linhas_superiores_' + imgName, imgOut)

def main(argv1):
    try:
        reflexaoLinhas(argv1)
    except:
        print("Caminho para imagem nao definido !")
    

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python reflexaoLinhasSuperiores.py pathCompletoParaImagem")
import cv2
from cv2 import imwrite, imread
import numpy as np
import sys

def inversaoLinhas(pathFileName):
    img = imread(pathFileName, 0)
    list1 = img[::2,::-1]
    list2 = img[1::2,::]
    result = [None]*(len(list1)+len(list2))
    result[::2] = list1
    result[1::2] = list2
    imgOut = np.array(result)
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('InverseLinesOutputs/inversao_linhas_pares_' + imgName, imgOut)

def main(argv1):
    try:
        inversaoLinhas(argv1)
    except:
        print("Caminho para imagem nao definido !")
    

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python inversaoLinhasPares.py pathImagem")
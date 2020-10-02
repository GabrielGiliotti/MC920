import cv2
from cv2 import imwrite, imread
import numpy as np
import sys

def espelhamentoVertical(pathFileName):
    img = imread(pathFileName, 0)
    img_flip = cv2.flip(img, 0)
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('MirrorOutputs/vertical_mirror_' + imgName, img_flip)

def main(argv1):
    try:
        espelhamentoVertical(argv1)
    except:
        print("Caminho para imagem nao definido !")
    

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python espelhamento.py pathImagem")
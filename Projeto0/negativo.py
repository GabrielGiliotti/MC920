from cv2 import imwrite, imread
import numpy as np
import sys

def negativo(pathFileName):
    img = 255 - imread(pathFileName, 0)
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('NegativeOutputs/negative_' + imgName, img)

def main(argv):
    negativo(argv)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python negativo.py pathImagem")
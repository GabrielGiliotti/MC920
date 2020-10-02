from cv2 import imwrite, imread
import numpy as np
import sys

def ajusteBrilho(pathFileName, gama):
    if(gama == "0"):
        gama = "1"
    # (i) conversao para do intervalo [0,255] para intervalo [0,1]
    img = imread(pathFileName, 0)/255
    # (ii) aplicando a equacao B = A ** (1/gama)
    img = img**(1/float(gama))
    # (iii) retornando valores para intervalo [0,255]
    img = np.uint8(img*255)    
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('BrightAdjustOutputs/ajuste_brilho_' + gama + '_' + imgName, img)


def main(argv1, argv2):
    ajusteBrilho(argv1, argv2)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        print("Path da imagem nao definido ou valor gama nao informado !")
        print("Execute: ", end="")
        print("python ajustaBrilho.py pathImagem valorGamaDiferenteDeZero")
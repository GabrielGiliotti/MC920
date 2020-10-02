from cv2 import imwrite, imread
import numpy as np
import sys

def extraiPlanoBits(pathFileName, ordem):
    img = imread(pathFileName, 0)
    # img >> ordem faz shift right nos bits de um pixel da imagem
    img = ((img >> int(ordem)) % 2)*255
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('BitPlaneOutputs/plano_bits_ordem_' + ordem + '_' + imgName, img)


def main(argv1, argv2):
    extraiPlanoBits(argv1, argv2)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        print("Path da imagem nao definido ou valor ordem nao informado !")
        print("Execute: ", end="")
        print("python extrairPlanoBits.py pathImagem valorPlanoBitsDe0a7")
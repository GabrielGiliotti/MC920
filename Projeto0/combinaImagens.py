from cv2 import imwrite, imread
import numpy as np
import sys

def combinaImagens(pathFileName1, pathFileName2, pond1, pond2):
    img1 = imread(pathFileName1, 0)
    img2 = imread(pathFileName2, 0)
    output = float(pond1)*img1 + float(pond2)*img2
    index1 = pathFileName1.rfind("\\")
    index2 = pathFileName2.rfind("\\")
    imgName1 = pathFileName1[index1+1:]
    imgName1 = imgName1[:len(imgName1)-4]
    imgName2 = pathFileName2[index2+1:]
    imwrite('MergeImagesOutputs/merge_'+ str(pond1) + '_' + str(pond2) + '_' + imgName1 + '_' + imgName2, output)


def main(argv1, argv2, argv3, argv4):
    combinaImagens(argv1, argv2, argv3, argv4)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    except:
        print("Path das imagens nao definidos ou valores de ponderacao nao informados !")
        print("Execute: ", end="")
        print("python combinaImagens.py pathImagem1 pathImagem2 valorPond1 valorPond2")
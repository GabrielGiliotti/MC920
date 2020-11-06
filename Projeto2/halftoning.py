import cv2 as cv
import numpy as np
import sys

def halftoning(imgPath):
    # Leitura da Img
    img = cv.imread(imgPath)

    # Separacao da Img orginal em RGB
    b,g,r = cv.split(img)
    k = np.zeros_like(b)
    b = cv.merge([b,k,k])
    g = cv.merge([k,g,k])
    r = cv.merge([k,k,r])

    # Aplicar os filtros para cada espectro


    # Saida imgs
    index = imgPath.rfind("\\")
    imgName = imgPath[index+1:]
    cv.imwrite("Outputs/"+ imgName +"_blue.png",b); 
    cv.imwrite("Outputs/"+ imgName +"_green.png",g); 
    cv.imwrite("Outputs/"+ imgName +"_red.png",r); 
    #cv.imwrite("Outputs/"+ imgName +".png", img)


def main(argv1):
    halftoning(argv1)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python halftoning.py pathImagem")
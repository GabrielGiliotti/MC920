from cv2 import imwrite, imread
import numpy as np
import sys
import math

def intervaloIntensidade(pathFileName):
    # Modo 1 de fazer
    """img = imread(pathFileName, 0)
    img = np.uint8(((img/255) * 100) + 100)
    #img = np.trunc(((img/255) * 100) + 100)
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('IntensityOutputs/new_intensity1_' + imgName, img)"""
    # Modo 2 de fazer
    img = imread(pathFileName, 0)
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    img2 = np.array(img)
    minPixelValue = img2.min()
    maxPixelValue = img2.max()
    img3 = (((img2-minPixelValue)/(maxPixelValue-minPixelValue))*100)+100
    img4 = np.trunc(img3)
    #img4 = np.uint8(img3)
    imgOut = img4.astype(int)    
    imwrite('IntensityOutputs/new_intensity2_' + imgName, imgOut)



def main(argv):
    intervaloIntensidade(argv)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python intervalo100200.py pathImagem")
from cv2 import imwrite, imread
import numpy as np
import sys
import cv2

def mosaico(pathFileName):
    # a imagem obrigatoriamente deve ter 512x512 de tamanho para que o codigo funcione
    img = imread(pathFileName, 0)
    img1 = img[0:128,0:128]
    img2 = img[0:128,128:256]
    img3 = img[0:128,256:384]
    img4 = img[0:128,384:512]
    img5 = img[128:256,0:128]
    img6 = img[128:256,128:256]
    img7 = img[128:256,256:384]
    img8 = img[128:256,384:512]
    img9 = img[256:384,0:128]
    img10 = img[256:384,128:256]
    img11 = img[256:384,256:384]
    img12 = img[256:384,384:512]
    img13 = img[384:512,0:128]
    img14 = img[384:512,128:256]
    img15 = img[384:512,256:384]
    img16 = img[384:512,384:512]
    output1 = cv2.hconcat([img6, img11, img13, img3])
    output2 = cv2.hconcat([img8, img16, img1, img9])
    output3 = cv2.hconcat([img12, img14, img2, img7])
    output4 = cv2.hconcat([img4, img15, img10, img5])
    output = cv2.vconcat([output1,output2,output3,output4])
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('MosaicOutputs/mosaic_' + imgName , output)


def main(argv1):
    mosaico(argv1)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python mosaico.py pathImagem")
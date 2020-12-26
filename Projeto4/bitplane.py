from cv2 import imwrite, imread, IMREAD_COLOR
import numpy as np
import argparse

# Esteganografada
# python bitplane.py ./Outputs\baboon_0.png 0 red
# Original
# python bitplane.py ./ColorImgs\baboon.png 0 blue
# ainda nao entendi muito bem como comparar, mas praticamente ja podemos iniciar o relatorio 

def bit_plane_extract(pathFileName, order, color):
    img = imread(pathFileName, IMREAD_COLOR)
    # img >> ordem faz shift right nos bits de um pixel da imagem
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (str(color) == 'blue'):
                img[i][j][0] = ((img[i][j][0].astype(np.uint8) >> int(order)) % 2)*255
                img[i][j][1] = 0
                img[i][j][2] = 0
            elif(str(color) == 'green'):
                img[i][j][1] = ((img[i][j][1].astype(np.uint8) >> int(order)) % 2)*255
                img[i][j][0] = 0
                img[i][j][2] = 0
            elif(str(color) == 'red'):
                img[i][j][2] = ((img[i][j][2].astype(np.uint8) >> int(order)) % 2)*255
                img[i][j][0] = 0
                img[i][j][1] = 0         

    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('Outputs/plano_bits_ordem_' + order + '_color_' + color + '_' + imgName, img)


def main():
    parser = argparse.ArgumentParser(description='Extrair plano de bits')
    parser.add_argument('img_path')
    parser.add_argument('bit_plane')
    parser.add_argument('band')

    args = parser.parse_args()
    bit_plane_extract(args.img_path, args.bit_plane, args.band)

if __name__ == '__main__':
    main()
   
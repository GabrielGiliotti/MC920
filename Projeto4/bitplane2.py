from cv2 import imwrite, imread, IMREAD_COLOR
import numpy as np
import argparse

def bit_plane_extract(pathFileName, order):
    img = imread(pathFileName, IMREAD_COLOR)
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    img2 = img.copy()
    img3 = img.copy()

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j][0] = ((img[i][j][0].astype(np.uint8) >> int(order)) % 2)*255
            img[i][j][1] = 0
            img[i][j][2] = 0
         
    imwrite('Outputs/plano_bits_'+ order +'_blue_' + imgName, img)

    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            img2[i][j][0] = 0
            img2[i][j][1] = ((img2[i][j][1].astype(np.uint8) >> int(order)) % 2)*255
            img2[i][j][2] = 0  

    imwrite('Outputs/plano_bits_'+ order +'_green_' + imgName, img2)

    for i in range(img3.shape[0]):
        for j in range(img3.shape[1]):
            img3[i][j][0] = 0
            img3[i][j][1] = 0
            img3[i][j][2] = ((img3[i][j][2].astype(np.uint8) >> int(order)) % 2)*255
         
    imwrite('Outputs/plano_bits_'+ order +'_red_' + imgName, img3)


def main():
    parser = argparse.ArgumentParser(description='Extrair plano de bits')
    parser.add_argument('img_path')
    parser.add_argument('bit_plane')

    args = parser.parse_args()
    bit_plane_extract(args.img_path, args.bit_plane)

if __name__ == '__main__':
    main()
   
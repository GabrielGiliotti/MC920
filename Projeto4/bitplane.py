from cv2 import imwrite, imread, IMREAD_COLOR
import numpy as np
import argparse

def bit_plane_extract(pathFileName, order):
    img = imread(pathFileName, IMREAD_COLOR)
    # img >> ordem faz shift right nos bits de um pixel da imagem
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j][0] = ((img[i][j][0].astype(np.uint8) >> int(order)) % 2)*255
            img[i][j][1] = ((img[i][j][1].astype(np.uint8) >> int(order)) % 2)*255
            img[i][j][2] = ((img[i][j][2].astype(np.uint8) >> int(order)) % 2)*255
            # Para gerar plano de bits somente na cor Blue, comente o codigo acima e descomente as 3 linhas abaixo desse comentario
            #img[i][j][0] = ((img[i][j][0].astype(np.uint8) >> int(order)) % 2)*255
            #img[i][j][1] = 0
            #img[i][j][2] = 0
            # Para gerar plano de bits somente na cor Green, comente o codigo acima e descomente as 3 linhas abaixo desse comentario
            #img[i][j][0] = 0
            #img[i][j][1] = ((img[i][j][1].astype(np.uint8) >> int(order)) % 2)*255
            #img[i][j][2] = 0
            # Para gerar plano de bits somente na cor Red, comente o codigo acima e descomente as 3 linhas abaixo desse comentario
            #img[i][j][0] = 0
            #img[i][j][1] = 0
            #img[i][j][2] = ((img[i][j][2].astype(np.uint8) >> int(order)) % 2)*255
         
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    imwrite('Outputs/plano_bits_ordem_' + order + '_' + imgName, img)


def main():
    parser = argparse.ArgumentParser(description='Extrair plano de bits')
    parser.add_argument('img_path')
    parser.add_argument('bit_plane')

    args = parser.parse_args()
    bit_plane_extract(args.img_path, args.bit_plane)

if __name__ == '__main__':
    main()
   
from cv2 import imwrite, imread, IMREAD_COLOR
import numpy as np
import cv2 as cv
import argparse

# python codificar.py ./ColorImgs\baboon.png ./ColorImgs\text.txt 0 baboon_0
def main():
    parser = argparse.ArgumentParser(description='Codificador')
    parser.add_argument('path_imagem_entrada')
    parser.add_argument('path_texto_entrada')
    parser.add_argument('plano_bits')
    parser.add_argument('imagem_saida')

    args = parser.parse_args()
    img = cv.imread(args.path_imagem_entrada, IMREAD_COLOR)

    message = getBinaryMessageFromTxtFile(args.path_texto_entrada)
    # Cada pixel tem 3 bandas de cores onde cada uma tem valor entre 0 e 255 --> 8 bits por banda em 1 pixel
    # logo sao 24 bits por pixel (ou 3 Bytes).  
    if(int(args.plano_bits) > 2 or int(args.plano_bits) < 0):
        print("O Plano de Bits especificado pode alterar drasticamente a imagem. Escolha um plano entre 0 e 2.")
        return
    # Plano de bits deve ser aceitavel
    #print(img[0][0])
    bites_img = img.shape[0] * img.shape[1] * 24
    if (len(message) < bites_img):
        encoded_img = hideMessage(img, message, int(args.plano_bits))
        #print(encoded_img[0][0])
        save_img(encoded_img, "Outputs", args.imagem_saida)
    else:
        print("A Imagem não comporta a mensagem. Escolha uma imagem maior ou uma mensagem menor.")
 

def getBinaryMessageFromTxtFile(path_message):
    text = open(path_message, "r")
    # Estou marcando o inicio e o fim da messagem com ~
    message = "~"
    for c in text:
        message += c
    message +="~"
    return ''.join([format(ord(i),"08b") for i in message])


def hideMessage(img, message, pb):
    msg_index = 0
    msg_len = len(message)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # pegando cada valor de r, g, b e transformando em binario para esconder a msg
            r,g,b = transformPixelsToBinary(img[i][j])
            if (msg_index < msg_len): 
                ini = r[:-pb-1]
                end = r[8-pb:]
                middle = message[msg_index]
                newBinary = ini + middle + end
                img[i][j][0] = int(newBinary, 2)
                msg_index += 1
            if (msg_index <  msg_len):
                ini = g[:-pb-1]
                end = g[8-pb:]
                middle = message[msg_index]
                newBinary = ini + middle + end
                img[i][j][1] = int(newBinary, 2)
                msg_index += 1
            if (msg_index <  msg_len):
                ini = b[:-pb-1]
                end = b[8-pb:]
                middle = message[msg_index]
                newBinary = ini + middle + end
                img[i][j][2] = int(newBinary, 2)
                msg_index += 1
            else:
                break
    return img

# Um unico pixel tem 24 bits ou 3 bytes (8 para r, 8 para g, 8 para b)
def transformPixelsToBinary(pixel):
    return [format(i, "08b") for i in pixel]


def save_img(img, folder, output_img_name):
    name = output_img_name.lower()
    if(".png" not in name):
        name += ".png"
    imwrite(folder +"/"+ name, img)

if __name__ == '__main__':
    main()
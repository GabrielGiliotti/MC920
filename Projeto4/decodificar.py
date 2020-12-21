from cv2 import imwrite, imread, IMREAD_COLOR
import numpy as np
import cv2 as cv
import argparse

# python decodificar.py ./Outputs\baboon_0.png 0 txtdecoded
def main():
    parser = argparse.ArgumentParser(description='Decodificador')
    parser.add_argument('path_img_to_decode')
    parser.add_argument('plano_bits')
    parser.add_argument('text_file_name')

    args = parser.parse_args()
    img = cv.imread(args.path_img_to_decode, IMREAD_COLOR)
    if( int(args.plano_bits) < 0 or  int(args.plano_bits) > 2):
        print("Nao é possivel decodificar o plano de bits especificado. Escolha valores entre 0 e 2.")
        return
    decodeMessage(img, args.plano_bits, args.text_file_name)


def decodeMessage(encoded_img, bp, out_file_name):
    b_text = ""
    for i in range(encoded_img.shape[0]):
        for j in range(encoded_img.shape[1]):
            r, g, b = transformPixelsToBinary(encoded_img[i][j])
            # Extrai todos os bits do plano especificado na entrada
            b_text += r[-1-int(bp)]
            b_text += g[-1-int(bp)]
            b_text += b[-1-int(bp)]
    # Separa os bits do plano em cadeias de 8 Ex: 0101100100101011 --> 01011001 00101011 (8 bits = 1 byte)
    m_bytes = [ b_text[i: i+8] for i in range(0, len(b_text),8)]
    decoded_message = convertBytesToChar(m_bytes)
    save_txt(decoded_message, "Outputs", out_file_name)



# Transforma os bytes na mensagem original
def convertBytesToChar(m_bytes):
    message = ""
    count = 0
    for byte in m_bytes:
        message += chr(int(byte,2))
        if(message[-1] == "~"):
            count += 1
        if(message[-1] == "~" and count == 2):
            break
    # Retorna mensagem sem os delimitadores do texto
    return message[1:len(message)-1]
    

# Um unico pixel tem 24 bits ou 3 bytes (8 para r, 8 para g, 8 para b)
def transformPixelsToBinary(pixel):
    return [format(i, "08b") for i in pixel]


def save_txt(message, folder, output_text_name):
    name = output_text_name.lower()
    if(".txt" not in name):
        name += ".txt"
    f = open(folder + "/" + name,"w+")
    f.write(message)
    f.close()


if __name__ == '__main__':
    main()

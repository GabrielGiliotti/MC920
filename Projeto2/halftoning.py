import cv2 as cv
from numpy import newaxis
import numpy as np
import sys

floyd_steinberg_filter = 1/16*np.array([[0,0,7],
                                        [3,5,1]])


def slide_filter(image, kernel, sub_factor, band):
    lista=[] # lista de saida que se tornara a nova imagem g(x,y)
    kernel_rows = len(kernel)
    kernel_columns = len(kernel[0]) # preciso das dimensoes (numero de linhas e colunas) do kernel para aplicar os filtros corretamente

    rows = len(image)
    columns = len(image[0])

    for i in range(0,rows-sub_factor):
        for j in range(1,columns-sub_factor):            
            # image[i][j][b/g/r] eh o valor f(x,y) da mascara. Colocando o pixel f(x,y) no kernel para completar a mascara
            last_value = -1
            if(image[i][j][band] < 128):
                lista.append(0)
                #image[i][j][band] = 0
                last_value = 0
            else:
                lista.append(1)
                #image[i][j][band] = 255
                last_value = 1
            # Calculamos o erro para fazer a propagacao
            erro = image[i][j][band] - (last_value * 255)
            # pro dado recorte da iteracao corrente, fazemos com que os valores do recorte sejam acrescidos de kernel*erro
            image[i:i+kernel_rows, j-sub_factor:j+kernel_columns-sub_factor,band] = image[i:i+kernel_rows, j-sub_factor:j+kernel_columns-sub_factor,band] + (kernel*erro)

    return image
    #return np.array(lista).reshape(512, 512)



def halftoning_alternado(imgPath, filtro):
    print("nada ainda")


def halftoning_direto(imgPath, filtro):
    # Leitura da Img
    img = cv.imread(imgPath).astype(np.uint8)

    # Separacao da Img orginal em BGR
    b,g,r = cv.split(img)
    k = np.zeros_like(b)
    b = cv.merge([b,k,k])
    g = cv.merge([k,g,k])
    r = cv.merge([k,k,r])


    if(filtro == "Floyd_Steinberg"):
        # top, bottom, left, right
        # Acrescentando bordas para nas imagens BGR para aplicar filtro
        for i in range(0,3): 
            img_border = cv.copyMakeBorder(img, 0, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
            img_masked = slide_filter(img_border, floyd_steinberg_filter, 1, i)
        
        b_img_border = cv.copyMakeBorder(b, 0, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        b_img_masked = slide_filter(b_img_border, floyd_steinberg_filter, 1, 0)
        g_img_border = cv.copyMakeBorder(g, 0, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        g_img_masked = slide_filter(g_img_border, floyd_steinberg_filter, 1, 1)
        r_img_border = cv.copyMakeBorder(r, 0, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        r_img_masked = slide_filter(r_img_border, floyd_steinberg_filter, 1, 2)


    elif(filtro == "Stevenson_Arce"):
        print("Stevenson_Arce escolhido")
    elif(filtro == "Burkes"):
        print("Burkes escolhido")
    elif(filtro == "Sierra"):
        print("Sierra escolhido")
    elif(filtro == "Stucki"):
        print("Stucki escolhido")
    elif(filtro == "Jarvis_Judice_Ninke"):
        print("Jarvis_Judice_Ninke escolhido")
    else:
        print("Filtro nao definido !")
        return
    # Aplicar os filtros para cada espectro

    # Algoritmo na aula 13, por volta do minuto 50
    # No proprio algoritmo, eh calculado o erro.
    # Apos calculado o erro, aplicamos a mascara multiplicada pelo erro 
    # Aplicamos as mascaras em cada espectro
    
    # finalemnte unimos os espctros em uma imagem de saida 
    # OBS: Percorrer a imagem em 2 orientacoes
    # Na ida mascara vai no sentido normal, na volta, flipar a mascara

    # Saida imgs
    index = imgPath.rfind("\\")
    imgName = imgPath[index+1:]
    cv.imwrite("Outputs/"+ imgName +"_blue.png", b_img_masked) 
    cv.imwrite("Outputs/"+ imgName +"_green.png",g_img_masked) 
    cv.imwrite("Outputs/"+ imgName +"_red.png", r_img_masked) 
    cv.imwrite("Outputs/"+ imgName +"_merged.png", img_masked)


def main(argv1, argv2, argv3):
    if(argv3 == "Direto"):
        halftoning_direto(argv1, argv2)
    elif(argv3 == "Alternado"):
        halftoning_alternado(argv1, argv2)
    else:
        print("Percurso inexistente ! Execute novamente definindo o tipo de percurso.")


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python halftoning.py pathImagem filtro percurso")
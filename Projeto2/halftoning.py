import cv2 as cv
from cv2 import IMREAD_COLOR, BORDER_CONSTANT
from math import floor
from numpy import newaxis
import numpy as np
import sys
import time

floyd_steinberg_filter = 1/16*np.array([[0,0,7],
                                        [3,5,1]])

stevenson_arce_filter = 1/200*np.array([[0,0,0,0,0,32,0],
                                        [12,0,26,0,30,0,16],
                                        [0,12,0,26,0,12,0],
                                        [5,0,12,0,12,0,5]])

burkes_filter = 1/32*np.array([[0,0,0,8,4],
                               [2,4,8,4,2]])
                        
sierra_filter = 1/32*np.array([[0,0,0,5,3],
                               [2,4,5,4,2],
                               [0,2,3,2,0]])

stucki_filter = 1/42*np.array([[0,0,0,8,4],
                               [2,4,8,4,2],
                               [1,2,4,2,1]])

jarvis_judice_ninke_filter = 1/48*np.array([[0,0,0,7,5],
                                            [3,5,7,5,3],
                                            [1,3,5,3,1]])

def slide_filter(image, kernel):

    # column_x eh o numero de colunas com valor 0 que devemos adicionar nas laterais da imagem para aplicar os filtros 
    column_x = floor(kernel.shape[1]/2)
    # row_y eh o numero de linhas com valor 0 que devemos adicionar na base da imagem.
    # Para esse projeto nao eh necessario inserir linha no topo da imagem
    row_y = kernel.shape[0] - 1 
   
    image = cv.copyMakeBorder(image, top=0, bottom=row_y, left=column_x, right=column_x, borderType=BORDER_CONSTANT, value=0)
    image = image.astype(float, copy=False)
    
    # X e Y sao os valores maximos do range que vamos percorrer na imagem de entrada com bordas
    X = image.shape[1] - column_x
    Y = image.shape[0] - row_y
    
    # img_out sera a imagem que recebera valores de saida
    img_out = np.zeros((image.shape[0],image.shape[1]))

    for j in range(Y):      
        for i in range(column_x, X):
            # Pegamos o maximo valor entre 0 e pixel corrente pois existem pixels com valores negativos
            image[j,i] = max(0,image[j,i])
            # Fazendo a divisao por 128, estamos separando os pixels com valores entre (0.,1.99)
            # Fazendo floor, definimos se o valor sera 0 ou 255 (ou seja, 0 ou 1)
            img_out[j,i] = 255 * floor(image[j,i]/128)
            # Erro eh a diferenca de valor entre imagem original e imagem de saida
            erro = image[j,i] - img_out[j,i]
            # Pegamos o slice com as mesmas dimensoes do kernel
            img_slice = image[j:j+row_y+1, i-column_x:i+column_x+1]
            # Propagamos o erro para pedaco corrente da imagem
            img_slice += (kernel*erro)
    
    # Removendo as bordas com valor 0 da imagem de saida
    img_out = img_out[:Y,column_x:X]
    # Retorna cada banda BGR
    return img_out   


def slide_filter_alternado(image, kernel):

    # column_x eh o numero de colunas com valor 0 que devemos adicionar nas laterais da imagem para aplicar os filtros 
    column_x = floor(kernel.shape[1]/2)
    # row_y eh o numero de linhas com valor 0 que devemos adicionar na base da imagem.
    # Para esse projeto nao eh necessario inserir linha no topo da imagem
    row_y = kernel.shape[0] - 1 
    # Armazenamos uma copia flipada do kernel para aplicar nas iteracoes alternadas
    fliped_kernel = np.fliplr(kernel)
   
    image = cv.copyMakeBorder(image, top=0, bottom=row_y, left=column_x, right=column_x, borderType=BORDER_CONSTANT, value=0)
    image = image.astype(float, copy=False)
    
    # X e Y sao os valores maximos do range que vamos percorrer na imagem de entrada com bordas
    X = image.shape[1] - column_x
    Y = image.shape[0] - row_y
    
    # img_out sera a imagem que recebera valores de saida
    img_out = np.zeros((image.shape[0],image.shape[1]))

    for j in range(Y): 
        
        # Reverse if odd indexed line
        reverse = (j % 2 == 1)
        current_kernel = fliped_kernel if reverse else kernel     
        
        for i in range(column_x, X)[::-1 if reverse else 1]:
            image[j,i] = max(0,image[j,i])
            img_out[j,i] = 255 * floor(image[j,i]/128)
            # Calculos de difusao do Erro
            erro = image[j,i] - img_out[j,i]
            img_slice = image[j:j+row_y+1, i-column_x:i+column_x+1]
            img_slice += (kernel*erro)
    
    # Removendo as bordas com valor 0 da imagem de saida
    img_out = img_out[:Y,column_x:X]
    # Retorna cada banda BGR
    return img_out   



def halftoning_alternado(imgPath, filtro):
    # Leitura da Img
    img = cv.imread(imgPath, IMREAD_COLOR)
    img = img.astype(float, copy=False)

    if(filtro == "Floyd_Steinberg"):
        # para cada Banda BGR da imagem, aplicamos o filtro
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter_alternado(img[:,:,i], floyd_steinberg_filter)        

    elif(filtro == "Stevenson_Arce"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter_alternado(img[:,:,i], stevenson_arce_filter)

    elif(filtro == "Burkes"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter_alternado(img[:,:,i], burkes_filter)

    elif(filtro == "Sierra"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter_alternado(img[:,:,i], sierra_filter)

    elif(filtro == "Stucki"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter_alternado(img[:,:,i], stucki_filter)    
    
    elif(filtro == "Jarvis_Judice_Ninke"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter_alternado(img[:,:,i], jarvis_judice_ninke_filter) 
    else:
        print("Filtro nao definido ou inexistente !")
        return

    index = imgPath.rfind("\\")
    imgName = imgPath[index+1:]
    print("--- %s seconds ---" % (time.time() - start_time))
    cv.imwrite("Outputs/Alternate_" + filtro + "_" + imgName, img)


def halftoning_direto(imgPath, filtro):
    # Leitura da Img
    img = cv.imread(imgPath, IMREAD_COLOR)
    img = img.astype(float, copy=False)

    if(filtro == "Floyd_Steinberg"):
        # para cada Banda BGR da imagem, aplicamos o filtro
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter(img[:,:,i], floyd_steinberg_filter)        

    elif(filtro == "Stevenson_Arce"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter(img[:,:,i], stevenson_arce_filter)

    elif(filtro == "Burkes"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter(img[:,:,i], burkes_filter)

    elif(filtro == "Sierra"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter(img[:,:,i], sierra_filter)

    elif(filtro == "Stucki"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter(img[:,:,i], stucki_filter)    
    
    elif(filtro == "Jarvis_Judice_Ninke"):
        for i in range(img.shape[2]):
            img[:,:,i] = slide_filter(img[:,:,i], jarvis_judice_ninke_filter) 
    else:
        print("Filtro nao definido ou inexistente !")
        return
   
    # Saida imgs
    index = imgPath.rfind("\\")
    imgName = imgPath[index+1:]
    print("--- %s seconds ---" % (time.time() - start_time))
    cv.imwrite("Outputs/" + filtro + "_" + imgName, img)


def main(argv1, argv2, argv3):
    if(argv3 == "Direto"):
        halftoning_direto(argv1, argv2)
    elif(argv3 == "Alternado"):
        halftoning_alternado(argv1, argv2)
    else:
        print("Percurso inexistente ! Execute novamente definindo o tipo de percurso.")


if __name__ == '__main__':
    try:
        start_time = time.time()
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Path da imagem nao definido !")
        print("Execute: ", end="")
        print("python halftoning.py pathImagem filtro percurso")
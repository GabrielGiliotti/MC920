from cv2 import imwrite, imread
import cv2 as cv
import numpy as np
import sys
import time

start_time = time.time()

def slide_filter(image, kernel, sub_factor):
    lista=[]
    for i in range(0,len(image)-sub_factor):
        for j in range(0,len(image)-sub_factor):
            result = image[i:len(kernel)+i,j:len(kernel)+j]*kernel    # img[1:4,0:3]*kernel -- matrix[column, row]
            lista.append(np.sum(result))
    return np.array(lista).reshape(512, 512)
    

def normalize(image_masked):
    minValue = image_masked.min()
    maxValue = image_masked.max()
    img_normalized = (((image_masked-minValue)/(maxValue-minValue))*255)
    img_trunc = np.trunc(img_normalized)
    output = img_trunc.astype(int)
    return output



def filtros(pathFileName, filtro):
    if(filtro == 'h1'):
        img = imread(pathFileName, 0) # Leitura img, no caso de exemplo minha img era 4x4
        maskh1 = np.array([[0,0,-1,0,0],   # mascara, nesse caso é 5x5 
                           [0,-1,-2,-1,0],
                           [-1,-2,16,-2,-1],
                           [0,-1,-2,-1,0],
                           [0,0,-1,0,0]])
 
        # top, bottom, left, right tem valor 2 pois a mascara é 5x5, logo o pixel central fica
        # a uma distancia de 2 unidades das bordas da mascara
        img_border = cv.copyMakeBorder(img, 2, 2, 2, 2, cv.BORDER_CONSTANT, None, 0)
        # metodo criado para aplicar a mascara em cada pixel (nao eh o modo mais eficiente, mas foi o que deu pra fazer kk)
        img_masked = slide_filter(img_border, maskh1, 4)
        # Existem pixels fora do intervalo [0,255], entao normalizamos antes de dar a saida
        output = normalize(img_masked)
        # Para obter o filtro aplicado sem a normalização dos valores dos pixels, comente img_masked e output acima
        # e descomente a linha logo a baixo
        #output = slide_filter(img_border, maskh1, 4)

    elif(filtro == 'h2'):
        img = imread(pathFileName, 0)
        maskh2 = np.array([[1,4,6,4,1],
                           [4,16,24,16,4],
                           [6,24,36,24,6],
                           [4,16,24,16,4],
                           [1,4,6,4,1]])/256

        # Aqui nao precisamos normalizar por causa dos valores da mascara aplicada
        img_border = cv.copyMakeBorder(img, 2, 2, 2, 2, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh2, 4)
        img_trunc = np.trunc(img_masked)
        output = img_trunc.astype(int)

    elif(filtro == 'h3'):
        img = imread(pathFileName, 0)
        maskh3 = np.array([[-1,0,1],
                           [-2,0,2],
                           [-1,0,1]])
        # top, bottom, left, right tem valor 1 pois a mascara é 3x3, logo o pixel central fica
        # a uma distancia de 1 unidade das bordas da mascara
        img_border = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh3, 2)
        output = normalize(img_masked)
        # Para obter o filtro aplicado sem a normalização dos valores dos pixels, comente img_masked e output acima
        # e descomente a linha logo a baixo
        #output = slide_filter(img_border, maskh3, 2)

    elif(filtro == 'h4'):
        img = imread(pathFileName, 0)
        maskh4 = np.array([[-1,-2,-1],
                           [0,0,0],
                           [1,2,1]])
        img_border = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh4, 2)
        output = normalize(img_masked)
        # Para obter o filtro aplicado sem a normalização dos valores dos pixels, comente img_masked e output acima
        # e descomente a linha logo a baixo
        #output = slide_filter(img_border, maskh4, 2)
   
    elif(filtro == 'h5'):
        img = imread(pathFileName, 0)
        maskh5 = np.array([[-1,-1,-1],
                           [-1,8,-1],
                           [-1,-1,-1]])
        
        img_border = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh5, 2)
        output = normalize(img_masked)
        # Para obter o filtro aplicado sem a normalização dos valores dos pixels, comente img_masked e output acima
        # e descomente a linha logo a baixo
        #output = slide_filter(img_border, maskh5, 2)

    elif(filtro == 'h6'):
        img = imread(pathFileName, 0)
        maskh6 = np.array([[1,1,1],
                           [1,1,1],
                           [1,1,1]])/9
        
        img_border = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh6, 2)
        img_trunc = np.trunc(img_masked)
        output = img_trunc.astype(int)

    elif(filtro == 'h7'):
        img = imread(pathFileName, 0)
        maskh7 = np.array([[-1,-1,2],
                           [-1,2,-1],
                           [2,-1,-1]])
        
        img_border = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh7, 2)
        output = normalize(img_masked)

    elif(filtro == 'h8'):
        img = imread(pathFileName, 0)
        maskh8 = np.array([[2,-1,-1],
                           [-1,2,-1],
                           [-1,-1,2]])
        img_border = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh8, 2)
        output = normalize(img_masked)

    elif(filtro == 'h9'):
        img = imread(pathFileName, 0)
        maskh9 = np.array([[1,0,0,0,0,0,0,0,0],
                           [0,1,0,0,0,0,0,0,0],
                           [0,0,1,0,0,0,0,0,0],
                           [0,0,0,1,0,0,0,0,0],
                           [0,0,0,0,1,0,0,0,0],
                           [0,0,0,0,0,1,0,0,0],
                           [0,0,0,0,0,0,1,0,0],
                           [0,0,0,0,0,0,0,1,0],
                           [0,0,0,0,0,0,0,0,1]])/9
        
        img_border = cv.copyMakeBorder(img, 4, 4, 4, 4, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh9, 8)
        img_trunc = np.trunc(img_masked)
        output = img_trunc.astype(int)

    elif(filtro == 'h10'):
        img = imread(pathFileName, 0)
        maskh10 = np.array([[-1,-1,-1,-1,-1],
                            [-1,2,2,2,-1],
                            [-1,2,8,2,-1],
                            [-1,2,2,2,-1],
                            [-1,-1,-1,-1,-1]])/8
                     
        img_border = cv.copyMakeBorder(img, 2, 2, 2, 2, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh10, 4)
        output = normalize(img_masked)

    elif(filtro == 'h11'):
        img = imread(pathFileName, 0)
        maskh11 = np.array([[-1,-1,0],
                            [-1,0,1],
                            [0,1,1]])
        
        img_border = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked = slide_filter(img_border, maskh11, 2)
        output = normalize(img_masked)

    elif(filtro == 'h3h4'):
        img = imread(pathFileName, 0)
        maskh3 = np.array([[-1,0,1],
                           [-2,0,2],
                           [-1,0,1]])

        maskh4 = np.array([[-1,-2,-1],
                           [0,0,0],
                           [1,2,1]])

        img_border_h3 = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_border_h4 = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)
        img_masked_h3 = slide_filter(img_border_h3, maskh3, 2)
        img_masked_h4 = slide_filter(img_border_h4, maskh4, 2)
        output3 = normalize(img_masked_h3)
        output4 = normalize(img_masked_h4)
        output_sum = np.sqrt([sum(x) for x in zip(np.square(output3), np.square(output4))]).astype(int)
        output = normalize(output_sum)
    
    index = pathFileName.rfind("\\")
    imgName = pathFileName[index+1:]
    print("--- %s seconds ---" % (time.time() - start_time))
    imwrite('FilterOutputs/filter_' + filtro + '_' + imgName, output)


def main(argv1, argv2):
    filtros(argv1, argv2)



if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        print("Path da imagem ou tipo de filtro nao definido !")
        print("Execute: ", end="")
        print("python filtros.py pathImagem tipoFiltro")
from cv2 import imwrite, imread, imshow, waitKey, destroyAllWindows, IMREAD_GRAYSCALE
from os.path import join, basename, splitext
from math import exp
import numpy as np
import matplotlib.pyplot as plt
import argparse

def main():
    # Definicao de argumentos para aplicacao das mascaras
    parser = argparse.ArgumentParser(description='Algoritmo de aplicacao de limiarizacao global ou local em uma imagem')
    parser.add_argument('imgPath', help='path completo para o arquivo (.pgm)')
    parser.add_argument('methodName', help='Nome de um metodo de limiarizacao escolhido: global, bernsen, niblack, sauvola, more, contrast, mean, median')
    parser.add_argument('--thresh', help='Valor que pode ser definido para limiarizacao global. Usado como default valor 128', default=128, type=int)
    parser.add_argument('--size', help='Tamanho da janela para limiarizacao local (default eh 5, para uma janela 5x5).', default=5, type=int)
    parser.add_argument('--k', help='Valor que pode ser definido para o parametro "k". Valor default 0.25', default=0.25, type=float)
    parser.add_argument('--r', help='Valor que pode ser definido para o parametro "r". Valor default 0.5', default=11, type=float)
    parser.add_argument('--p', help='Valor que pode ser definido para o parametro "p". Valor default 2', default=2, type=float)
    parser.add_argument('--q', help='Valor que pode ser definido para o parametro "q". Valor default 10.', default=10, type=float)
    
    args = parser.parse_args()
    # leitura e copia da imagem
    img = imread(args.imgPath, IMREAD_GRAYSCALE)
    inputImg = img.copy()

    if(args.methodName == "global"):
        img = global_thresholding(img, args.thresh)
        # argumentos: img de saida, img original, salvar histograma, nome da img, pasta de saida
        histograma(img, inputImg, "global_"+basename(args.imgPath), "Outputs")
        salvar_imagem(img, args.imgPath, "global", "Outputs")
    else:
        # argumentos: img de saida, metodo utilizado, tamanho janela, valor k, valor r, valor p, valor q
        img = local_thresholding(img, args.methodName, args.size, args.k, args.r, args.p, args.q)
        # argumentos: img de saida, img original, salvar histograma, nome da img, pasta de saida
        histograma(img, inputImg, "local_"+ args.methodName +"_"+basename(args.imgPath), "Outputs")
        salvar_imagem(img, args.imgPath, "local_"+ args.methodName, "Outputs")

    # Retorna proporcoes de pixels pretos para imagem de saida
    qtd_pixels = img.size
    pixels_brancos = np.count_nonzero(img)
    pixels_pretos = qtd_pixels - pixels_brancos
    print()
    print("Fracao de pixels pretos: ", pixels_pretos/qtd_pixels)


# Global: valor fixado em 128
def global_thresholding(img, threshold_number):
    return np.uint8(np.where(img > threshold_number, 255, 0))


def local_thresholding(img, methodName, size, k, r, p, q):
    # mat_thresh eh a imagem de saida que recebera os valores da aplicacao dos metodos
    # na janela_metodo_local. mat_thresh inicialmente eh toda zerada
    mat_thresh = np.zeros(img.shape)
    # delta serve para ajustar as dimensoes da janela de aplicacao dos metodos locais
    delta = size//2
    
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            janela_metodo_local = img[max(0, y-delta) : min(y+delta+1, img.shape[0]),
                                      max(0, x-delta) : min(x+delta+1, img.shape[1])]
            
            # escolha para o metodo definido no parametro da execucao
            if(methodName == "bernsen"):
                mat_thresh[y,x] = metodo_bernsen(janela_metodo_local, k, r, p, q)
            elif(methodName == "niblack"):
                mat_thresh[y,x] = metodo_niblack(janela_metodo_local, k, r, p, q)
            elif(methodName == "sauvola"):
                mat_thresh[y,x] = metodo_sauvola_pietaksinen(janela_metodo_local, k, r, p, q)
            elif(methodName == "more"):
                mat_thresh[y,x] = metodo_phansalskar_more_sabale(janela_metodo_local, k, r, p, q)
            elif(methodName == "contrast"):
                mat_thresh[y,x] = metodo_contraste(janela_metodo_local, k, r, p, q)
            elif(methodName == "mean"):
                mat_thresh[y,x] = metodo_media(janela_metodo_local, k, r, p, q)
            elif(methodName == "median"):
                mat_thresh[y,x] = metodo_mediana(janela_metodo_local, k, r, p, q)
            else:
                print("Metodo nao encontrado !")
                # Se o metodo nao for encontrado, a imagem retornada eh um pixel preto 
                # e ainda sim um histograma da imagem deentrada eh gerado
                return mat_thresh[y,x]
    
    img = np.uint8(np.where(img >= mat_thresh, 255, 0))
    return img
  

# Metodo Local de thresholding: (zmax + zmin)/2 
def metodo_bernsen(win, *_):
    return (np.amax(win) - np.amin(win))/2

# Metodo Local de thresholding: mean + k*stdev
# Metodo estatistico onde k eh um parametro de ajuste.
def metodo_niblack(win, k, *_):
    return np.mean(win) + k*np.std(win)

# Metodo Local de thresholding projetado sobre Niblack, para imagens com iluminacao ruim.
# k=0.5 e r=128 sugeridos
def metodo_sauvola_pietaksinen(win, k, r, *_):
    return np.mean(win) * (1 + k*(np.std(win)/r - 1))

# Metodo Local de thresholding projetado sobre Sauvola e Pietaksinen, para imagens de baixo contraste.
# k=0.25, r=0.5, p=2 and q=10 sao valores sugeridos.
def metodo_phansalskar_more_sabale(win, k, r, p, q):
    mean = np.mean(win)
    return mean * (1 + p * exp(-1*q*mean) + k * (np.std(win)/r - 1))

# Metodo Local de thresholding para checagem de contraste.
def metodo_contraste(win, *_):
    shape = win.shape
    pixel = win[shape[0]//2, shape[1]//2]
    if(abs(int(pixel)-int(np.amax(win))) < abs(int(pixel)-int(np.amin(win)))):
        return 0
    else: 
        return 255

# Metodo Local de thresholding: mean
def metodo_media(win, *_):
    return np.mean(win)

# Metodo Local de thresholding: median
def metodo_mediana(win, *_):
    return np.median(win)

def histograma(img, inputImg, name='image', folder='Outputs'):
    # Plot do histograma imagem original.
    plt.hist(inputImg, bins='auto')
    plt.title("Histograma " + name + " Input")
    plt.xlim(0,255)
    plt.xlabel("Niveis de Cinza")
    plt.ylabel("Quantidade de Pixels")

    # Salva histograma da img como um arquivo de saida .png
    hist_part_name,_ = splitext(name)
    name = "histograma_" + hist_part_name + '.png'
    path = join(folder,name)
    plt.savefig(path)
    
def salvar_imagem(img, path, method, folder):
    name = method.lower() + '_' + basename(path)
    # Se desejar a saida em .pgm, comente a duas linhas indicadas a seguir
    name = name[:-4] # comente aqui
    name = name + ".png" # comente aqui
    imwrite(join(folder, name), img)

if(__name__ == '__main__'):  
    main()
    
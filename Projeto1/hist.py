from cv2 import imwrite, imread
import cv2
import numpy as np 
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance

im = Image.open("C:\\Users\\Woodstock\\Desktop\\baboon_zoado.png")

enhancer = ImageEnhance.Contrast(im)

factor = 4
im_output = enhancer.enhance(factor)
im_output.save("test.png")

#img = imread('C:\\Users\\Woodstock\\Desktop\\baboon_zoado.png', 0)
#col, row = img.shape

#hist = np.bincount(img.ravel(), minlength=256)
#x = np.arange(0,256)
#plt.bar(x,hist,color="gray")
#plt.show()

# fazer equalizacao pra teste
# Total pixels
#total = col * row

# prob pra cada nivel
#prob = hist/total

# prob cumulativa pra cada nivel
#y = np.cumsum(prob)

# retornando para os valores originais
#origin = y*255
#output = [round(x) for x in origin]

#hist2 = np.bincount(output, minlength=256)
#x2 = np.arange(0,256)
#plt.bar(x2,hist2,color="red")
#plt.show()

#reshaped = np.reshape(np.array(output), (-1, 256))
#print(reshaped)
#imwrite('test.png', reshaped)
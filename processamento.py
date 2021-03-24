from PIL import Image
from PIL import ImageEnhance
import os
import numpy as np
import cv2 as cv
import load
import config


# ==============================================================================================================
# Funções que auxilião o melhoramento da imagem para extração de features
# ==============================================================================================================
def dilation(img):
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv.dilate(img, kernel, iterations=1)
    return dilation

def erosion(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv.erode(img, kernel)

def opening(img):
    kernel = np.ones((10, 10), np.uint8)
    edges_3 = cv.Canny(img, 10, 50)
    return cv.morphologyEx(edges_3, cv.MORPH_OPEN, kernel)

def closing(img):
    kernel = np.ones((15, 15), np.uint8)
    return cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

def grad(img):
    kernel = np.ones((15, 15), np.uint8)
    return cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)

def sobel(img):
    return cv.Sobel(img, -1, 1, 1)

def edges(img):
    return cv.Canny(img, 100, 200)



# Gerar um copia da imagens com alterações de resolução , brilho , constraste em escala de cinza
def preProcessFiles(arquivo):

    # Carregar imagem
    imgp = Image.open(arquivo)

    # Escala de sinza
    imgp = imgp.convert("L")

    # Melhorar o contraste
    contrast = ImageEnhance.Brightness(imgp)
    imgp = contrast.enhance(1)

    # Melhorar o Brilho
    brilho = ImageEnhance.Contrast(imgp)
    imgp = brilho.enhance(5)

    # padronizar tamanho da imagem
    imgp = imgp.resize((180,180), Image.ANTIALIAS)

    # Salvar imagem
    imgp.save(arquivo)


# Gerar um copia da imagens com alterações de resolução , brilho e constraste
def preProcessFiles2(arquivo):

        # Carregar imagem
        imgp = Image.open(arquivo)

        # Melhorar o contraste
        contrast = ImageEnhance.Brightness(imgp)
        imgp = contrast.enhance(1)

        # Melhorar o Brilho
        brilho = ImageEnhance.Contrast(imgp)
        imgp = brilho.enhance(5)

        # padronizar tamanho da imagem
        imgp = imgp.resize((180,180), Image.ANTIALIAS)

        # Salvar imagem
        imgp.save(arquivo)



# Gerar um copia da imagens apenas aumentando as dimensões
def preProcessFiles3(arquivo):

        # Carregar imagem
        imgp = Image.open(arquivo)

        # padronizar tamanho da imagem
        imgp = imgp.resize((180,180), Image.ANTIALIAS)

        # Salvar imagem
        imgp.save(arquivo)



#Remover arquivos
def removeFile(arquivo):
    if os.path.exists(arquivo):
        os.remove(arquivo)



#Verificar se ha aquivo com o mesmo nome e os retorna uma nova sugestão de nome
def tempFileName(item):
    # Gerar um array de duas posições [0] nome - [1] extensão
    extend = item.split(".")

    if os.path.exists(item):
        return extend[0]+"dupli."+extend[1]
    else:
        return item


#checar se o arquivo é valido
def checkFile(file):
    try:
        imgp = Image.open(file)
        return True
    except:
        removeFile(file)
        return False



# metodo que gerar aas imagens temporarias na escala de cinza e aumenta o brilho e contraste
def copyImage(arquivo, nom_Dirtemp, file):
        newFiles = []

        if checkFile(arquivo):

            imgp = Image.open(arquivo).convert('RGB')
            img = cv.imread(arquivo)
            # Extensao
            extend = file.split(".")

            # Camino + nome do arquivo processado
            destinos =[
                    tempFileName(nom_Dirtemp + "cinza_" + extend[0] + ".jpeg"),
                    tempFileName(nom_Dirtemp + "cinResize_" + extend[0] + ".jpeg"),
                    tempFileName(nom_Dirtemp + "Resizebrilho_" + extend[0] + ".jpeg"),
                    tempFileName(nom_Dirtemp + "Resize_" + extend[0] + ".jpeg")
                    ]

             # Remover arquivos  redundantes
            for caminho in destinos:
                removeFile(caminho)

            # Copiar a imagem para o diretorio
            i = 0
            while i < len(destinos):
                copy = imgp
                copy.save(destinos[i])
                i = i + 1

            # Gerar a imagen em diversas rotações
            rotacao = np.arange(15, 360, 15)

            for giro in rotacao:
                newName = nom_Dirtemp + "G_"+str(giro)+ extend[0] + ".jpeg"
                copy = imgp
                copy = copy.rotate(giro)
                copy.save(newName)
                destinos.append(newName)



            # Transferir arquivo para o diretorio
            imgp.save(nom_Dirtemp+file)

            # Gerar um imagen em escala de cinza
            if checkFile(destinos[0]) == True:
                preProcessFiles(destinos[0])

            # Gerar uma imagem na dimensão do modelo de deeplearning cinza
            if checkFile(destinos[1]) == True:
                preProcessFiles(destinos[1])

        # Gerar uma imagem na dimensão do modelo de deeplearning natural
            if checkFile(destinos[2]) == True:
                 preProcessFiles2(destinos[2])

        # Gerar uma imagem na dimensão do modelo de deeplearning natural
            if checkFile(destinos[3]) == True:
                 preProcessFiles3(destinos[3])

        # Gerar os filtros para a imagem original
            mtComb = [  dilation(img),
                    erosion(img),
                    opening(img),
                    closing(img),
                    grad(img),
                    sobel(img),
                    edges(img)
                ]
            x = 0

            for file in mtComb:
                 newName = nom_Dirtemp + "Copy"+str(x)+".jpeg"
                 cv.imwrite(newName, file)
                 destinos.append(newName)
                 x = x +1
        return destinos


# resetar o diretorio de imagens
def resetImagenDir():
    #carregar as subpastas
    diret = load.getSubPastas(config.dir_imagens)

    for i in diret:
        # gerar o caminho absoluto
        caminho = config.dir_imagens + i + "/"

        # carregar os arquivos do diretorio
        file = load.getFiles(caminho)

        for f in file:
            # Serar o nome por .
            n = f.split(".")[0]

            # Deletar arquivos cujos os nomes não são numericos
            if n[0] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                os.remove(caminho + "/" + f)
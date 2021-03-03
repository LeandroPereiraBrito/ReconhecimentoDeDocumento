from PIL import Image
from PIL import ImageEnhance
import os
import numpy as np
import core.carregamento as carreg
from matplotlib import image



class Processamento():

# metodo que gerar aas imagens temporarias na escala de cinza e aumenta o brilho e contraste
    def preProcessFiles(arquivo, dim, nom_Dirtemp):
            print(arquivo)
            print(nom_Dirtemp)

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

            # Remover arquivos  redundantes
            Processamento.removeFile(nom_Dirtemp)

            # padronizar tamanho da imagem
            imgp = imgp.resize(dim, Image.ANTIALIAS)

            # Salvar imagem
            imgp.save(nom_Dirtemp)

            # Remover arquivos  redundantes
            Processamento.removeFile(arquivo)



    # Retorna o tamanho da primeira imagem para redimensionar as demais
    def getSize(arquivo):
        imgp = Image.open(arquivo)
        largura = imgp.size[1]
        altura = imgp.size[0]
        dim = (altura, largura)
        return dim


    #Remover arquivos
    def removeFile(arquivo):
        if os.path.exists(arquivo):
            os.remove(arquivo)


    # Elimina as linhas que tenham o mesmo padrão de cores
    def modLinha(self, file):
        # Abrir o arquivo
        img = Image.open(file)

        #transforma a imagem emum array
        matriz = np.asarray(img)

        # Pegar a altura da imagem
        altura = matriz.shape[0]

        i = altura * 255
        arr = []
        matriz = Processamento.modColuna(matriz)
        for linha in matriz:
            new = linha
            valor = 0
            for item in linha:
                valor = valor + item
                if valor != 0 and valor != i:
                    arr.append(new)
        return np.asarray(Processamento.modColuna(arr))



    # Elimina as coluna que tenham uma unica cor
    def modColuna(matriz):
        new = np.transpose(matriz)
        i = new.shape[1] * 255
        arr = []
        for linha in matriz:
            new = linha
            valor = 0
            for item in linha:
                valor = valor + item
            if valor != 0 and valor != i:
                arr.append(new)
        return np.transpose(arr)



# Retorna uma projeção para redimencionamento da imagem para redimensionar as demais
    def getDim(arquivo):
        imgp = Image.open(arquivo)
        largura = imgp.size[1]
        altura = imgp.size[0]
        r = largura / altura
        dim = (altura, int(largura * r))
        return dim


# Retorna a dimensão da primeira imagem de cada arquivo
    def getDimFiles1(dir_imagens):
        list = []
        dirImagem = carreg.Carregar.getSubPastas(dir_imagens)
        for subPasta in dirImagem:
            listFile = carreg.Carregar.getFiles(dir_imagens + subPasta + "/")[0]
            list.append(Processamento.getSize(dir_imagens + subPasta + "/" + listFile))
        return  list

##################################
# Teste deverão ser excluidas
#########################################
    # metodo que gerar aas imagens temporarias na escala de cinza e aumenta o brilho e contraste
    def preProcessFiles2(arquivo,  nom_Dirtemp):
            print(arquivo)
            print(nom_Dirtemp)

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

            # Remover arquivos  redundantes
            Processamento.removeFile(nom_Dirtemp)

            # padronizar tamanho da imagem
            #imgp = imgp.resize(Image.ANTIALIAS)

            # Salvar imagem
            imgp.save(nom_Dirtemp)



    # metodo que gerar aas imagens temporarias na escala de cinza e aumenta o brilho e contraste
    def preProcessFiles3(arquivo, nom_Dirtemp):
            print(arquivo)
            print(nom_Dirtemp)

            # Carregar imagem
            imgp = Image.open(arquivo)
            img = image.imread(arquivo)

            # Escala de sinza
            imgp = imgp.convert("L")

            # Melhorar o contraste
            contrast = ImageEnhance.Brightness(imgp)
            imgp = contrast.enhance(1)

            # Melhorar o Brilho
            brilho = ImageEnhance.Contrast(imgp)
            imgp = brilho.enhance(5)

            # Remover arquivos  redundantes
            Processamento.removeFile(nom_Dirtemp)

            x = imgp.copy()

            # Salvar imagem
            x.save(nom_Dirtemp)

            # Remover arquivos  redundantes
            Processamento.removeFile(arquivo)

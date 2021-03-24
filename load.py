import os


#Retorna os arquivos do diretorio
def getFiles(diretorio):
    list = []
    for pastaAtual, subPastas, arquivos in os.walk(diretorio):
        for item in arquivos:
            list.append(item)
        return list

# Retorna os arquivos do diretorio
def getSubPastas(diretorio):
        list = []
        for pastaAtual, subPastas, arquivos in os.walk(diretorio):
            for item in subPastas:
                list.append(item)
            return list


# Criar a subpasta se ela não existr e limpa caso exista
def gerarSubPasta(caminho):
    if not os.path.exists(caminho):
        os.mkdir(caminho)






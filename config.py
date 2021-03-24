import os
import pathlib

#diretorio raiz
dir_Raiz = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")

#diretorio de imagens
dir_imagens = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")+"/imagem/"

#diretorio Analise
dir_analise = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")+"/analise/"

#diretorio com de imagens temporarias
dir_model = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")+"/modelo/"

# Diretorio macro das imagens  
data_dir = pathlib.Path(dir_imagens)


seed = 123

#Dimensão das imagens  
image_size = (180, 180)

# Tamano da imagens  
batch_size = 32

# Data set de treino 
validation = 0.2

# Quantidade de treinos
epochs = 15
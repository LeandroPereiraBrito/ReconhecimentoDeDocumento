import numpy as np
import os
import load
import config as conf
import processamento as pr
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model



#=====================================================================================================================
#                              Retorna as classes previstas
#=====================================================================================================================
def getClass():
    # Validação de dados de treino
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                                                                    conf.dir_imagens,
                                                                    validation_split=0.2,
                                                                    subset="training",
                                                                    seed=123,
                                                                    image_size=conf.image_size,
                                                                    batch_size=conf.batch_size)
    return train_ds.class_names



# Criar modelo
def gerarModelo(modelName):
    # quantidade de classes
    num_classes = len(load.getSubPastas(conf.dir_imagens))
    print(num_classes)


    # Validação de dados de treino
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                                                                    conf.data_dir,
                                                                    validation_split=0.2,
                                                                    subset="training",
                                                                    seed=123,
                                                                    image_size=conf.image_size,
                                                                    batch_size=conf.batch_size)

    # Validação de dados
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
                                                                conf.data_dir,
                                                                validation_split=0.2,
                                                                subset="validation",
                                                                seed=123,
                                                                image_size=conf.image_size,
                                                                batch_size=conf.batch_size)

    # Criar modelo
    model = Sequential([
                        layers.experimental.preprocessing.Rescaling(1. / 255),
                        layers.Conv2D(16, 3, padding='same', activation='relu'),
                        layers.MaxPooling2D(),
                        layers.Conv2D(32, 3, padding='same', activation='relu'),
                        layers.MaxPooling2D(),
                        layers.Conv2D(64, 3, padding='same', activation='relu'),
                        layers.MaxPooling2D(),
                        layers.Dropout(0.2),
                        layers.Flatten(),
                        layers.Dense(128, activation='relu'),
                        layers.Dense(num_classes)
                    ])

    # Compilar o modelo
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    if os.path.exists(conf.dir_model+modelName):
        model = load_model(conf.dir_model+modelName)

    history = model.fit(train_ds, validation_data=val_ds, epochs=15)

    model.save(conf.dir_model+modelName)



#=====================================================================================================================
#   Verificar se existe um modelo já treinado  para diminuir o nivel de processamento
#=====================================================================================================================
def modelExist():

    # Verificar se existe um modelo pronto para poder ser carregado 
    if not os.path.exists(conf.dir_model+"modeloImagens.h5"):
        preprarImg()

        # Gerar o modelo caso este não exista  
        gerarModelo("modeloImagens.h5")

        # Remover arquivos gerados para o pré - processamento
        pr.resetImagenDir()



    #carregar o modelo para retorna  
    return load_model(conf.dir_model+"modeloImagens.h5")

#=====================================================================================================================
#                        Prepara as imagens para ser processadas
#=====================================================================================================================
def preprarImg():
    #lista com todos os caminho das imagens gerados
    list = []

    #carregar os subdiretorios
    diretorios = load.getSubPastas(conf.dir_imagens)

    # pecorre a lista com os subdiretorios
    for diretotio in diretorios:
        # Caminho até o subdiretorio
        caminho =  conf.dir_imagens+diretotio+"/"

        # carregar todos os arquivos do subdiretorio
        files = load.getFiles(caminho)

        # pecorre a lista com os arquivos
        for file in files:

            # Gerar copias das imagens para o modelo
            listRetorno = pr.copyImage(caminho+file, caminho,file)

            # Inseriri os caminhos dos arquivos gerados para a lista de retorno
            if len(listRetorno) > 0:
                for i in listRetorno:
                    list.append(i)

    return list

#=====================================================================================================================
#              Classificar  as imagens
#=====================================================================================================================
def classificacao():
    # Carregar modelo  
    model = modelExist()
    
    # Carregar as classes de classificação 
    class_names = getClass()

    # Carregar os arquivos que deverão ser classificados  
    files = load.getFiles(conf.dir_analise)

    # Pecorre a lista com os arquivos  
    for file in files:
        # prepar a imagem  para processamento 
        img = keras.preprocessing.image.load_img(conf.dir_analise+file, target_size=conf.image_size,)
        # Gerar um array para a classificação  
        img_array = keras.preprocessing.image.img_to_array(img)
        
        #Retorna um tensor com um eixo de comprimento 
        img_array = tf.expand_dims(img_array, 0)  

        # Classificar imagem 
        predictions = model.predict(img_array)
        
        # Busca a classe que a imagem se ajusta  
        score = tf.nn.softmax(predictions[0])

        print("Imagem {} classsificada como {} com {:.2f}% de probabilidade".format(file, class_names[np.argmax(score)], 100 * np.max(score)))


import numpy as np
import os
import core.processamento as pr
import core.carregamento as car
import tensorflow as tf
import pathlib
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model
import config


#Classe para exução do modelo
class ModeloImagem(object):

    def __init__(self):
        # parâmetros para o carregador:
        self.batch_size = 32
        self.img_height = 180
        self.img_width = 180
        self.epochs = 15
        self.dirAnalise = config.dir_analise
        self.data_dir = pathlib.Path("imagem/")


        # Checando o diretorio de imagens
    def checkImageAnalise(self):
        data_dir = "imagem/"
        data_dir = pathlib.Path(data_dir)
        image_count = len(list(self.data_dir.glob('*/*.jpeg')))
        if image_count < 10:
            return "Analise"
        else:
            return "Modelo"


    # Criar modelo
    def criarModelo(self):
        data_augmentation = keras.Sequential([
            layers.experimental.preprocessing.RandomFlip("horizontal",
                                                         input_shape=(self.img_height, self.img_width, 3)),
            layers.experimental.preprocessing.RandomRotation(0.1),
            layers.experimental.preprocessing.RandomZoom(0.1),
        ])


        model = Sequential([
            data_augmentation,
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
            layers.Dense(5)
        ])
        return model


     #Nomes das classes
    def getClass(self):
        # Validação de dados
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                                                                        self.data_dir,
                                                                        validation_split=0.2,
                                                                        subset="training",
                                                                        seed=123,
                                                                        image_size=(self.img_height, self.img_width),
                                                                        batch_size=self.batch_size)
        return train_ds.class_names


    #=============================================================================================
    #                           Gerador do modelo de deppelearning                               #
    #=============================================================================================
    def gerarModelo(self):
        # Validação de dados de treino
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                                                                        self.data_dir,
                                                                        validation_split=0.2,
                                                                        subset="training",
                                                                        seed=123,
                                                                        image_size=(self.img_height, self.img_width),
                                                                        batch_size=self.batch_size)
        # Validação de dados
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
                                                                    self.data_dir,
                                                                    validation_split=0.2,
                                                                    subset="validation",
                                                                    seed=123,
                                                                    image_size=(self.img_height, self.img_width),
                                                                    batch_size=self.batch_size)

        #Criação do modelo
        model = ModeloImagem.gerarModelo(self)


        # Compilar o modelo
        model.compile(
                      optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy']
                     )


        # Treinar o modelo
        history = model.fit(train_ds, validation_data=val_ds, epochs=self.epochs)

        # Salvaro modelo
        model.save("modeloImagens.h5")





    # Verificar se existe um modelo já treinado  para diminuir o nivel de processamento
    def modelExist(self):
        if not os.path.exists(config.dir_Raiz+"modeloImagens.h5"):
            ModeloImagem.gerarModelo(self)






    #Classificar imagens
    def classificacao(self):
        model = load_model("modeloImagens.h5")
        # Lêr o diretorio
        class_names = ModeloImagem.getClass(self)

        files = car.Carregar.getFiles("analise/dadosIdentidade/")

        # Lê todos aos arquivos do diretotio
        for file in files:
            sunflower_path = "analise/dadosIdentidade/" + file

            img = keras.preprocessing.image.load_img(sunflower_path, target_size=(self.img_height, self.img_width))
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch

            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            print("Imagem {} classsificada como {} com {:.2f} de probabilidade".format(file, class_names[np.argmax(score)], 100 * np.max(score)))


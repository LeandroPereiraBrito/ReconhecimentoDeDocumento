import os
import pytesseract as pyt

#diretorio raiz
dir_Raiz = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")

#diretorio de imagens
dir_imagens = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")+"/imagem/"

#diretorio Analise
dir_analise = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")+"/analise/"

#diretorio com de imagens temporarias
dir_temp = os.path.dirname(os.path.realpath(__file__)).replace(chr(92),"/")+"/imagem/temp/"

# Inicia o tesseract ocr
pyt.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
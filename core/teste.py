import core.carregamento as carreg
import core.processamento as pr
import config as conf
from PIL import Image


x = carreg.Carregar.getSubPastas(conf.dir_imagens)
for i in x:
    if i != "temp":
        getlis = carreg.Carregar.getFiles(conf.dir_imagens+i+"/")
        for item in getlis:
            extensao = item.split(".")
            if extensao != "jpeg":
                try:
                    img2 = Image.open(conf.dir_imagens+i+"/"+item)
                    img2.save(conf.dir_imagens+i+"/"+extensao[0]+".jpeg")

                    pr.Processamento.removeFile(conf.dir_imagens+i+"/"+item)
                except:
                    print(conf.dir_imagens+i+"/"+item)




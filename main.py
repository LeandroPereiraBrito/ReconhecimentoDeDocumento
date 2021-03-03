import core.carregamento as carreg
import core.processamento as pr
import config as conf



# Pegar todos os subdiretotio
lit_subPastas  =  carreg.Carregar.getSubPastas(conf.dir_imagens)
for subpasta in lit_subPastas:
    ############################################################
    #      Carregar arquivos das subpasta para tranformação
    ############################################################

    # Concatenar o caminho da subpasta
    caminhoSub = conf.dir_imagens+subpasta+"/"

    # Carregar todos os carquivos da subpasta
    lis_files = carreg.Carregar.getFiles(caminhoSub)

    #############################################################
    #      Eta de tranformação de arquivos
    ############################################################

    # retorna as dimensão padrão para todas as imagens
    dim = pr.Processamento.getSize( caminhoSub+lis_files[0])


    # Pecorre todas as posições da lista de arquivos
    for file in lis_files:
        # caminho do arquivo
        caminho = caminhoSub+file

        #Extensao
        extend = file.split(".")

        # Camino + nome do arquivo processado
        destino = conf.dir_temp+subpasta+"/Copia_"+extend[0]+".jpeg"

        # Gerar a subpasta
        carreg.Carregar.gerarSubPasta(conf.dir_temp+subpasta)

        #PreProcessamento de imagens para o data set
        pr.Processamento.preProcessFiles(caminho,dim,destino)






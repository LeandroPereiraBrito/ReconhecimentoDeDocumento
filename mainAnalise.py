import core.carregamento as carreg
import core.processamento as pr
import config as conf





    # Carregar todos os carquivos da subpasta
lis_files = carreg.Carregar.getFiles(conf.dir_analise)

#############################################################
#      Eta de tranformação de arquivos
############################################################
list_dim = pr.Processamento.getDimFiles1(conf.dir_imagens)






# Pecorre todas as posições da lista de arquivos
for file in lis_files:
    #========================================================
    #   Teste de
    #========================================================
    partName = file.split(".")

    dirName = conf.dir_analise+partName[0]

    carreg.Carregar.gerarSubPasta(dirName)

    # Contar a quantidade de subpastas
    subpastas = carreg.Carregar.getSubPastas(conf.dir_imagens)

    for pasta in subpastas:
        #==================== FIm Teste ========================

        # caminho do arquivo
        caminhoFile = conf.dir_analise+file


        # Gerar a subpasta
        #carreg.Carregar.gerarSubPasta(conf.dir_analise+"teste/")

        contardor = 1

        for dim in list_dim:
            # Extensão do arquivo
            extens = file.split(".")

            # Camino + nome do arquivo processado
            destino = dirName + "/c_" +str(contardor)+".jpeg"

            #PreProcessamento de imagens para o data set
            pr.Processamento.preProcessFiles(caminhoFile,dim,destino)

            # incrementar contador
            contardor = contardor+1






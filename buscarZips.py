from os import walk
import os
import zipfile
import textract

path = "/root/periciar"
home = "/root"
targetdir = "/tmp/descompactado"

files_find = []
files_find = files_find + ['pdf']
files_find = files_find + ['doc','docx']
files_find = files_find + ['xls','xlsx']
files_find = files_find + ['ppt','pptx']
files_find = files_find + ['pps','ppsx']

lista_palavras = ['palavra_1'] 
lista_palavras = lista_palavras + ['Orlando','Saraiva'] 

def extrair_conteudos(arquivos):
    lista_conteudos = []
    palavras_encontradas = []
    for arquivo in arquivos:
        try:
           texto = textract.process(arquivo)
           texto = texto.decode("utf-8") 
           arquivo_path = arquivo.replace(path,'')
           for palavra in lista_palavras:
               if palavra in texto.lower():
                   palavras_encontradas.append(palavra)
           tupla = (arquivo_path, palavras_encontradas)
           lista_conteudos.append(tupla)
           palavras_encontradas = []
        except Exception as e:
            print(e)
    return lista_conteudos

def caca_palavras(arquivos, nome_zip):
    arquivo_evidencias = home +'/zip/'+ nome_zip + '.txt'
    conteudos = extrair_conteudos(arquivos)
    log = open(arquivo_evidencias, 'w')
    for conteudo in conteudos:
        if len(conteudo[1]) > 0:
            nome_arquivo = conteudo[0]
            nome_arquivo = nome_arquivo.replace(targetdir,'')
            log.write(nome_arquivo +"\n")
            log.write("\t" + str(conteudo[1])+"\n\n")
    log.close()

def arquivos_pesquisados(arquivos):
    arquivos_pesquisados = []
    for arquivo in arquivos:
        for file_type in files_find: 
            if arquivo.endswith(file_type): 
                arquivos_pesquisados.append(arquivo)
    return arquivos_pesquisados

def arquivos_zip(arquivos):
    arquivos_pesquisados = []
    for arquivo in arquivos:
        if arquivo.endswith("zip"): 
            arquivos_pesquisados.append(arquivo)
    return arquivos_pesquisados

def extrair_zip(arquivo,target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    arquivos_internos = []
    arquivos_internos_zip = []
    internos = []
    with zipfile.ZipFile(arquivo,"r") as zip_ref: 
        zip_ref.extractall(target_path)
    for (dirpath, dirnames, filenames) in walk(target_path):  
        for filename in filenames: 
            file_name = str(dirpath + '/'+ filename)
            arquivos_internos.append(file_name)
    arquivos_internos_zip = arquivos_zip(arquivos_internos)
    for arquivo_zipado in arquivos_internos_zip:
        alvo = target_path+"/internos"
        internos = extrair_zip(arquivo_zipado, alvo)
    arquivos_internos = arquivos_internos + internos
    return arquivos_internos

if __name__ == "__main__":
    arquivos = []
    for (dirpath, dirnames, filenames) in walk(path):  
        for filename in filenames: 
            file_name = str(dirpath + '/'+ filename)
            arquivos.append(file_name)
    arquivos = arquivos_zip(arquivos)
    log = open('arquivos_zipados.txt', 'w')
    for arquivo in arquivos:
        nome_arquivo = arquivo
        nome_arquivo = nome_arquivo.replace(path,'')
        log.write(nome_arquivo +"\n")
        try:
            lista = extrair_zip(arquivo, targetdir)
        except Exception as e:
            print(e)
        lista = arquivos_pesquisados(lista)
        arquivo = arquivo.split('/')[-1]
        arquivo = arquivo.replace(" ","_") 
        caca_palavras(lista, arquivo)
        os.system("rm -rf "+targetdir + "/*")
    log.close()

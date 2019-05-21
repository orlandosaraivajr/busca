from os import walk
import hashlib
from functools import partial
import textract

def hashfile(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.sha256()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
        f.close()
    return d.hexdigest()


path = "/root/periciar"
home = "/root"

files_find = []
files_find = files_find + ['pdf']
files_find = files_find + ['doc','docx']
files_find = files_find + ['xls','xlsx']
files_find = files_find + ['ppt','pptx']
files_find = files_find + ['pps','ppsx']

lista_palavras = ['palavra_1'] 
lista_palavras = lista_palavras + ['Orlando','Saraiva'] 

arquivo_evidencias = home + '/buscaPalavras2.txt'

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
           tupla = (arquivo_path, texto, palavras_encontradas)
           lista_conteudos.append(tupla)
           palavras_encontradas = []
        except Exception as e:
            print(e)
    return lista_conteudos

def caca_palavras(arquivos):
    conteudos = extrair_conteudos(arquivos)
    log = open(arquivo_evidencias, 'w')
    for conteudo in conteudos:
        if len(conteudo[2]) > 0:
            log.write(conteudo[0]+"\n")
            log.write("\t" + str(conteudo[2])+"\n\n")
    log.close()

def arquivos_pesquisados(arquivos):
    arquivos_pesquisados = []
    for arquivo in arquivos:
        for file_type in files_find: 
            if arquivo.endswith(file_type): 
                arquivos_pesquisados.append(arquivo)
    return arquivos_pesquisados

if __name__ == "__main__":
    arquivos = []
    for (dirpath, dirnames, filenames) in walk(path):  
        for filename in filenames: 
            file_name = str(dirpath + '/'+ filename)
            arquivos.append(file_name)
    arquivos = arquivos_pesquisados(arquivos)
    caca_palavras(arquivos)


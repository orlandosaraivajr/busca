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

arquivo_evidencias = home + '/assinaturas.txt'

def caca_palavras(arquivos):
    log = open(arquivo_evidencias, 'w')
    for arquivo in arquivos:
        try:
            assinatura = hashfile(arquivo)
            arquivo = arquivo.replace(path,'')
            log.write(assinatura + " \n " + arquivo + "\n\n\n")

        except Exception as e:
            print(e)
    log.close()


if __name__ == "__main__":
    arquivos = []
    for (dirpath, dirnames, filenames) in walk(path):  
        for filename in filenames:
            file_name = str(dirpath + '/'+ filename)
            arquivos.append(file_name)
    caca_palavras(arquivos)


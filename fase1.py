from os import walk
import os
import sys
from shutil import copyfile  
import hashlib
from functools import partial

def hashfile(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.sha256()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
        f.close()
    return d.hexdigest()

path_ori = "/mnt"
path_dest = "/media/hd_externo/maquina_01"

files_find = []
files_find = files_find + ['doc','docx','ppt','pptx']
files_find = files_find + ['pdf','xls','xlsx']
files_find = files_find + ['pst','epub','eml']
files_find = files_find + ['html','htm','odt','csv']

maquina = 'maquina_01'
arquivo_log = 'arquivos_coletados_'+maquina + '.txt'


log = open(arquivo_log, 'w')
for (dirpath, dirnames, filenames) in walk(path_ori):
    for filename in filenames:
        for file_type in files_find: 
            if filename.endswith(file_type): 
                try: 
                    file_name = str(dirpath + '/'+ filename)
                    dirpath_dest = dirpath.replace(path_ori, path_dest)
                    file_dest = dirpath_dest+'/'+ filename
                    if not os.path.exists(dirpath_dest):
                       os.makedirs(dirpath_dest)
                    assinatura_arquivo_ori = hashfile(file_name)
                    log.write(assinatura_arquivo_ori + '\t')
                    log.write(file_name + '\t\n')
                    copyfile(file_name, file_dest)
                    assinatura_arquivo_dest = hashfile(file_dest)
                    if assinatura_arquivo_dest != assinatura_arquivo_ori:
                        log.write('ARQUIVO COMPROMETIDO=>' + file_name + '\t')
                except Exception as e:
                    print(e)
log.close()

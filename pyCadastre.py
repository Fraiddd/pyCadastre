# coding: utf-8

import os
import requests
import tarfile
from tkinter import messagebox as mb
from urllib import request

##############################################################################
def extract(str, deb, end):
    return str[str.index(deb)+len(deb):str.index(end)]
##############################################################################
def takachoice(tit, txt):
    res = mb.askquestion(tit, txt)
    if res == 'yes' :
        return True
    else :
        return False
# print(takachoice('Download Cadastre', 'Delete existing files?'))
##############################################################################
def unzipbz2(file):
    tar = tarfile.open(file)
    tar.extractall('/'.join(file.split('/')[:-1]))
    tar.close()
##############################################################################
def download(url, fich):
    try:
        reponse = request.urlopen(url)
        contenu_web = reponse.read().decode('UTF-8')
        with open(fich, 'w') as f: f.write(contenu_web)
        return True
    except:
        return False
##############################################################################
def getCadastre(insee):
    
    url = 'https://cadastre.data.gouv.fr/data/dgfip-pci-vecteur/latest/dxf/feuilles/'\
         + insee[0:2] + '/' + insee
    htm = './tmp.html'
    path = 'c:/Data/Carto/'+ insee[0:2] + '/' + insee + '/'
    try:
        files = os.listdir(path)
    except:
        files = None
    if files:
        if takachoice('Download Cadastre', 'Delete existing files?'):
            for fi in files:
                os.remove(fi)
        else:
            os.sys.exit()
    download(url, htm)
    lbz2 = []
    file = open(htm, 'r')
    for l in file:
        if '<a href="dxf-' in l:
            lbz2.append(extract(l,'.tar.bz2">','</a>'))
    file.close()
    os.makedirs(path, exist_ok=True)
    lf = []
    for f in lbz2:
        lf.append(path+f)
        response = requests.get(url+'/'+f)
        open(path+f, 'wb').write(response.content)
       
    for f in lf:
        unzipbz2(f)
        os.remove(f)
    
    os.remove(htm)

getCadastre('05007')

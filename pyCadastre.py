# coding: utf-8

import os
import sys
import requests
import tarfile
from tkinter import messagebox as mb
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Entry, Label,\
                        Button, Style
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
def getString(appli, label):
    def ok():
        win.destroy()
    def ext():
        mb.showerror(title='Canceled', message='You lost your way ...')
        sys.exit()
    win = Tk()
    st =  Style()
    st.configure('frameStyle.TFrame', borderwidth=2, relief='solid')
    text = StringVar()
    win.title(appli)
    win.geometry('250x120+820+270')
    win.resizable(False, False)
    Label(win, text = label).pack()
    fram  = Frame(win, style='frameStyle.TFrame')
    fram.pack(padx=10, pady=10)
    Entry(fram, textvariable=text).pack()

    ok_but = Button(win, text="Ok", command=ok)
    ok_but.pack(pady=10)

    win.bind('<Escape>', lambda e: ext())
    win.protocol("WM_DELETE_WINDOW", ext)
    win.mainloop()
    return text.get()

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
        if takachoice('pyCadastre', 'Effacer les fichiers existants?'):
            for fi in files:
                os.remove(path+fi)
        else:
            mb.showerror(title='Abandon', message='Un cadastre est déjà present')
            os.sys.exit()
    if download(url, htm):
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
    else:
        mb.showerror(title='Abandon', message='Vérifiez le numéro INSEE')
insee = ''
insee = getString('pyCadastre', 'Numéro INSEE ex: 35288')
while len(insee) != 5 or not insee.isdigit():
    insee = getString('pyCadastre', '   Numéro INVALIDE\nNuméro INSEE ex: 35288')
getCadastre(insee)

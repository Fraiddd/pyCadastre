# coding: utf-8
# Python 3.11.1
'''
    pyCadastre 1.0

    Télécharge et extrait les feuilles cadastrales d'une commune Française.

    - Pas installation.

    - Seulement pour Windows

    - Testé avec Windows 10 et Autocad 2015

    :No copyright: (!) 2023 by Frédéric Coulon.
    :No license: Do with it what you want.
'''
import os
import sys
import requests
import tarfile
from tkinter import Tk, StringVar, messagebox as mb
from tkinter.ttk import Entry, Label, Button
from urllib import request

# Sub Functions
##############################################################################
'''
exctract(<String>, <String>, <String>)
Extrait un texte entre deux textes.
Arguments: String, Texte total
           String, 1er texte
           String, 2em texte
Retour: String
extract('Extrait un texte entre deux textes.', 'Extrait un ',' deux textes')
-> 'texte entre'
'''
def extract(str, deb, end):
    return str[str.index(deb)+len(deb):str.index(end)]
##############################################################################
'''
takachoice(<String>, <String>)
Affiche un messageBox oui/non.
Arguments: String, Titre
           String, Question
Retour: Boolean, True or False
'''
def takachoice(tit, txt):
    res = mb.askquestion(tit, txt)
    if res == 'yes' :
        return True
    else :
        return False
##############################################################################
'''
unzipbz2(<String>)
Décompresse les fichiers .tar.bz2.
Argument: String, Chemin complet du fichier.
Retour: Aucun
'''
def unzipbz2(file):
    tar = tarfile.open(file)
    tar.extractall('/'.join(file.split('/')[:-1]))
    tar.close()
##############################################################################
'''
download(<String>, <String>)
Télécharge un fichier.
Arguments: String, Adresse internet complete du fichier
           String, Chemin complet du fichier.
Retour: Boolean, True or False
download('https://monsite/mapage.html', 'c://monDossier/mapage.html')
'''
def download(url, fich):
    try:
        reponse = request.urlopen(url)
        contenu_web = reponse.read().decode('UTF-8')
        with open(fich, 'w') as f: f.write(contenu_web)
        return True
    except:
        return False
##############################################################################
'''
getString(<String>, <String>)
Entrée utilisateur pour un texte.
Arguments: String, titre.
           String, Texte affiché.
Retour: String, Texte saisi.
'''
def getString(appli, label):
    def ok():
        win.destroy()
    def ext():
        mb.showerror(title='Canceled', message='You lost your way ...')
        sys.exit()
    win = Tk()
    text = StringVar()
    win.title(appli)
    win.geometry('250x120+820+270')
    win.resizable(False, False)
    Label(win, text = label).pack()
    Entry(win, textvariable=text).pack(padx=10, pady=10)
    Button(win, text="Ok", command=ok).pack(pady=10)
    win.bind('<Escape>', lambda e: ext())
    win.protocol("WM_DELETE_WINDOW", ext)
    win.mainloop()
    return text.get()
##############################################################################
# Main
def pyCadastre(insee):
    url = 'https://cadastre.data.gouv.fr/data/dgfip-pci-vecteur/latest/dxf/feuilles/'\
         + insee[0:2] + '/' + insee
    htm = './tmp.html'
    path = 'c:/Data/Carto/'+ insee[0:2] + '/' + insee + '/'
    # Test si il existe déjà un cadastre dans le dossier.
    try: files = os.listdir(path)
    except: files = None
    if files:
        # Si un cadastre est présent, demande si on éfface les fichiers.
        if takachoice('pyCadastre', 'Effacer les fichiers existants?'):
            for fi in files:
                os.remove(path + fi)
        else:
            mb.showerror(title='Abandon', message='Un cadastre est déjà present')
            os.sys.exit()
    #  Si le téléchargement de la page est réussi.
    if download(url, htm):
        lbz2 = []
        file = open(htm, 'r')
        # Lecture de la page ligne par ligne.
        for l in file:
            # Ajout du nom du fichier à la liste lbz2.
            if '<a href="dxf-' in l:
                lbz2.append(extract(l,'.tar.bz2">','</a>'))
        file.close()
        # Création éventuelle du dossier.
        os.makedirs(path, exist_ok=True)
        lf = []
        # Téléchargement des .bz2.
        for f in lbz2:
            lf.append(path+f)
            response = requests.get(url + '/ '+ f)
            open(path + f, 'wb').write(response.content)
        # Décompression des bz2.
        for f in lf:
            unzipbz2(f)
            os.remove(f)
        # Supprime la page.
        os.remove(htm)
    else:
        mb.showerror(title='Abandon', message='Vérifiez le numéro INSEE, \
                     ou votre connexion.')
##############################################################################
# Launcher
insee = ''
# Saisie du Numéro INSEE
insee = getString('pyCadastre', 'Numéro INSEE ex: 35288')
# Tant que le numéro n'a pas 5 caractères numériques.
while len(insee) != 5 or not insee.isdigit():
    insee = getString('pyCadastre', '   Numéro INVALIDE\nNuméro INSEE ex: 35288')
pyCadastre(insee)

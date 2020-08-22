import time

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

# ---------------------------------
def supprime_accent(ligne):
    """ supprime les accents du texte source """
    out = ""
    for mot in ligne:
        for c in mot:
            if c == 'é' or c == 'è' or c == 'ê':
                c = 'e'
            elif c == 'à' or c == 'ä' or c == 'â':
                c = 'a'
            elif c == 'ù' or c == 'û' or c == 'ü':
                c = 'u'
            elif c == 'î' or c == 'ï':
                c = 'i'
            elif c == 'ç':
                c = 'c'
            out += c
    return out


# ---------------------------------
def supprimer_ponctuation(ligne):
    """ supprime la ponctuatios du texte source """
    ponctuation = "!?.;:,%-/_è|*[~`\^@=){}]'#"
    result = ''

    for lettre in ligne:
        if not (lettre in ponctuation):
            result = result + lettre
    return result


# ---------------------------------
def Pretraitements(ligne):
    if ligne != '':
        return (supprimer_ponctuation(supprime_accent(ligne.lower().strip())))
    else:
        return 0


# ---------------------------------
# read and clean data from prenom csv file
def get_names_as_df():
    dataframe = pd.read_csv("./Prenoms.csv")
    for i, row in dataframe.iterrows():
        value = Pretraitements(row[0])
        dataframe.at[i, '01_prenom'] = value
    return np.array(dataframe['01_prenom']), np.array(dataframe['02_genre'])


def check(prenom):
    out = False
    prenom = Pretraitements(prenom.lower().strip())
    vecteur_prenoms, vecteur_class = get_names_as_df()
    i = 0
    taille_max = len(vecteur_prenoms)
    result = 'none'
    while (i < taille_max and (not out)):
        if fuzz.ratio(prenom, vecteur_prenoms[i]) > 98:
            out = True
            result = vecteur_class[i]
        i = i + 1
    return result


inputFile = pd.read_csv("./testfile.csv")

taille_max = len(inputFile)

for i, row in inputFile.iterrows():
    value = Pretraitements(row['prenom'])
    rez = check(value)

    if rez == 'f':
        rez=("Feminin")
    elif rez == 'm':
        rez=("Masculin")
    elif 'f' in rez and 'm' in rez:
        rez=('Mixte')
    else:
        rez=('Introuvable')
    inputFile.at[i, 'Sexe'] = rez
    i = i + 1

inputFile.to_csv("ResultatNom.csv", encoding='utf-8', sep=',', index=False)

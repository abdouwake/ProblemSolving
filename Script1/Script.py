from Script1.Utils import tester_adresse, Pretraitements, generer_mails
import pandas as pd
import numpy as np

# Variables
adresses = []
j = 0

# Pour le fichier CSV
tableau = []
entetes = ['nom', 'prenom', 'domaine', 'mails', 'potentiels_mails']

# Lecture du fichier et récupération des données
df = pd.read_csv("data.csv")
firstNames = np.array(df['nom'])
lastNames = np.array(df['prenom'])
domaines = np.array(df['domaine'])

dataframe = pd.DataFrame(columns=entetes)
dataframe_fail = pd.DataFrame(columns=['nom', 'prenom', 'domaine'])

for i in range(0, len(firstNames)):
    ligne = []
    ligne.append(Pretraitements(lastNames[i]))
    ligne.append(Pretraitements(firstNames[i]))
    ligne.append(Pretraitements(domaines[i]))

    adresses = generer_mails(Pretraitements(firstNames[i]), Pretraitements((lastNames[i])), Pretraitements(domaines[i]))
    adresses_valides = ''
    potentiels_adresses = ''

    for mail in adresses:
        result = tester_adresse(mail)
        if (result == 'valid'):
            adresses_valides = adresses_valides + ' - ' + mail
        elif (result == 'unknown'):
            potentiels_adresses = potentiels_adresses + ' - ' + mail

    ligne.append(adresses_valides)
    ligne.append(potentiels_adresses)

    if (adresses_valides != '' or potentiels_adresses != ''):
        dataframe.loc[i] = ligne
    else:
        ligne_fail = []
        ligne_fail.append(Pretraitements(lastNames[i]))
        ligne_fail.append(Pretraitements(firstNames[i]))
        ligne_fail.append(Pretraitements(domaines[i]))
        dataframe_fail.loc[j] = ligne_fail
        j = j + 1


#Ecriture des datafraùes dans des fichiers
dataframe.to_csv("Success.csv", encoding='utf-8', sep=',', index=False)
dataframe_fail.to_csv("Fail.csv", encoding='utf-8', sep=',', index=False)

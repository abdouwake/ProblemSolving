import whois
from Script1.Config import url
from Script1.Config import tld
import requests


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


def supprimer_ponctuation(ligne):
    """ supprime la ponctuatios du texte source """
    ponctuation = "!?.;:,%-/_è|*[~`\^@=){}]'#"
    result = ''

    for lettre in ligne:
        if not (lettre in ponctuation):
            result = result + lettre
    return result


def Pretraitements(ligne):
    if ligne != '':
        return (supprimer_ponctuation(supprime_accent(ligne.lower().strip())))
    else:
        return 0


def get_valide_domaines(domaineName):
    resultatTld = []
    for item in tld:
        w = whois.whois(domaineName + item)
        if (w.domain_name):
            resultatTld.append(domaineName + item)
    return resultatTld


def generer_mails(firstName, lastName, domaine):
    resultatMails = []
    for item in get_valide_domaines(domaine):
        Tab_formats = [
            firstName[0] + lastName,
            firstName + lastName,
            lastName + firstName,
            lastName[0] + firstName,
            firstName + '_' + lastName,
            lastName + '_' + firstName,
            firstName + '-' + lastName,
            lastName + '-' + firstName,
            firstName + '.' + lastName,
            lastName + '.' + firstName,
            firstName[0] + '.' + lastName,
            lastName[0] + '.' + firstName,
            firstName[0] + '-' + lastName,
            lastName[0] + '-' + firstName,
            firstName[0] + '_' + lastName,
            lastName[0] + '_' + firstName,
        ]

        for format in Tab_formats:
            email = format + "@" + item
            resultatMails.append(email)
    return resultatMails


def tester_adresse(adresse):
    response = requests.get(url+adresse)
    response=response.json()
    print(response)
    return (response['format_valid'])

import random

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def inverseModulaire(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def genererPaireClef(bits):
    p = q = 1
    while p == q:
        p = random.getrandbits(bits)
        q = random.getrandbits(bits)
        p = nombrePremierSuivant(p)
        q = nombrePremierSuivant(q)
    n = p * q
    lambdaVal = (p - 1) * (q - 1)
    g = n + 1
    mu = inverseModulaire(lambdaVal, n)
    return ((n, g), (lambdaVal, mu, n))

def estPremier(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def nombrePremierSuivant(n):
    while True:
        n += 1
        if estPremier(n):
            return n

def chiffrer(clefPublique, messageClair):
    while True:
        r = random.randrange(1, clefPublique[0])
        if pgcd(r, clefPublique[0]) == 1:
            break
    x = pow(r, clefPublique[0], clefPublique[0] ** 2)
    messageChiffre = (pow(clefPublique[1], messageClair, clefPublique[0] ** 2) * x) % clefPublique[0] ** 2
    return messageChiffre

def dechiffrer(clefPrivee, messageChiffre):
    x = pow(messageChiffre, clefPrivee[0], clefPrivee[2] ** 2) - 1
    messageClair = (x // clefPrivee[2]) * clefPrivee[1] % clefPrivee[2]
    return messageClair

def texteVersNombres(texte):
    return [ord(caractere) for caractere in texte]

def nombresVersTexte(nombres):
    return ''.join(chr(nombre) for nombre in nombres)

def chiffrerTexte(clefPublique, texte):
    nombres = texteVersNombres(texte)
    return [chiffrer(clefPublique, nombre) for nombre in nombres]

def dechiffrerTexte(clefPrivee, texteChiffre):
    nombresClairs = [dechiffrer(clefPrivee, nombreChiffre) for nombreChiffre in texteChiffre]
    return nombresVersTexte(nombresClairs)

def sauvegarderTexteChiffre(fichier, texteChiffre):
    with open(fichier, 'w') as f:
        f.write(','.join(map(str, texteChiffre)))

def chargerTexteChiffre(fichier):
    with open(fichier, 'r') as f:
        return list(map(int, f.read().split(',')))

def sauvegarderClefs(fichierPublique, fichierPrive, clefPublique, clefPrivee):
    with open(fichierPublique, 'w') as f:
        f.write(f"{clefPublique[0]},{clefPublique[1]}")
    with open(fichierPrive, 'w') as f:
        f.write(f"{clefPrivee[0]},{clefPrivee[1]},{clefPrivee[2]}")

def chargerClefs(fichierPublique, fichierPrive):
    with open(fichierPublique, 'r') as f:
        n, g = map(int, f.read().split(','))
    with open(fichierPrive, 'r') as f:
        lambdaVal, mu, n = map(int, f.read().split(','))
    return (n, g), (lambdaVal, mu, n)

clefPublique, clefPrivee = genererPaireClef(8)

phrase = """

    ’Paroles’’ (1949)
    Il dit non avec la tête
    mais il dit oui avec le coeur
    il dit oui à ce qu’il aime
    il dit non au professeur
    il est debout
    on le questionne
    et tous les problèmes sont posés
    soudain le fou rire le prend
    et il efface tout
    les chiffres et les mots
    les dates et les noms
    les phrases et les pièges
    et malgré les menaces du maître
    sous les huées des enfants prodiges
    avec les craies de toutes les couleurs
    sur le tableau noir du malheur
    il dessine le visage du bonheur.
    
    """

phraseChiffree = chiffrerTexte(clefPublique, phrase)

sauvegarderTexteChiffre('phrase_chiffree.txt', phraseChiffree)

sauvegarderClefs('clef_publique.txt', 'clef_privee.txt', clefPublique, clefPrivee)

phraseChiffreeChargee = chargerTexteChiffre('phrase_chiffree.txt')
clefPubliqueChargee, clefPriveeChargee = chargerClefs('clef_publique.txt', 'clef_privee.txt')

phraseDechiffree = dechiffrerTexte(clefPriveeChargee, phraseChiffreeChargee)

print(f"Phrase originale: {phrase}")
print(f"Phrase déchiffrée: {phraseDechiffree}")

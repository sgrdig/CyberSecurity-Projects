import random

class CryptoUtils:
    @staticmethod
    def pgcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def inverse_modulaire(a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    @staticmethod
    def est_premier(n):
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

    @staticmethod
    def nombre_premier_suivant(n):
        while True:
            n += 1
            if CryptoUtils.est_premier(n):
                return n


class Paillier:
    def __init__(self, bits=8):
        self.bits = bits
        self.public_key = None
        self.private_key = None

    def generer_cles(self):
        p = q = 1
        while p == q:
            p = random.getrandbits(self.bits)
            q = random.getrandbits(self.bits)
            p = CryptoUtils.nombre_premier_suivant(p)
            q = CryptoUtils.nombre_premier_suivant(q)

        n = p * q
        lambda_val = (p - 1) * (q - 1)
        g = n + 1
        mu = CryptoUtils.inverse_modulaire(lambda_val, n)

        self.public_key = (n, g)
        self.private_key = (lambda_val, mu, n)

    def chiffrer(self, message):
        n, g = self.public_key
        while True:
            r = random.randrange(1, n)
            if CryptoUtils.pgcd(r, n) == 1:
                break
        x = pow(r, n, n ** 2)
        c = (pow(g, message, n ** 2) * x) % (n ** 2)
        return c

    def dechiffrer(self, message_chiffre):
        lambda_val, mu, n = self.private_key
        x = pow(message_chiffre, lambda_val, n ** 2) - 1
        return ((x // n) * mu) % n

    def sauvegarder_cles(self, fichier_publique, fichier_privee):
        with open(fichier_publique, 'w') as f:
            f.write(f"{self.public_key[0]},{self.public_key[1]}")
        with open(fichier_privee, 'w') as f:
            f.write(f"{self.private_key[0]},{self.private_key[1]},{self.private_key[2]}")

    def charger_cles(self, fichier_publique, fichier_privee):
        with open(fichier_publique, 'r') as f:
            n, g = map(int, f.read().split(','))
        with open(fichier_privee, 'r') as f:
            lambda_val, mu, n2 = map(int, f.read().split(','))
        self.public_key = (n, g)
        self.private_key = (lambda_val, mu, n2)


class TexteCrypto:
    @staticmethod
    def texte_vers_nombres(texte):
        return [ord(c) for c in texte]

    @staticmethod
    def nombres_vers_texte(nombres):
        return ''.join(chr(n) for n in nombres)

    @staticmethod
    def chiffrer_texte(paillier, texte):
        return [paillier.chiffrer(n) for n in TexteCrypto.texte_vers_nombres(texte)]

    @staticmethod
    def dechiffrer_texte(paillier, texte_chiffre):
        nombres = [paillier.dechiffrer(c) for c in texte_chiffre]
        return TexteCrypto.nombres_vers_texte(nombres)

    @staticmethod
    def sauvegarder_texte_chiffre(fichier, texte_chiffre):
        with open(fichier, 'w') as f:
            f.write(','.join(map(str, texte_chiffre)))

    @staticmethod
    def charger_texte_chiffre(fichier):
        with open(fichier, 'r') as f:
            return list(map(int, f.read().split(',')))


# --- Utilisation ---
phrase = """
    ’Paroles’’ (1949)
    Il dit non avec la tête
    mais il dit oui avec le coeur
    ...
    il dessine le visage du bonheur.
"""

paillier = Paillier(bits=64)
paillier.generer_cles()

texte_chiffre = TexteCrypto.chiffrer_texte(paillier, phrase)
TexteCrypto.sauvegarder_texte_chiffre('phrase_chiffree.txt', texte_chiffre)
paillier.sauvegarder_cles('clef_publique.txt', 'clef_privee.txt')

paillier.charger_cles('clef_publique.txt', 'clef_privee.txt')
texte_chiffre_charge = TexteCrypto.charger_texte_chiffre('phrase_chiffree.txt')
texte_dechiffre = TexteCrypto.dechiffrer_texte(paillier, texte_chiffre_charge)

print("Phrase originale:\n", phrase)
print("\nPhrase déchiffrée:\n", texte_dechiffre)

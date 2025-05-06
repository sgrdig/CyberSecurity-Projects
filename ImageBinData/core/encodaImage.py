import random
from PIL import Image

marqueFin = '11111110'

def convertirEnBinaire(donnees):
    return ''.join(format(octet, '08b') for octet in donnees)

def convertirDepuisBinaire(bits):
    octets = []
    for i in range(0, len(bits), 8):
        bloc = bits[i:i+8]
        if ''.join(bloc) == marqueFin:
            break
        octets.append(int(''.join(bloc), 2))
    return bytes(octets)

def cacherDonnees(image, donnees, motDePasse):
    binaire = convertirEnBinaire(donnees) + marqueFin
    pixels = list(image.getdata())
    pixelsPlats = [canal for pixel in pixels for canal in pixel]

    if len(binaire) > len(pixelsPlats):
        raise ValueError("Données trop volumineuses pour l'image.")

    random.seed(motDePasse)
    positions = random.sample(range(len(pixelsPlats)), len(binaire))

    for i, bit in enumerate(binaire):
        pos = positions[i]
        pixelsPlats[pos] = (pixelsPlats[pos] & ~1) | int(bit)

    nouveauxPixels = list(zip(*(iter(pixelsPlats),) * 3))
    nouvelleImage = Image.new("RGB", image.size)
    nouvelleImage.putdata(nouveauxPixels)
    return nouvelleImage

def extraireDonnees(image, motDePasse):
    pixels = list(image.getdata())
    pixelsPlats = [canal for pixel in pixels for canal in pixel]

    random.seed(motDePasse)
    positions = random.sample(range(len(pixelsPlats)), len(pixelsPlats))

    bits = [str(pixelsPlats[i] & 1) for i in positions]
    return convertirDepuisBinaire(bits)

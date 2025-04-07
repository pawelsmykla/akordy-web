from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
import os

STRUNY = ['e', 'B', 'G', 'D', 'A', 'E']
WSZYSTKIE_DZWIEKI = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

progi = {
    1: (6, 90), 2: (90, 169), 3: (169, 244), 4: (244, 317), 5: (317, 384), 6: (384, 448),
    7: (448, 508), 8: (508, 563), 9: (563, 616), 10: (616, 666), 11: (666, 714),
    12: (714, 759), 13: (759, 802), 14: (802, 842), 15: (842, 879), 16: (879, 915),
    17: (915, 949), 18: (949, 980), 19: (980, 1011), 20: (1011, 1039),
    21: (1039, 1065), 22: (1065, 1091), 23: (1091, 1114), 24: (1114, 1136)
}

struna_y = {
    'e': 98, 'B': 80, 'G': 63, 'D': 46, 'A': 29, 'E': 11
}

MAPA_STRUN = {}
for struna, baza_dzwieku in zip(STRUNY, ['E', 'B', 'G', 'D', 'A', 'E']):
    idx = WSZYSTKIE_DZWIEKI.index(baza_dzwieku)
    dzwieki = [(prog, WSZYSTKIE_DZWIEKI[(idx + prog) % 12]) for prog in range(0, 25)]
    MAPA_STRUN[struna] = dzwieki

def znajdz_na_strunie_blisko(struna, nuta, preferowane_progi):
    dostepne = [(prog, dzwiek) for prog, dzwiek in MAPA_STRUN[struna] if dzwiek == nuta]
    if not dostepne:
        return None
    return min(dostepne, key=lambda x: min(abs(x[0] - p) for p in preferowane_progi))[0]

def znajdz_na_strunie(struna, nuta, minimalny_prog=0):
    for prog, dzwiek in MAPA_STRUN[struna]:
        if dzwiek == nuta and prog >= minimalny_prog:
            return prog
    return None

def rysuj_diagram(ax, punkty, tytul):
    img_path = os.path.join("static", "template_gryf.jpg")
    img = Image.open(img_path)
    ax.imshow(img, extent=[0, img.width, 0, img.height])
    ax.set_title(tytul)
    ax.set_xlim(0, img.width)
    ax.set_ylim(0, img.height)
    ax.axis('off')

    kolory = {
        'pryma': 'green', 'sekunda': 'orange', 'tercja': 'red',
        'kwinta': 'blue', 'septyma': 'purple'
    }
    size = 24

    for klucz, (prog, nuta) in punkty.items():
        czesci = klucz.split('_')
        struna = czesci[0]
        interwal = czesci[1]
        x = sum(progi[prog]) / 2 if prog in progi else 0
        y = struna_y[struna]
        color = kolory.get(interwal, 'black')

        if interwal == 'pryma':
            shape = patches.Rectangle((x - size / 2, y - size / 2), size, size, color=color)
        else:
            shape = patches.Circle((x, y), size / 2, color=color)
        ax.add_patch(shape)
        ax.text(x, y, nuta, ha='center', va='center', fontsize=10, color='white',
                path_effects=[path_effects.withStroke(linewidth=1.2, foreground='black')])

def rozpoznaj_typ_akordu(slowo):
    if "maj7" in slowo:
        return "Durowy"
    elif "m7b5" in slowo:
        return "Półzmniejszony"
    elif "m7" in slowo:
        return "Molowy"
    elif "7" in slowo:
        return "Dominantowy"
    return None

def rozbij_akordy_na_parametry(ciag):
    akordy = []
    for blok in ciag.split(","):
        czesci = blok.strip().split()
        if len(czesci) != 2:
            akordy.append((blok.strip(), None, "ERROR"))
            continue
        slowo, struna = czesci
        typ = rozpoznaj_typ_akordu(slowo)
        tonika = slowo.replace("maj7", "").replace("m7b5", "").replace("m7", "").replace("7", "")
        akordy.append((tonika, typ, struna))
    return akordy

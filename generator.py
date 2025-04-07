import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # folder tymczasowy PyInstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects

# --- KONFIGURACJA MAPOWANIA ---

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

# --- MAPA STRUN I DźWIĘKÓW ---

MAPA_STRUN = {}
for struna, baza_dzwieku in zip(STRUNY, ['E', 'B', 'G', 'D', 'A', 'E']):
    idx = WSZYSTKIE_DZWIEKI.index(baza_dzwieku)
    dzwieki = [(prog, WSZYSTKIE_DZWIEKI[(idx + prog) % 12]) for prog in range(0, 25)]
    MAPA_STRUN[struna] = dzwieki

# --- FUNKCJE POMOCNICZE ---

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

# --- BUDOWANIE AKORDU I ETIUDY ---

def buduj_akord_sztywno(tonika, struna_bazowa, przewrot, typ):
    INTERWALY = {
        'Durowy': {'tercja': 4, 'septyma': 11, 'kwinta': 7, 'sekunda': 2},
        'Molowy': {'tercja': 3, 'septyma': 10, 'kwinta': 7, 'sekunda': 2},
        'Dominantowy': {'tercja': 4, 'septyma': 10, 'kwinta': 7, 'sekunda': 2},
        'Półzmniejszony': {'tercja': 3, 'septyma': 10, 'kwinta': 6, 'sekunda': 1}
    }
    tonika_idx = WSZYSTKIE_DZWIEKI.index(tonika)
    tercja = WSZYSTKIE_DZWIEKI[(tonika_idx + INTERWALY[typ]['tercja']) % 12]
    septyma = WSZYSTKIE_DZWIEKI[(tonika_idx + INTERWALY[typ]['septyma']) % 12]

    struktura = {
        ('E', 1): {'E': tonika, 'D': septyma, 'G': tercja},
        ('E', 2): {'E': tonika, 'A': tercja, 'D': septyma},
        ('A', 1): {'A': tonika, 'G': septyma, 'B': tercja},
        ('A', 2): {'A': tonika, 'D': tercja, 'G': septyma},
        ('D', 1): {'D': tonika, 'B': septyma, 'e': tercja},
        ('D', 2): {'D': tonika, 'G': tercja, 'B': septyma}
    }

    problematyczne_wyjatki = {
        ('E', 'E#'), ('E', 'F'),
        ('A', 'A#'),
        ('D', 'D#'),
        ('D', 'C')
    }

    pryma_prog_min = 0
    if przewrot == 2:
        if tonika == struna_bazowa or (struna_bazowa, tonika) in problematyczne_wyjatki:
            pryma_prog_min = 10

    akord = {}
    pozycje_akordu = {}
    prog_prymy = None

    for struna, nuta in struktura[(struna_bazowa, przewrot)].items():
        if nuta == tonika:
            prog = znajdz_na_strunie(struna, nuta, minimalny_prog=pryma_prog_min)
            prog_prymy = prog
            interwal = 'pryma'
        elif nuta == tercja:
            if prog_prymy is not None:
                preferowane = [prog_prymy + i for i in range(-1, 3)]
                prog = znajdz_na_strunie_blisko(struna, nuta, preferowane)
            else:
                prog = znajdz_na_strunie(struna, nuta, minimalny_prog=pryma_prog_min)
            interwal = 'tercja'
        elif nuta == septyma:
            if prog_prymy is not None:
                preferowane = [prog_prymy + i for i in range(-1, 3)]
                prog = znajdz_na_strunie_blisko(struna, nuta, preferowane)
            else:
                prog = znajdz_na_strunie(struna, nuta, minimalny_prog=pryma_prog_min)
            interwal = 'septyma'

        akord[f"{struna}_{interwal}"] = (prog, nuta)
        pozycje_akordu[interwal] = (struna, prog)

    return akord, tercja, septyma, typ, pryma_prog_min, pozycje_akordu

def buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ, pryma_prog_min=0, pozycje_akordu={}):
    INTERWALY = {
        'Durowy': {'kwinta': 7, 'sekunda': 2},
        'Molowy': {'kwinta': 7, 'sekunda': 2},
        'Dominantowy': {'kwinta': 7, 'sekunda': 2},
        'Półzmniejszony': {'kwinta': 6, 'sekunda': 1}
    }

    skala = {
        'pryma': tonika,
        'tercja': tercja,
        'septyma': septyma,
        'sekunda': WSZYSTKIE_DZWIEKI[(WSZYSTKIE_DZWIEKI.index(tonika) + INTERWALY[typ]['sekunda']) % 12],
        'kwinta': WSZYSTKIE_DZWIEKI[(WSZYSTKIE_DZWIEKI.index(tonika) + INTERWALY[typ]['kwinta']) % 12]
    }

    struktury = {
        ('E', 1): {'D': ['septyma', 'pryma', 'sekunda'], 'G': ['tercja', 'kwinta']},
        ('E', 2): {'A': ['tercja', 'kwinta'], 'D': ['septyma', 'pryma', 'sekunda']},
        ('A', 1): {'G': ['septyma', 'pryma', 'sekunda'], 'B': ['tercja', 'kwinta']},
        ('A', 2): {'D': ['tercja', 'kwinta'], 'G': ['septyma', 'pryma', 'sekunda']},
        ('D', 1): {'B': ['septyma', 'pryma', 'sekunda'], 'e': ['tercja', 'kwinta']},
        ('D', 2): {'G': ['tercja', 'kwinta'], 'B': ['septyma', 'pryma', 'sekunda']}
    }

    etiuda = {}
    for struna_doc, interwaly in struktury[(struna, przewrot)].items():
        for idx, interwal in enumerate(interwaly):
            nuta = skala[interwal]
            if interwal in ['tercja', 'septyma'] and interwal in pozycje_akordu:
                prog = pozycje_akordu[interwal][1]
            else:
                poprzedni_interwal = interwaly[idx - 1] if idx > 0 else None
                poprzedni_prog = pozycje_akordu.get(poprzedni_interwal, (None, None))[1] if poprzedni_interwal else None
                preferowane = [poprzedni_prog + i for i in range(1, 4)] if poprzedni_prog is not None else list(range(pryma_prog_min, 25))
                prog = znajdz_na_strunie_blisko(struna_doc, nuta, preferowane)

            if prog is not None:
                etiuda[f"{struna_doc}_{interwal}"] = (prog, nuta)

    return etiuda

def rysuj_diagram(ax, punkty, tytul):
    img = Image.open(resource_path("static/template_gryf.jpg"))
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
        struna, interwal = klucz.split('_')
        x = sum(progi[prog]) / 2 if prog in progi else 0
        y = struna_y[struna]
        color = kolory.get(interwal, 'black')

        if interwal == 'pryma':
            ax.add_patch(patches.Rectangle((x - size / 2, y - size / 2), size, size, color=color))
        else:
            ax.add_patch(patches.Circle((x, y), size / 2, color=color))

        ax.text(x, y, nuta, ha='center', va='center', fontsize=12, color='white',
                path_effects=[path_effects.withStroke(linewidth=1.2, foreground='black')])

import matplotlib.pyplot as plt
def generuj_wizualizacje(tonika, typ):
    fig, axs = plt.subplots(6, 2, figsize=(16, 10))
    pary = [('E', 1), ('E', 2), ('A', 1), ('A', 2), ('D', 1), ('D', 2)]

    for i, (struna, przewrot) in enumerate(pary):
        akord, tercja, septyma, typ_akordu, pryma_prog_min, pozycje_akordu = buduj_akord_sztywno(tonika, struna, przewrot, typ)
        etiuda = buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ_akordu, pryma_prog_min, pozycje_akordu)
        rysuj_diagram(axs[i, 0], akord, f"Akord {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
        rysuj_diagram(axs[i, 1], etiuda, f"Etiuda dla akordu {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")

    output_path = f"static/diagram_{tonika}_{typ}.png"
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

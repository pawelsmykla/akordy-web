import os
import matplotlib.pyplot as plt
from akordy_logika import (
    buduj_akord_sztywno,
    buduj_etiude_sztywno,
    rysuj_diagram,
    rozbij_akordy_na_parametry,
    rozpoznaj_typ_akordu,
    znajdz_na_strunie
)

def zapisz_wykres(fig):
    sciezka = "static/wynik.png"
    fig.tight_layout(pad=1)
    fig.savefig(sciezka, format='png')
    plt.close(fig)
    return sciezka

def generuj_wszystkie_warianty(tonika, typ):
    pary = [('E', 1), ('E', 2), ('A', 1), ('A', 2), ('D', 1), ('D', 2)]

    fig, axs = plt.subplots(len(pary), 2, figsize=(16, len(pary) * 2.5))

    for idx, (struna, przewrot) in enumerate(pary):
        akord, tercja, septyma, typ_akordu, pryma_prog_min, pozycje = buduj_akord_sztywno(tonika, struna, przewrot, typ)
        etiuda = buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ_akordu, pryma_prog_min, pozycje)

        rysuj_diagram(axs[idx][0], akord, f"Akord {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
        rysuj_diagram(axs[idx][1], etiuda, f"Etiuda dla akordu {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")

    return zapisz_wykres(fig)

def generuj_konkretne_akordy(ciag):
    akordy = rozbij_akordy_na_parametry(ciag)
    fig, axs = plt.subplots(len(akordy), 2, figsize=(16, len(akordy) * 2.5))

    idx = 0
    for (tonika, typ, struna) in akordy:
        if struna not in ['E', 'A', 'D'] or typ is None:
            continue
        for przewrot in [1, 2]:
            akord, tercja, septyma, typ_akordu, pryma_prog_min, pozycje = buduj_akord_sztywno(tonika, struna, przewrot, typ)
            etiuda = buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ_akordu, pryma_prog_min, pozycje)

            rysuj_diagram(axs[idx][0], akord, f"Akord {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
            rysuj_diagram(axs[idx][1], etiuda, f"Etiuda dla akordu {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
            idx += 1

    return zapisz_wykres(fig)

def generuj_optymalne_akordy(ciag):
    akordy_wejsciowe = [a.strip() for a in ciag.split(",")]
    typy_strun = ['E', 'A', 'D']

    wybrane_struny = []
    ostatni_prog = None

    for akord_wej in akordy_wejsciowe:
        typ_akordu = rozpoznaj_typ_akordu(akord_wej)
        tonika = akord_wej.replace("maj7", "").replace("m7b5", "").replace("m7", "").replace("7", "")

        najlepsza_struna = None
        najblizszy_prog = None
        min_odleglosc = None

        for struna in typy_strun:
            prog = znajdz_na_strunie(struna, tonika)
            if prog is None:
                continue

            if ostatni_prog is None or min_odleglosc is None or abs(prog - ostatni_prog) < min_odleglosc:
                najlepsza_struna = struna
                najblizszy_prog = prog
                min_odleglosc = abs(prog - ostatni_prog) if ostatni_prog is not None else 0

        if najlepsza_struna is None:
            continue

        wybrane_struny.append((tonika, typ_akordu, najlepsza_struna))
        ostatni_prog = najblizszy_prog

    fig, axs = plt.subplots(len(wybrane_struny), 2, figsize=(16, len(wybrane_struny) * 2.5))

    for idx, (tonika, typ, struna) in enumerate(wybrane_struny):
        for przewrot in [1, 2]:
            akord, tercja, septyma, typ_akordu, pryma_prog_min, pozycje = buduj_akord_sztywno(tonika, struna, przewrot, typ)
            etiuda = buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ_akordu, pryma_prog_min, pozycje)

            rysuj_diagram(axs[idx][0], akord, f"Akord {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
            rysuj_diagram(axs[idx][1], etiuda, f"Etiuda dla akordu {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")

    return zapisz_wykres(fig)

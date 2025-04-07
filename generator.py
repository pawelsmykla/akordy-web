
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
import tkinter as tk
from tkinter import ttk, scrolledtext

def uruchom_gui():
    root = tk.Tk()
    root.title("Generator Akordów i Etiud dla uczniów Szkoły Muzycznej Adama Fulary. by Paweł Smykla")
    root.geometry("700x600")

    tk.Label(root, text="Wybierz typ akordu:").pack()
    typy = ['Durowy', 'Molowy', 'Dominantowy', 'Półzmniejszony']
    typ_var = tk.StringVar(value=typy[0])
    ttk.Combobox(root, textvariable=typ_var, values=typy, state="readonly").pack()

    tk.Label(root, text="Podaj tonację (np. C, D#, F#):").pack()
    tonika_entry = tk.Entry(root)
    tonika_entry.pack()

    def wygeneruj():
        tonika = tonika_entry.get().strip()
        typ = typ_var.get()
        pary = [('E', 1), ('E', 2), ('A', 1), ('A', 2), ('D', 1), ('D', 2)]

        figury = []
        for (struna, przewrot) in pary:
            fig, axs = plt.subplots(1, 2, figsize=(16, 2.5))
            akord, tercja, septyma, typ_akordu, pryma_prog_min, pozycje_akordu = buduj_akord_sztywno(tonika, struna, przewrot, typ)
            etiuda = buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ_akordu, pryma_prog_min, pozycje_akordu)
            rysuj_diagram(axs[0], akord, f"Akord {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
            rysuj_diagram(axs[1], etiuda, f"Etiuda dla akordu {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
            figury.append(fig)

        pokaz_wyniki(figury)

    tk.Button(root, text="Generuj wszystkie warianty", command=wygeneruj).pack(pady=10)

    tk.Label(root, text="Podaj konkretne akordy w poprawnej formie (Xmaj7, X7, Xm7, Xm7b5), po kazdym akordzie podaj na ktorej strunie ma byc Tonika (E, A, D), kolejny akord oddziel przecinkiem (np Amaj7 E, D7 A, Em7 A, Gm7b5 E)").pack()
    custom_entry = tk.Entry(root, width=70)
    custom_entry.pack()

    def wygeneruj_konkretne():
        ciag = custom_entry.get()
        akordy = rozbij_akordy_na_parametry(ciag)

        figury = []
        for (tonika, typ, struna) in akordy:
            if struna not in ['E', 'A', 'D'] or typ is None:
                continue
            for przewrot in [1, 2]:
                fig, axs = plt.subplots(1, 2, figsize=(16, 2.5))
                akord, tercja, septyma, typ_akordu, pryma_prog_min, pozycje_akordu = buduj_akord_sztywno(tonika, struna, przewrot, typ)
                etiuda = buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ_akordu, pryma_prog_min, pozycje_akordu)
                rysuj_diagram(axs[0], akord, f"Akord {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
                rysuj_diagram(axs[1], etiuda, f"Etiuda dla akordu {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
                figury.append(fig)

        pokaz_wyniki(figury)

    tk.Button(root, text="Generuj konkretne akordy", command=wygeneruj_konkretne).pack(pady=10)

    tk.Label(root, text="Podaj konkretne akordy w poprawnej formie (Xmaj7, X7, Xm7, Xm7b5),a spróbuję znaleźć dla nich warianty by były optymalnie blisko siebie. Akordy oddziel przecinkami.").pack(pady=10)
    custom_optimal_entry = tk.Entry(root, width=70)
    custom_optimal_entry.pack()

    def wygeneruj_optymalne():
        ciag = custom_optimal_entry.get()
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
                print(f"Nie znaleziono pozycji dla akordu {akord_wej}")
                continue

            wybrane_struny.append((tonika, typ_akordu, najlepsza_struna))
            ostatni_prog = najblizszy_prog

        figury = []
        for tonika, typ, struna in wybrane_struny:
            for przewrot in [1, 2]:
                fig, axs = plt.subplots(1, 2, figsize=(16, 2.5))
                akord, tercja, septyma, typ_akordu, pryma_prog_min, pozycje_akordu = buduj_akord_sztywno(tonika, struna, przewrot, typ)
                etiuda = buduj_etiude_sztywno(tonika, tercja, septyma, struna, przewrot, typ_akordu, pryma_prog_min, pozycje_akordu)
                rysuj_diagram(axs[0], akord, f"Akord {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
                rysuj_diagram(axs[1], etiuda, f"Etiuda dla akordu {typ} ({tonika}) na strunie {struna} - przewrót {przewrot}")
                figury.append(fig)

        pokaz_wyniki(figury)

    tk.Button(root, text="Generuj optymalnie bliskie akordy", command=wygeneruj_optymalne).pack(pady=10)

    root.mainloop()

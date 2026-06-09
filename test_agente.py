import datetime

def calcola_anno_nascita(eta_attuale, anno_corrente=None):
    if anno_corrente is None:
        anno_corrente = datetime.datetime.now().year
    return anno_corrente - eta_attuale

if __name__ == "__main__":
    # Esempio di utilizzo:
    eta = 30
    anno_nascita = calcola_anno_nascita(eta)
    print(f"Se hai {eta} anni, sei nato/a nel {anno_nascita}.")

    eta_diversa = 25
    anno_nascita_diversa = calcola_anno_nascita(eta_diversa, 2026) # Esempio con anno specifico
    print(f"Se hai {eta_diversa} anni nel 2026, sei nato/a nel {anno_nascita_diversa}.")
import requests
from bs4 import BeautifulSoup
import os
import re
from tkinter import Tk, simpledialog, filedialog

def clean_title(title):
    # Rimuovi il numero dopo il simbolo #
    cleaned_title = re.sub(r'\s*#\d+', '', title).strip()
    # Rimuovi i caratteri non validi per i nomi dei file su Windows
    cleaned_title = re.sub(r'[<>:"/\\|?*]', '', cleaned_title)
    return cleaned_title

def download_images_from_page(url, save_dir):
    # Creare la cartella se non esiste
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Ottenere il contenuto della pagina
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Errore durante il download della pagina: {response.status_code}")
        return

    # Analizzare la pagina HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Selezionare tutti i tag 'a' con la classe 'card-grid-item-card'
    card_links = soup.select('a.card-grid-item-card')

    # Iterare attraverso i link e scaricare le immagini
    for index, card_link in enumerate(card_links):
        # Trovare l'immagine all'interno del link
        img_tag = card_link.find('img')
        if img_tag and 'src' in img_tag.attrs and 'title' in img_tag.attrs:
            img_url = img_tag['src']
            img_title = img_tag['title']
            cleaned_title = clean_title(img_title)  # Pulire il titolo

            # Rimuovere qualsiasi parte dell'URL dopo il '?'
            img_url = img_url.split('?')[0]
            img_extension = os.path.splitext(img_url)[1]  # Ottieni l'estensione dell'immagine
            img_name = f"{index + 1:03} {cleaned_title}{img_extension}"  # Nome file con numero progressivo e titolo pulito

            # Scaricare l'immagine
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_path = os.path.join(save_dir, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_response.content)
                print(f"Immagine salvata: {img_name}")
            else:
                print(f"Errore durante il download dell'immagine {img_url}: {img_response.status_code}")

# Funzione principale per l'interfaccia utente
def main():
    # Inizializza la finestra Tkinter
    root = Tk()
    root.withdraw()  # Nasconde la finestra principale

    # Chiedi l'URL all'utente
    page_url = simpledialog.askstring("Input", "Inserisci l'URL della pagina web:")

    # Chiedi all'utente di selezionare una cartella di destinazione
    save_dir = filedialog.askdirectory(title="Seleziona la cartella di destinazione")

    # Verifica che l'utente abbia inserito un URL e selezionato una cartella
    if page_url and save_dir:
        download_images_from_page(page_url, save_dir)
    else:
        print("URL o cartella non specificati. Operazione annullata.")

# Avvia lo script
if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from tkinter import Tk, simpledialog, filedialog

def clean_title(title):
    # Rimuovi il numero dopo il simbolo #
    cleaned_title = re.sub(r'\s*#\d+', '', title).strip()
    # Rimuovi i caratteri non validi per i nomi dei file su Windows
    cleaned_title = re.sub(r'[<>:"/\\|?*]', '', cleaned_title)
    return cleaned_title

def process_td_content(content):
    # Usa una regular expression per trovare tutte le occorrenze tra {}
    matches = re.findall(r'\{(.*?)\}', content)
    # Unisci tutte le occorrenze in una stringa
    result_string = ''.join(matches)
    # Funzione per determinare il tipo di contenuto della stringa e restituire il risultato
    def classify_string(s):
        digits = [char for char in s if char.isdigit()]
        letters = [char for char in s if char.isalpha()]
        if digits and letters:
            unique_letters = set(letters)
            if len(unique_letters) == 1:
                return unique_letters.pop()  
            else:
                return 'M'
        elif digits:
            return 'A'
        elif letters:
            unique_letters = set(letters)
            if len(unique_letters) == 1:
                return unique_letters.pop()
            else:
                return 'M'
        else:
            return 'L'
    return classify_string(result_string)

def scrape_table_data(url):
    """Estrae i dati dalla tabella HTML e restituisce una lista di righe per il CSV."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Errore durante il download della pagina: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    # Trova la tabella nella pagina
    table = soup.find('table')
    if not table:
        print("Nessuna tabella trovata nella pagina.")
        return []
    rows = []
    for tr in table.find_all('tr'):
        cols = tr.find_all('td')
        if len(cols) >= 5:
            # Estrai e processa i dati
            set_data = cols[0].get_text(strip=True)
            number_data = cols[1].get_text(strip=True)
            name_data = cols[2].get_text(strip=True).zfill(3)
            color_data = process_td_content(cols[3].get_text(strip=True))
            rarity_data = cols[5].get_text(strip=True)
            rows.append([set_data, number_data, name_data, color_data, rarity_data])
    return rows

def download_images_from_page(url, save_dir):
    """Scarica le immagini dalla pagina web e le salva nella directory specificata."""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Errore durante il download della pagina: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    card_links = soup.select('a.card-grid-item-card')
    for index, card_link in enumerate(card_links):
        img_tag = card_link.find('img')
        if img_tag and 'src' in img_tag.attrs and 'title' in img_tag.attrs:
            img_url = img_tag['src']
            img_title = img_tag['title']
            cleaned_title = clean_title(img_title)
            img_url = img_url.split('?')[0]
            img_extension = os.path.splitext(img_url)[1]
            img_name = f"{index + 1:03} {cleaned_title}{img_extension}"
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_path = os.path.join(save_dir, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_response.content)
                print(f"Immagine salvata: {img_name}")
            else:
                print(f"Errore durante il download dell'immagine {img_url}: {img_response.status_code}")

def main():
    """Funzione principale per l'interfaccia utente e l'esecuzione dello script."""
    root = Tk()
    root.withdraw()  # Nasconde la finestra principale

    # Chiedi l'URL all'utente
    page_url = simpledialog.askstring("Input", "Inserisci l'URL della pagina web:")

    # Chiedi all'utente di selezionare una cartella di destinazione
    save_dir = filedialog.askdirectory(title="Seleziona la cartella di destinazione")

    if page_url and save_dir:
        # Estrai il nome del set dal URL per i file CSV e immagini
        set_name = re.search(r'sets/(\w+)', page_url)
        if set_name:
            set_name = set_name.group(1)
            csv_url = f"https://scryfall.com/sets/{set_name}?as=checklist"
            csv_filename = os.path.join(save_dir, f"{set_name}.csv")

            # Scarica e salva il CSV
            data = scrape_table_data(csv_url)
            if data:
                with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Set', 'Number', 'Name', 'Color', 'Rarity'])
                    writer.writerows(data)
                print(f"Dati CSV salvati nel file {csv_filename}")
            else:
                print("Nessun dato estratto dalla tabella.")

            # Scarica e salva le immagini
            download_images_from_page(page_url, save_dir)
        else:
            print("Impossibile estrarre il nome del set dall'URL.")
    else:
        print("URL o cartella non specificati. Operazione annullata.")

if __name__ == "__main__":
    main()

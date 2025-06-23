import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Frame, Label, Entry, Button, Radiobutton, StringVar
import os
import markdown2
import re
from datetime import datetime

# --- CONFIGURAZIONE PRINCIPALE ---
# Qui definiamo le impostazioni per ogni tipo di contenuto che vogliamo generare.
# "template": il file "stampino" HTML da usare.
# "content_dir": la cartella dove salveremo i file sorgente .md che scrivi.
# "output_dir": la cartella pubblica dove finiranno le pagine .html finite.
# "index_page": la pagina dell'elenco principale da aggiornare automaticamente.
CONFIG = {
    "Articolo": {
        "template": "templates/template_articolo.html",
        "content_dir": "contenuti/articoli",
        "output_dir": "istruzione",
        "index_page": "istruzione.html"
    },
    "News": {
        "template": "templates/template_news.html",
        "content_dir": "contenuti/news",
        "output_dir": "news",
        "index_page": "news.html"
    }
}


def processa_contenuto_speciale(testo_html):
    """
    Cerca nel testo HTML dei "comandi" speciali (da noi inventati) e li
    sostituisce con il codice HTML corretto e stilizzato.
    """
    # Comando per le immagini: [IMMAGINE: percorso/file.jpg "didascalia"]
    testo_html = re.sub(
        r'\[IMMAGINE:\s*(.*?)\s*"?(.*?)"?\s*\]',
        # Nota: il percorso dell'immagine è relativo alla cartella principale del sito.
        # Lo script lo rende corretto per una pagina dentro /istruzione/ o /news/.
        r'<figure class="article-image"><img src="../\1" alt="\2"><figcaption>\2</figcaption></figure>',
        testo_html,
        flags=re.IGNORECASE
    )

    # Comando per i box di commento: [COMMENTO] testo... [/COMMENTO]
    testo_html = re.sub(
        r'\[COMMENTO\]([\s\S]*?)\[/COMMENTO\]',
        # Sostituisce con il div che abbiamo già stilato nel nostro CSS.
        r'<blockquote class="comment-box"><p><strong>Nota del collettivo:</strong>\1</p></blockquote>',
        testo_html,
        flags=re.IGNORECASE
    )

    return testo_html


def aggiorna_pagina_indice(tipo_pagina):
    """
    Funzione CHIAVE: rigenera l'elenco di articoli o news nella pagina principale.
    Legge tutti i file .md, li ordina per data e aggiorna il blocco HTML
    corrispondente nella pagina indice (es. istruzione.html).
    """
    conf = CONFIG[tipo_pagina]
    content_dir = conf['content_dir']
    index_page_path = conf['index_page']
    
    # 1. Trova e leggi tutti i file di contenuto .md per questo tipo.
    if not os.path.exists(content_dir):
        print(f"Info: La cartella '{content_dir}' non esiste. Salto l'aggiornamento dell'indice.")
        return

    posts = []
    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            with open(os.path.join(content_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            
            meta_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
            if not meta_match:
                continue
            
            meta = {k.strip(): v.strip() for k, v in (line.split(':', 1) for line in meta_match.group(1).strip().split('\n') if ':' in line)}
            meta['filename'] = f"{os.path.splitext(filename)[0].lower().replace(' ', '-')}.html"
            posts.append(meta)

    # 2. Ordina i post per data, dal più recente al più vecchio.
    posts.sort(key=lambda p: p.get('data', '1970-01-01'), reverse=True)

    # 3. Genera il blocco HTML per l'elenco dei post.
    html_elenco = ""
    if tipo_pagina == "Articolo":
        placeholder_start = "<!-- START: LISTA ARTICOLI GENERATA DALLO SCRIPT -->"
        placeholder_end = "<!-- END: LISTA ARTICOLI GENERATA DALLO SCRIPT -->"
        for post in posts:
            img_path = post.get('immagine_copertina', 'images/placeholder.png') # Immagine di fallback
            html_elenco += f"""            <article class="article-card animate-on-scroll">
                <img src="{img_path}" alt="Copertina per {post.get('titolo', '')}">
                <div class="article-card-content">
                    <h3>{post.get('titolo', 'Titolo mancante')}</h3>
                    <p>{post.get('sottotitolo', '')}</p>
                    <a href="{conf['output_dir']}/{post['filename']}" class="btn btn-secondary">Leggi di più</a>
                </div>
            </article>\n"""
            
    elif tipo_pagina == "News":
        placeholder_start = "<!-- START: LISTA NEWS GENERATA DALLO SCRIPT -->"
        placeholder_end = "<!-- END: LISTA NEWS GENERATA DALLO SCRIPT -->"
        for post in posts:
            try:
                data_obj = datetime.strptime(post.get('data', '1970-01-01'), '%Y-%m-%d')
                data_ita = data_obj.strftime('%d %B %Y').capitalize()
            except ValueError:
                data_ita = post.get('data', 'Data non specificata')
            
            html_elenco += f"""            <article class="news-list-item animate-on-scroll">
                <span>{data_ita}</span>
                <h2>{post.get('titolo', 'Titolo mancante')}</h2>
                <p>{post.get('sottotitolo', '')}</p>
                <a href="{conf['output_dir']}/{post['filename']}">Leggi tutto →</a>
            </article>\n"""
    
    # 4. Leggi la pagina indice, sostituisci il blocco tra i commenti-segnaposto.
    try:
        with open(index_page_path, 'r', encoding='utf-8') as f:
            pagina_indice_html = f.read()

        # Questa RegEx trova il blocco tra i commenti e lo sostituisce
        # con il nuovo elenco, preservando i commenti stessi.
        nuova_pagina_html = re.sub(
            f"({re.escape(placeholder_start)})([\\s\\S]*?)({re.escape(placeholder_end)})",
            f"\\1\n{html_elenco}            \\3",
            pagina_indice_html
        )
        
        with open(index_page_path, 'w', encoding='utf-8') as f:
            f.write(nuova_pagina_html)
        print(f"✅ Pagina indice '{index_page_path}' aggiornata correttamente.")
            
    except FileNotFoundError:
        messagebox.showwarning("Attenzione", f"File indice non trovato: {index_page_path}\nLa pagina è stata creata, ma l'elenco non è stato aggiornato.")
    except Exception as e:
        messagebox.showerror("Errore Aggiornamento Indice", f"Impossibile aggiornare l'elenco.\nDettagli: {e}")


def crea_pagina_e_aggiorna():
    """
    Funzione principale che viene eseguita al click del bottone.
    Orchestra la creazione del file .md, la generazione dell'HTML e l'aggiornamento della pagina indice.
    """
    # 1. Raccogli i dati dalla GUI
    tipo_pagina = tipo_pagina_var.get()
    titolo = entry_titolo.get()
    sottotitolo = entry_sottotitolo.get()
    nome_file_base = entry_nome_file.get()
    data_articolo = entry_data.get()
    immagine = entry_immagine.get()
    corpo_md_raw = text_corpo.get("1.0", tk.END).strip()
    
    # 2. Valida l'input dell'utente
    if not all([tipo_pagina, titolo, nome_file_base, data_articolo]):
        messagebox.showerror("Errore di Input", "I campi 'Tipo', 'Titolo', 'Nome del File' e 'Data' sono obbligatori.")
        return

    # 3. Crea il contenuto completo per il file sorgente .md
    meta_str = f"---\ntitolo: {titolo}\nsottotitolo: {sottotitolo}\ndata: {data_articolo}\n"
    if tipo_pagina == "Articolo":
        meta_str += f"immagine_copertina: {immagine}\n"
    meta_str += "---\n\n"
    contenuto_md_completo = meta_str + corpo_md_raw
    
    # 4. Salva il file sorgente .md
    conf = CONFIG[tipo_pagina]
    content_dir = conf['content_dir']
    os.makedirs(content_dir, exist_ok=True)
    nome_file_md = f"{nome_file_base.lower().replace(' ', '-')}.md"
    percorso_md = os.path.join(content_dir, nome_file_md)
    with open(percorso_md, 'w', encoding='utf-8') as f:
        f.write(contenuto_md_completo)
        
    # 5. Genera la pagina HTML singola
    nome_file_html = f"{nome_file_base.lower().replace(' ', '-')}.html"
    percorso_output_html = os.path.join(conf['output_dir'], nome_file_html)
    
    try:
        with open(conf['template'], 'r', encoding='utf-8') as f:
            template_html = f.read()
    except FileNotFoundError:
        messagebox.showerror("Errore Critico", f"File template non trovato: {conf['template']}")
        return
        
    corpo_html_markdown = markdown2.markdown(corpo_md_raw, extras=['fenced-code-blocks', 'tables'])
    corpo_html_finale = processa_contenuto_speciale(corpo_html_markdown)
    
    pagina_html_finale = template_html.replace("{{TITOLO}}", titolo).replace("{{SOTTOTITOLO}}", sottotitolo).replace("{{CORPO_HTML}}", corpo_html_finale)
    
    os.makedirs(conf['output_dir'], exist_ok=True)
    with open(percorso_output_html, 'w', encoding='utf-8') as f:
        f.write(pagina_html_finale)
        
    # 6. Esegui la funzione chiave: aggiorna la pagina dell'elenco
    aggiorna_pagina_indice(tipo_pagina)

    messagebox.showinfo("Completato!", f"Operazione conclusa con successo:\n1. Pagina creata: {percorso_output_html}\n2. Elenco aggiornato: {conf['index_page']}")

def toggle_image_field(*args):
    """Abilita o disabilita il campo immagine in base al tipo di pagina selezionato."""
    if tipo_pagina_var.get() == "Articolo":
        entry_immagine.config(state='normal')
        label_immagine.config(state='normal')
    else:
        entry_immagine.config(state='disabled')
        label_immagine.config(state='disabled')

# --- Sezione Interfaccia Grafica (GUI) con Tkinter ---
root = tk.Tk()
root.title("Generatore Contenuti - La Giovane Fino")
root.minsize(650, 600)

frame = ttk.Frame(root, padding="15")
frame.pack(fill="both", expand=True)

# 1. Scelta Tipo
tipo_frame = ttk.LabelFrame(frame, text="1. Scegli il tipo di contenuto", padding="10")
tipo_frame.pack(fill='x', pady=(0, 10))
tipo_pagina_var = StringVar(value=None)
tipo_pagina_var.trace_add("write", toggle_image_field) # Collega la funzione al cambio
for tipo in CONFIG.keys():
    ttk.Radiobutton(tipo_frame, text=tipo, variable=tipo_pagina_var, value=tipo).pack(side='left', padx=10)

# 2. Dettagli del Post
details_frame = ttk.LabelFrame(frame, text="2. Inserisci i dettagli", padding="10")
details_frame.pack(fill='x', pady=(0, 10))
details_frame.columnconfigure(1, weight=1)

ttk.Label(details_frame, text="Titolo:").grid(row=0, column=0, sticky='w', pady=2, padx=(0,5))
entry_titolo = ttk.Entry(details_frame)
entry_titolo.grid(row=0, column=1, columnspan=3, sticky='ew')

ttk.Label(details_frame, text="Sottotitolo:").grid(row=1, column=0, sticky='w', pady=2, padx=(0,5))
entry_sottotitolo = ttk.Entry(details_frame)
entry_sottotitolo.grid(row=1, column=1, columnspan=3, sticky='ew')

ttk.Label(details_frame, text="Nome File:").grid(row=2, column=0, sticky='w', pady=2, padx=(0,5))
entry_nome_file = ttk.Entry(details_frame)
entry_nome_file.grid(row=2, column=1, sticky='ew')

ttk.Label(details_frame, text="Data:").grid(row=2, column=2, sticky='e', padx=(10,5))
entry_data = ttk.Entry(details_frame, width=15)
entry_data.insert(0, datetime.now().strftime('%Y-%m-%d'))
entry_data.grid(row=2, column=3, sticky='w')

label_immagine = ttk.Label(details_frame, text="Immagine Copertina:")
label_immagine.grid(row=3, column=0, sticky='w', pady=5, padx=(0,5))
entry_immagine = ttk.Entry(details_frame)
entry_immagine.insert(0, "images/articolo-placeholder.png")
entry_immagine.grid(row=3, column=1, columnspan=3, sticky='ew')

# 3. Corpo Articolo
body_frame = ttk.LabelFrame(frame, text="3. Scrivi il corpo del post (usa Markdown e comandi speciali)", padding="10")
body_frame.pack(fill="both", expand=True, pady=(0, 10))
text_corpo = scrolledtext.ScrolledText(body_frame, wrap=tk.WORD, height=10)
text_corpo.pack(fill="both", expand=True)

# 4. Bottone Finale
bottone_crea = ttk.Button(frame, text="Crea Pagina e Aggiorna Elenco", command=crea_pagina_e_aggiorna, style="Accent.TButton")
style = ttk.Style()
style.configure("Accent.TButton", font=("Helvetica", 10, "bold"))
bottone_crea.pack(pady=5, fill='x', ipady=5)

toggle_image_field()
root.mainloop()
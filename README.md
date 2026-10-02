# HIVE Global Advisory — sito web

Sito statico multilingua (HTML/CSS/JS puri, nessuna build necessaria a runtime) per uno studio di servizi legali, fiscali e finanziari internazionali.

## Struttura del progetto

```
site/
├── index.html              Pagina di ingresso: rileva la lingua del browser e reindirizza,
│                            con selezione manuale come alternativa (nessun JS richiesto)
├── en/                      Versione inglese — 7 pagine (LIVE)
├── it/                      Versione italiana — 7 pagine (LIVE)
├── de/ fr/ es/ ar/ ru/      Cartelle pronte, in attesa di traduzione (vedi sezione 5)
├── assets/
│   ├── logo-full.svg        Logo completo (esagono + HIVE + Global Advisory)
│   └── logo-mark.svg        Versione compatta usata nell'header (senza sottotitolo)
├── css/style.css            Foglio di stile unico, sistema di design "ink & brass"
├── js/main.js                Menu mobile, selettore lingua, anno dinamico in footer
└── README.md                 Questo file
```

Ogni lingua live contiene le stesse 7 pagine:
`index.html` (Home) · `about-us.html` · `global-presence.html` · `services.html` · `contact-us.html` · `faq.html` · `privacy.html`

---

## 1. Anteprima in locale

```bash
cd site
python3 -m http.server 8000
```
poi visita `http://localhost:8000` (reindirizza automaticamente a `/en/` o `/it/` in base alla lingua del browser).

---

## 2. Come metterlo online

Nessuna build richiesta: basta caricare il contenuto della cartella `site/` così com'è.

**Netlify (drag & drop)** — vai su [app.netlify.com/drop](https://app.netlify.com/drop) e trascina la cartella `site/`.
**Vercel / GitHub Pages** — carica il repository, nessuna build command necessaria.
**Hosting tradizionale** — carica tutti i file via FTP/SFTP mantenendo la struttura delle sottocartelle.

Una volta pubblicato, collega il dominio reale tramite le impostazioni DNS del provider.

---

## 3. Checklist prima della pubblicazione definitiva

- [ ] Sostituire indirizzi, telefoni ed email segnaposto (sedi in header/footer/contatti/presenza globale)
- [ ] Completare i profili del team in `about-us.html` / `chi-siamo` con nomi reali e numeri di iscrizione agli albi
- [ ] Far redigere i contenuti legali reali di `privacy.html` da un legale qualificato per ogni giurisdizione servita (il testo attuale è segnaposto)
- [ ] Verificare le risposte delle FAQ relative a onorari e lingue parlate (contrassegnate nel testo)
- [ ] Collegare il modulo in `contact-us.html` a un servizio reale di invio (vedi punto 4)
- [ ] Aggiornare il dominio reale nei tag `hreflang` di ogni pagina (attualmente `www.hiveglobaladvisory.example`)
- [ ] Sostituire i numeri esempio (anni di esperienza, paesi coperti, professionisti) con i dati reali dello studio
- [ ] Verificare colori/contrasti del logo su sfondi diversi da quello scuro dell'header

---

## 4. Attivare il modulo di contatto

**Netlify Forms**: aggiungi `data-netlify="true"` e `name="contact"` al tag `<form class="contact" ...>` di ogni lingua, più un campo nascosto `<input type="hidden" name="form-name" value="contact">`.

**Formspree**: cambia `action="#"` in `action="https://formspree.io/f/TUO_ID"` dopo aver creato un account su [formspree.io](https://formspree.io).

---

## 5. Aggiungere le lingue mancanti (Tedesco, Francese, Spagnolo, Arabo, Russo)

Le cartelle `de/`, `fr/`, `es/`, `ar/`, `ru/` sono già pronte nella struttura ma contengono solo un file `README.md` segnaposto: il contenuto non è ancora stato tradotto. Due percorsi possibili:

**A — Rigenerare con lo script** (consigliato)
Il sito è stato generato dallo script Python incluso `build_site.py` (richiede solo Python 3, nessuna libreria esterna), che tiene tutti i testi in dizionari per lingua (`HOME`, `ABOUT`, `GLOBAL`, `SERVICES`, `CONTACT`, `FAQ`, `PRIVACY`, in cima al file). Aggiungere una lingua significa: aggiungere le traduzioni in quei dizionari, aggiungere il codice lingua a `LIVE`, e rilanciare `python3 build_site.py`. Header, footer, tag hreflang e link del selettore lingua si aggiornano automaticamente ovunque, senza rischio di incoerenze tra le pagine. Il sito generato resta comunque puro HTML/CSS/JS statico: lo script serve solo a costruirlo, non a farlo funzionare online.

**B — Tradurre manualmente**
Copiare la cartella `en/` in `de/` (o `fr/`, `es/`, `es/`, `ar/`, `ru/`), tradurre i testi pagina per pagina mantenendo intatti tag HTML, classi ed `href`, impostare `lang="de"` nel tag `<html>` (e `dir="rtl"` per l'arabo), e aggiungere i relativi `<link rel="alternate" hreflang="...">` su **tutte** le pagine di **tutte** le lingue già pubblicate.

**Nota sull'arabo**: essendo una lingua RTL (right-to-left), oltre alla traduzione serve una verifica del layout — il CSS attuale non include ancora le regole speculari necessarie (menu, allineamenti, icone direzionali). Da testare con cura prima della pubblicazione.

Una volta pronta una nuova lingua, aggiornare anche il selettore in tutte le pagine già live: il link con classe `soon` relativo a quella lingua va trasformato in un link reale verso `../xx/pagina.html`.

---

## Note tecniche

- Font: Fraunces (titoli), IBM Plex Sans (testo), IBM Plex Mono (etichette/utility) — da Google Fonts via CDN
- Nessuna dipendenza esterna oltre ai font: nessun framework, nessun passaggio di build
- Menu mobile e FAQ realizzati in CSS/HTML puro (`<details>`/checkbox hack), funzionano anche senza JavaScript
- Il selettore lingua in header mostra tutte e 7 le lingue richieste: le due pronte sono cliccabili, le altre cinque sono segnalate come "in preparazione" finché non vengono tradotte, per non generare link rotti
- Illustrazioni (griglia a reticolo, globo con sedi) sono SVG originali disegnati per il brand, non fotografie: evitano qualsiasi problema di licenza e restano nitidi a ogni risoluzione. Se disponi di fotografie reali con diritti d'uso (sede, team), possono sostituire o affiancare questi elementi
- Rispetta `prefers-reduced-motion` e stati di focus da tastiera visibili

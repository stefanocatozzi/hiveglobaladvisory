#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore statico per il sito HIVE Global Advisory.
Produce file HTML puri (nessuna dipendenza a runtime) per ogni lingua live,
con header/footer/hreflang coerenti. Le lingue non ancora tradotte restano
scaffolded (cartella pronta) e compaiono nel selettore come "in preparazione".
"""
import os

ROOT = "/home/claude/site"

LANGS = {
    "en": {"native": "English",  "dir": "ltr", "soon": "soon"},
    "it": {"native": "Italiano", "dir": "ltr", "soon": "presto"},
    "de": {"native": "Deutsch",  "dir": "ltr", "soon": "soon"},
    "fr": {"native": "Français", "dir": "ltr", "soon": "soon"},
    "es": {"native": "Español",  "dir": "ltr", "soon": "soon"},
    "ar": {"native": "العربية",  "dir": "rtl", "soon": "soon"},
    "ru": {"native": "Русский",  "dir": "ltr", "soon": "soon"},
}
LIVE = ["en", "it"]
PAGES = ["index", "about-us", "global-presence", "services", "contact-us", "faq", "privacy"]

NAV = {
    "en": {"index": "Home", "about-us": "About us", "global-presence": "Global presence",
           "services": "Services", "contact-us": "Contact us", "faq": "FAQ", "privacy": "Privacy"},
    "it": {"index": "Home", "about-us": "Chi siamo", "global-presence": "Presenza globale",
           "services": "Servizi", "contact-us": "Contatti", "faq": "FAQ", "privacy": "Privacy"},
}
CTA_LABEL = {"en": "Request a consultation", "it": "Richiedi una consulenza"}
SOON_TAG = {"en": "soon", "it": "presto"}

OFFICES = {
    "en": [
        ("Shanghai", "[Address], Shanghai, China", "+86 21 0000 0000", "shanghai@hiveglobaladvisory.example"),
        ("Ho Chi Minh City", "[Address], Ho Chi Minh City, Vietnam", "+84 28 0000 0000", "hcmc@hiveglobaladvisory.example"),
        ("Mumbai", "[Address], Mumbai, India", "+91 22 0000 0000", "mumbai@hiveglobaladvisory.example"),
        ("Dubai", "[Address], Dubai, United Arab Emirates", "+971 4 000 0000", "dubai@hiveglobaladvisory.example"),
        ("Milan", "Via [Address], 20100 Milan, Italy", "+39 02 0000 0000", "milan@hiveglobaladvisory.example"),
    ],
    "it": [
        ("Shanghai", "[Indirizzo], Shanghai, Cina", "+86 21 0000 0000", "shanghai@hiveglobaladvisory.example"),
        ("Ho Chi Minh City", "[Indirizzo], Ho Chi Minh City, Vietnam", "+84 28 0000 0000", "hcmc@hiveglobaladvisory.example"),
        ("Mumbai", "[Indirizzo], Mumbai, India", "+91 22 0000 0000", "mumbai@hiveglobaladvisory.example"),
        ("Dubai", "[Indirizzo], Dubai, Emirati Arabi Uniti", "+971 4 000 0000", "dubai@hiveglobaladvisory.example"),
        ("Milano", "Via [Indirizzo], 20100 Milano, Italia", "+39 02 0000 0000", "milano@hiveglobaladvisory.example"),
    ],
}
TICKER = {
    "en": [("Shanghai", "+8"), ("Ho Chi Minh City", "+7"), ("Mumbai", "+5:30"), ("Dubai", "+4"), ("Milan", "+1")],
    "it": [("Shanghai", "+8"), ("Ho Chi Minh City", "+7"), ("Mumbai", "+5:30"), ("Dubai", "+4"), ("Milano", "+1")],
}

FOOT = {
    "en": {"offices": "Offices", "services": "Services", "company": "Company",
           "rights": "All rights reserved.", "privacy": "Privacy", "contact": "Contact us", "about": "About us"},
    "it": {"offices": "Sedi", "services": "Aree di competenza", "company": "Studio",
           "rights": "Tutti i diritti riservati.", "privacy": "Privacy", "contact": "Contatti", "about": "Chi siamo"},
}

SERVICES = {
    "en": [
        {"ref": "§ I", "id": "corporate", "title": "Corporate &amp; commercial law",
         "intro": "We advise Italian and international businesses on incorporation, management and corporate reorganisation, with particular attention to cross-border transactions.",
         "items": ["Incorporation of companies and foreign subsidiaries", "International commercial contracts",
                    "Corporate governance", "Corporate restructuring", "Regulatory compliance"]},
        {"ref": "§ II", "id": "tax", "title": "International taxation",
         "intro": "We assist companies and individuals with cross-border tax planning, relations with tax authorities in multiple countries, and preventing the risk of double taxation.",
         "items": ["International tax planning", "Transfer pricing", "Double taxation treaties",
                    "Multi-jurisdictional tax compliance", "Assistance with audits and international tax disputes"]},
        {"ref": "§ III", "id": "wealth", "title": "Wealth management",
         "intro": "We support private clients, entrepreneurial families and institutional investors in estate planning and managing portfolios with international exposure.",
         "items": ["Estate and succession planning", "Structuring trusts and investment vehicles",
                    "International asset allocation", "Financial relocation", "Consolidated wealth reporting"]},
        {"ref": "§ IV", "id": "ma", "title": "M&amp;A &amp; due diligence",
         "intro": "We support the full lifecycle of extraordinary transactions, from deal structuring to legal and tax due diligence, through to closing.",
         "items": ["Legal, tax and financial due diligence", "Deal structuring", "M&amp;A negotiation and contracts",
                    "Post-merger integration", "International joint ventures"]},
    ],
    "it": [
        {"ref": "§ I", "id": "corporate", "title": "Diritto societario e commerciale",
         "intro": "Assistiamo imprese italiane e internazionali nella costituzione, gestione e riorganizzazione societaria, con particolare attenzione alle operazioni cross-border.",
         "items": ["Costituzione di società e filiali estere", "Contrattualistica commerciale internazionale",
                    "Corporate governance", "Ristrutturazioni societarie", "Compliance regolamentare"]},
        {"ref": "§ II", "id": "tax", "title": "Fiscalità internazionale",
         "intro": "Assistiamo aziende e privati nella pianificazione fiscale transnazionale, nella gestione dei rapporti con le amministrazioni finanziarie di più paesi e nella prevenzione dei rischi di doppia imposizione.",
         "items": ["Pianificazione fiscale internazionale", "Transfer pricing", "Convenzioni contro le doppie imposizioni",
                    "Compliance fiscale multi-giurisdizionale", "Assistenza in verifiche e contenzioso fiscale internazionale"]},
        {"ref": "§ III", "id": "wealth", "title": "Wealth management",
         "intro": "Affianchiamo privati, famiglie imprenditoriali e investitori istituzionali nella pianificazione patrimoniale e nella gestione di portafogli con esposizione internazionale.",
         "items": ["Pianificazione patrimoniale e successoria", "Strutturazione di trust e veicoli di investimento",
                    "Asset allocation internazionale", "Relocation finanziaria", "Reportistica patrimoniale consolidata"]},
        {"ref": "§ IV", "id": "ma", "title": "M&amp;A e due diligence",
         "intro": "Supportiamo l'intero ciclo delle operazioni straordinarie, dalla strutturazione dell'operazione alla due diligence legale e fiscale, fino al closing.",
         "items": ["Due diligence legale, fiscale e finanziaria", "Strutturazione dell'operazione",
                    "Negoziazione e contrattualistica di M&amp;A", "Post-merger integration", "Joint venture internazionali"]},
    ],
}

FAQS = {
    "en": [
        ("What services does HIVE Global Advisory provide?",
         "We provide integrated legal, tax and financial advisory services for cross-border business and private clients, spanning corporate &amp; commercial law, international taxation, wealth management, and M&amp;A &amp; due diligence. Our team coordinates across disciplines so you have a single point of contact for complex, multi-jurisdiction matters."),
        ("Which countries and regions do you operate in?",
         "We operate directly from our offices in Shanghai, Ho Chi Minh City, Mumbai, Dubai and Milan, and work through a vetted network of correspondent firms across North America, Latin America, the Middle East, Europe and Asia-Pacific. See our Global presence page for the full picture."),
        ("How does a first consultation work?",
         "Share a short description of your situation through our contact form, and a member of our team will reach out within 1-2 business days to arrange an introductory call at no obligation."),
        ("Do you work with both companies and individuals?",
         "Yes. We advise multinational companies and SMEs expanding abroad, as well as private individuals and families with cross-border assets, income or residency matters."),
        ("How are your fees structured?",
         "Fees depend on the scope, complexity and jurisdictions involved. We agree the fee structure — hourly, fixed-fee or retainer — with each client before any work begins, so there are no surprises.",
         "Customise with the firm&rsquo;s actual fee policy."),
        ("Is my information kept confidential?",
         "Absolutely. Confidentiality is a professional obligation for every member of our team, and all client information is handled under strict internal data-protection and ethical-conduct policies. See our Privacy page for details."),
        ("In which languages can I be assisted?",
         "Our team is genuinely multilingual; depending on the matter and the professional involved, we typically assist clients in English, Italian, French, German, Spanish, Russian and Arabic.",
         "Verify the language combinations actually covered by the real team."),
        ("How do I get started?",
         "The fastest way is through our contact form — tell us briefly what you need, and the right professional on our team will follow up directly."),
    ],
    "it": [
        ("Quali servizi offre HIVE Global Advisory?",
         "Offriamo una consulenza legale, fiscale e finanziaria integrata per aziende e privati con interessi internazionali, che copre diritto societario e commerciale, fiscalità internazionale, wealth management e M&amp;A/due diligence. Il nostro team coordina le diverse competenze per darti un unico punto di riferimento anche sui dossier più complessi."),
        ("In quali paesi e aree geografiche operate?",
         "Operiamo direttamente dalle nostre sedi di Shanghai, Ho Chi Minh City, Mumbai, Dubai e Milano, e ci avvaliamo di una rete selezionata di corrispondenti in Nord America, America Latina, Medio Oriente, Europa e Asia-Pacifico. Trovi il quadro completo nella pagina Presenza globale."),
        ("Come funziona una prima consulenza?",
         "Descrivi brevemente la tua esigenza tramite il modulo di contatto: un membro del nostro team ti risponderà entro 1-2 giorni lavorativi per fissare una prima chiamata conoscitiva, senza impegno."),
        ("Lavorate sia con aziende che con privati?",
         "Sì. Affianchiamo aziende multinazionali e PMI in fase di espansione internazionale, così come privati e famiglie con patrimoni, redditi o questioni di residenza transnazionali."),
        ("Come sono strutturati i vostri onorari?",
         "Gli onorari dipendono dall'ambito, dalla complessità e dalle giurisdizioni coinvolte. Concordiamo la struttura tariffaria — a ore, a forfait o a retainer — con ogni cliente prima di iniziare qualsiasi attività, senza sorprese.",
         "Personalizza con la politica tariffaria reale dello studio."),
        ("Le mie informazioni sono trattate in modo riservato?",
         "Assolutamente sì. La riservatezza è un obbligo professionale per ogni membro del team, e tutte le informazioni dei clienti sono trattate secondo rigorose policy interne di protezione dei dati e deontologia professionale. Trovi maggiori dettagli nella pagina Privacy."),
        ("In quali lingue posso essere assistito/a?",
         "Il nostro team è realmente multilingue: a seconda del dossier e del professionista coinvolto, assistiamo generalmente i clienti in italiano, inglese, francese, tedesco, spagnolo, russo e arabo.",
         "Verifica le combinazioni linguistiche effettivamente coperte dal team reale."),
        ("Come posso iniziare?",
         "Il modo più rapido è compilare il modulo di contatto: descrivi brevemente cosa ti serve e il professionista più indicato del nostro team ti risponderà direttamente."),
    ],
}

TEAM = {
    "en": [("MP", "Managing Partner — Corporate law"), ("PF", "Partner — International taxation"),
           ("WM", "Partner — Wealth management"), ("MA", "Senior Associate — M&amp;A &amp; due diligence")],
    "it": [("MP", "Managing Partner — Diritto societario"), ("PF", "Partner — Fiscalità internazionale"),
           ("WM", "Partner — Wealth management"), ("MA", "Senior Associate — M&amp;A e due diligence")],
}

print("Config loaded OK")

HOME = {
    "en": {
        "eyebrow": "International legal, tax and financial advisory",
        "h1": "Standing beside businesses that operate beyond borders",
        "lede": "A multidisciplinary team of lawyers, chartered accountants and financial advisors serving companies and individuals with interests across multiple jurisdictions.",
        "cta_secondary": "Explore our services",
        "services_eyebrow": "How we can help",
        "services_h2": "Integrated support, one point of contact",
        "services_p": "We cover the legal, tax and financial sides of international operations with a single coordinated team.",
        "why_eyebrow": "Why choose us",
        "why_h2": "An approach built for cross-border work",
        "facts": [("International network", "Vetted correspondents across North America, Latin America, the Middle East, Europe and Asia-Pacific."),
                  ("Integrated team", "One point of contact for legal, tax and financial expertise."),
                  ("Confidentiality", "Professional rigour on every file, without exception."),
                  ("Active since 2005", "Advising on cross-border matters for two decades.")],
        "gp_eyebrow": "Global presence",
        "gp_h2": "Rooted in multiple jurisdictions",
        "gp_p": "Offices in Shanghai, Ho Chi Minh City, Mumbai, Dubai and Milan, backed by a correspondent network spanning five continents.",
        "gp_cta": "See our global presence",
        "team_eyebrow": "The team",
        "team_h2": "A team that speaks your language — literally",
        "team_p": "Multilingual professionals, with verifiable qualifications and years of practice on international files.",
        "team_cta": "Meet the team",
        "faq_eyebrow": "FAQ",
        "faq_h2": "Common questions",
        "faq_cta": "View all FAQs",
        "cta_h2": "Have an international project?",
        "cta_p": "Let&rsquo;s talk about it.",
        "cta_btn": "Contact us",
    },
    "it": {
        "eyebrow": "Consulenza legale, fiscale e finanziaria internazionale",
        "h1": "Al fianco delle aziende che operano oltre confine",
        "lede": "Un team multidisciplinare di avvocati, commercialisti e consulenti finanziari al servizio di imprese e privati con interessi in più giurisdizioni.",
        "cta_secondary": "Scopri i nostri servizi",
        "services_eyebrow": "Come possiamo aiutarti",
        "services_h2": "Un supporto integrato, un unico interlocutore",
        "services_p": "Copriamo gli aspetti legali, fiscali e finanziari delle operazioni internazionali con un unico team coordinato.",
        "why_eyebrow": "Perché sceglierci",
        "why_h2": "Un approccio pensato per il cross-border",
        "facts": [("Rete internazionale", "Corrispondenti selezionati in Nord America, America Latina, Medio Oriente, Europa e Asia-Pacifico."),
                  ("Team integrato", "Un solo interlocutore per competenze legali, fiscali e finanziarie."),
                  ("Riservatezza", "Rigore professionale su ogni dossier, senza eccezioni."),
                  ("Attivi dal 2005", "Al fianco dei clienti nelle operazioni cross-border da due decenni.")],
        "gp_eyebrow": "Presenza globale",
        "gp_h2": "Radicati in più giurisdizioni",
        "gp_p": "Sedi a Shanghai, Ho Chi Minh City, Mumbai, Dubai e Milano, affiancate da una rete di corrispondenti su cinque continenti.",
        "gp_cta": "Scopri la nostra presenza globale",
        "team_eyebrow": "Il team",
        "team_h2": "Un team che parla la tua lingua — letteralmente",
        "team_p": "Professionisti multilingue, con qualifiche verificabili e anni di pratica su dossier internazionali.",
        "team_cta": "Conosci il team",
        "faq_eyebrow": "FAQ",
        "faq_h2": "Domande frequenti",
        "faq_cta": "Vedi tutte le FAQ",
        "cta_h2": "Hai un progetto internazionale?",
        "cta_p": "Parliamone insieme.",
        "cta_btn": "Contattaci",
    },
}

ABOUT = {
    "en": {
        "eyebrow": "About us", "h1": "A single point of contact for cross-border business challenges",
        "lede": "HIVE Global Advisory was founded in 2005 to give companies and individuals one point of reference for the legal, tax and financial challenges that come with operating across borders. Since then, we have supported our clients with an integrated, rigorous, results-driven approach.",
        "values_eyebrow": "Our values", "values_h2": "Four principles behind every engagement",
        "values": [("Integrity", "Confidentiality and fairness at every stage of the relationship."),
                   ("Integrated approach", "One team, combined legal, tax and financial expertise."),
                   ("International outlook", "Local roots, global perspective on every matter."),
                   ("Constant updates", "We track regulatory change in every jurisdiction we operate in.")],
        "team_eyebrow": "The team", "team_h2": "Multilingual professionals, verifiable qualifications",
        "team_p": "Every member of the team is registered with the relevant professional body. Replace these placeholder profiles with your real professionals&rsquo; details.",
        "cta_h2": "Want to get to know the team better?", "cta_p": "Let&rsquo;s set up an introductory call.",
        "cta_btn": "Contact us",
    },
    "it": {
        "eyebrow": "Chi siamo", "h1": "Un interlocutore unico per le sfide del business internazionale",
        "lede": "HIVE Global Advisory nasce nel 2005 dall'esigenza di offrire a imprese e privati un punto di riferimento unico per le questioni legali, fiscali e finanziarie che nascono dall'operare in più paesi. Da allora affianchiamo i nostri clienti con un approccio integrato, rigoroso e orientato al risultato.",
        "values_eyebrow": "I nostri valori", "values_h2": "Quattro principi che guidano ogni dossier",
        "values": [("Integrità", "Riservatezza e correttezza in ogni fase della collaborazione."),
                   ("Approccio integrato", "Un solo team, competenze legali, fiscali e finanziarie unite."),
                   ("Visione internazionale", "Radicamento locale, prospettiva globale su ogni operazione."),
                   ("Aggiornamento costante", "Monitoriamo l'evoluzione normativa in ogni giurisdizione in cui operiamo.")],
        "team_eyebrow": "Il team", "team_h2": "Professionisti multilingue, qualifiche verificabili",
        "team_p": "Ogni membro del team è iscritto ai rispettivi albi professionali di riferimento. Sostituisci questi profili segnaposto con i dati reali dei tuoi professionisti.",
        "cta_h2": "Vuoi conoscere il team più da vicino?", "cta_p": "Fissiamo una prima chiamata conoscitiva.",
        "cta_btn": "Contattaci",
    },
}

GLOBAL = {
    "en": {
        "eyebrow": "Global presence", "h1": "Rooted in multiple jurisdictions, built for cross-border work",
        "lede": "We combine offices we operate directly with a vetted network of correspondent firms, so you get qualified, coordinated support wherever your business takes you.",
        "offices_eyebrow": "Our offices", "offices_h2": "Where to find us",
        "network_eyebrow": "Correspondent network", "network_h2": "Qualified support, five continents",
        "network_p": "Beyond our own offices, we work with a carefully selected network of independent law firms, tax advisors and financial professionals across North America, Latin America, the Middle East, Europe and Asia-Pacific — vetted for quality and briefed directly by our team on every engagement.",
        "regions": [("Europe", "Direct presence in Milan, with extensive coverage across the EU, the UK and Switzerland."),
                    ("North America", "Correspondents in the United States and Canada."),
                    ("Latin America", "Partners across the region&rsquo;s main financial centres."),
                    ("Middle East", "Direct presence in Dubai, with correspondents across the Gulf&rsquo;s key business hubs."),
                    ("Asia-Pacific", "Direct presence in Shanghai, Ho Chi Minh City and Mumbai, with correspondents across the wider region.")],
        "cta_h2": "Operating in a country you don&rsquo;t see listed?",
        "cta_p": "Ask us — our network likely reaches there too.", "cta_btn": "Contact us",
    },
    "it": {
        "eyebrow": "Presenza globale", "h1": "Radicati in più giurisdizioni, pensati per il cross-border",
        "lede": "Uniamo le sedi in cui operiamo direttamente a una rete selezionata di corrispondenti, per garantirti un supporto qualificato e coordinato ovunque il tuo business ti porti.",
        "offices_eyebrow": "Le nostre sedi", "offices_h2": "Dove trovarci",
        "network_eyebrow": "Rete di corrispondenti", "network_h2": "Supporto qualificato, cinque continenti",
        "network_p": "Oltre alle nostre sedi, ci avvaliamo di una rete accuratamente selezionata di studi legali indipendenti, consulenti fiscali e professionisti finanziari in Nord America, America Latina, Medio Oriente, Europa e Asia-Pacifico — verificati per qualità e coordinati direttamente dal nostro team su ogni incarico.",
        "regions": [("Europa", "Presenza diretta a Milano, con copertura estesa su UE, Regno Unito e Svizzera."),
                    ("Nord America", "Corrispondenti negli Stati Uniti e in Canada."),
                    ("America Latina", "Partner nei principali centri finanziari della regione."),
                    ("Medio Oriente", "Presenza diretta a Dubai, con corrispondenti nei principali hub economici del Golfo."),
                    ("Asia-Pacifico", "Presenza diretta a Shanghai, Ho Chi Minh City e Mumbai, con corrispondenti su tutta l'area.")],
        "cta_h2": "Operi in un paese che non vedi elencato?",
        "cta_p": "Chiedici: la nostra rete probabilmente arriva anche lì.", "cta_btn": "Contattaci",
    },
}

CONTACT = {
    "en": {
        "eyebrow": "Contact us", "h1": "Let&rsquo;s talk about your project",
        "lede": "Our team is available for an initial assessment of your needs. Fill in the form or contact us directly at one of our offices.",
        "f_first": "First name", "f_last": "Last name", "f_email": "Email", "f_phone": "Phone",
        "f_country": "Country", "f_area": "Area of interest", "f_area_ph": "Select an area",
        "f_message": "Message", "f_privacy": "I have read the ",
        "f_privacy_link": "privacy notice", "f_privacy_end": " and consent to my data being processed so I can be contacted back.",
        "f_submit": "Send request",
        "f_note": "We reply within 1-2 business days. Please do not include sensitive data in this form.",
        "offices_eyebrow": "Our offices", "offices_h2": "Where to find us",
    },
    "it": {
        "eyebrow": "Contatti", "h1": "Parliamo del tuo progetto",
        "lede": "Il nostro team è a disposizione per una prima valutazione della tua esigenza. Compila il modulo o contattaci direttamente presso una delle nostre sedi.",
        "f_first": "Nome", "f_last": "Cognome", "f_email": "Email", "f_phone": "Telefono",
        "f_country": "Paese", "f_area": "Area di interesse", "f_area_ph": "Seleziona un'area",
        "f_message": "Messaggio", "f_privacy": "Ho letto l&rsquo;",
        "f_privacy_link": "informativa privacy", "f_privacy_end": " e acconsento al trattamento dei miei dati per essere ricontattato/a.",
        "f_submit": "Invia richiesta",
        "f_note": "Rispondiamo entro 1-2 giorni lavorativi. I campi con dati sensibili non devono essere inclusi in questo modulo.",
        "offices_eyebrow": "Le nostre sedi", "offices_h2": "Dove trovarci",
    },
}

PRIVACY = {
    "en": {
        "eyebrow": "Legal document", "h1": "Privacy policy",
        "notice": "This is a placeholder page. The actual privacy notice must be drafted by a qualified lawyer based on the firm&rsquo;s real data processing activities, GDPR and the local regulations applicable in every country served.",
        "sections": [
            ("Data controller", "[Legal name of the firm], with registered office at [address], is the controller of personal data collected through this site."),
            ("Categories of data collected", "[List the categories of data collected through contact forms, technical and analytics cookies, etc.]"),
            ("Purposes of processing", "[Describe the purposes: responding to consultation requests, managing the contractual relationship, legal obligations.]"),
            ("Cookies", "[Summary of technical and third-party cookies used, or a link to a dedicated cookie section/banner.]"),
            ("Your rights", "[Rights under GDPR and/or applicable local regulations: access, rectification, erasure, portability, objection.]"),
            ("Company &amp; legal information", "[Legal name, registered office, company registration number, VAT/tax ID, and professional registration numbers of the partners in each relevant jurisdiction.]"),
            ("Contact", "To exercise your rights or for any question about data processing, please write to [firm&rsquo;s privacy email]."),
        ],
    },
    "it": {
        "eyebrow": "Documento legale", "h1": "Privacy policy",
        "notice": "Questa è una pagina segnaposto. Il testo dell'informativa privacy deve essere redatto da un legale qualificato in base al trattamento dati effettivo dello studio, al GDPR e alle normative locali applicabili in ogni paese servito.",
        "sections": [
            ("Titolare del trattamento", "[Ragione sociale dello studio], con sede in [indirizzo], è titolare del trattamento dei dati personali raccolti tramite questo sito."),
            ("Tipologie di dati raccolti", "[Elenco delle categorie di dati raccolti tramite moduli di contatto, cookie tecnici e di analisi, ecc.]"),
            ("Finalità del trattamento", "[Descrizione delle finalità: rispondere a richieste di consulenza, gestione del rapporto contrattuale, adempimenti di legge.]"),
            ("Cookie", "[Riepilogo dei cookie tecnici e di terze parti utilizzati, oppure link a una sezione/banner cookie dedicato.]"),
            ("Diritti dell'interessato", "[Diritti previsti dal GDPR e/o dalle normative locali applicabili: accesso, rettifica, cancellazione, portabilità, opposizione.]"),
            ("Dati societari e iscrizioni professionali", "[Ragione sociale, sede legale, numero di iscrizione al registro imprese, partita IVA, e numeri di iscrizione agli albi professionali dei soci in ciascuna giurisdizione rilevante.]"),
            ("Contatti", "Per esercitare i propri diritti o per qualsiasi richiesta relativa al trattamento dei dati, è possibile scrivere a [email privacy dello studio]."),
        ],
    },
}
print("Content dictionaries loaded OK")

# ---------------------------------------------------------------- helpers

def graticule_svg(cls):
    return (f'<svg class="{cls}" width="100%" height="100%" aria-hidden="true">'
            f'<defs><pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse">'
            f'<path d="M 64 0 L 0 0 0 64" fill="none" stroke="#B98A3E" stroke-width="0.5"/>'
            f'</pattern></defs><rect width="100%" height="100%" fill="url(#grid)"/></svg>')

def globe_svg(lang):
    milan = "Milano" if lang == "it" else "Milan"
    return f'''<svg class="globe" viewBox="0 0 420 420" aria-hidden="true">
      <circle class="rim" cx="210" cy="210" r="170"/>
      <ellipse class="meridian" cx="210" cy="210" rx="110" ry="170"/>
      <ellipse class="meridian" cx="210" cy="210" rx="55" ry="170"/>
      <line class="meridian" x1="55.1" y1="140" x2="364.9" y2="140"/>
      <line class="meridian" x1="55.1" y1="280" x2="364.9" y2="280"/>
      <line class="meridian" x1="100.5" y1="80" x2="319.5" y2="80"/>
      <line class="meridian" x1="100.5" y1="340" x2="319.5" y2="340"/>
      <g><circle class="pin-ring" cx="150" cy="110" r="9"/><circle class="pin" cx="150" cy="110" r="4"/>
        <text x="164" y="107">{milan.upper()}</text></g>
      <g><circle class="pin-ring" cx="95" cy="175" r="9"/><circle class="pin" cx="95" cy="175" r="4"/>
        <text x="109" y="172">DUBAI</text></g>
      <g><circle class="pin-ring" cx="120" cy="250" r="9"/><circle class="pin" cx="120" cy="250" r="4"/>
        <text x="134" y="247">MUMBAI</text></g>
      <g><circle class="pin-ring" cx="260" cy="270" r="9"/><circle class="pin" cx="260" cy="270" r="4"/>
        <text x="274" y="267">HCMC</text></g>
      <g><circle class="pin-ring" cx="295" cy="160" r="9"/><circle class="pin" cx="295" cy="160" r="4"/>
        <text x="309" y="157">SHANGHAI</text></g>
    </svg>'''

def ticker_html(lang):
    stops = "\n    ".join(
        f'<span class="stop"><span class="city">{c}</span><span class="tz">UTC {t}</span></span>'
        for c, t in TICKER[lang])
    return f'<div class="ticker on-ink">\n  <div class="wrap">\n    {stops}\n  </div>\n</div>'

def facts_html(facts):
    return "\n    ".join(f'<div class="fact"><h3>{t}</h3><p>{d}</p></div>' for t, d in facts)

def services_teaser_html(lang):
    learn = "Learn more" if lang == "en" else "Scopri di più"
    cards = []
    for s in SERVICES[lang]:
        blurb = s["intro"].split(". ")[0].rstrip(".") + "."
        cards.append(f'''<div class="article">
        <span class="ref">{s["ref"]}</span>
        <h3>{s["title"]}</h3>
        <p>{blurb}</p>
        <a class="more" href="services.html#{s["id"]}">{learn} \u2192</a>
      </div>''')
    return "\n      ".join(cards)

def faq_items_html(items):
    out = []
    for item in items:
        q, a = item[0], item[1]
        note = item[2] if len(item) > 2 else None
        note_html = f'<span class="note">{note}</span>' if note else ""
        out.append(f'''<details class="faq-item">
        <summary>{q} <span class="plus">+</span></summary>
        <div class="answer">{a}{note_html}</div>
      </details>''')
    return "\n      ".join(out)

def offices_grid_html(lang, cls="offices-4"):
    cards = []
    for name, addr, phone, email in OFFICES[lang]:
        cards.append(f'''<div class="office-card">
        <div class="city">{name}</div>
        <p>{addr}</p>
        <p>{phone}</p>
        <p>{email}</p>
      </div>''')
    return f'<div class="{cls}">\n      ' + "\n      ".join(cards) + "\n    </div>"

def hreflang_tags(active_page):
    base = "https://www.hiveglobaladvisory.example"
    tags = [f'<link rel="alternate" hreflang="{c}" href="{base}/{c}/{active_page}.html">' for c in LIVE]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{base}/en/{active_page}.html">')
    return "\n".join(tags)

def lang_menu_html(lang, active_page):
    items = []
    for code, meta in LANGS.items():
        cur = ' aria-current="true"' if code == lang else ''
        if code in LIVE:
            items.append(f'<a href="../{code}/{active_page}.html"{cur}>{meta["native"]}</a>')
        else:
            items.append(f'<a class="soon" href="#" aria-disabled="true">{meta["native"]} <span class="tag">{SOON_TAG[lang]}</span></a>')
    return "\n          ".join(items)

def nav_html(lang, active_page):
    items = []
    for p in PAGES:
        cur = ' aria-current="page"' if p == active_page else ''
        items.append(f'<a href="{p}.html"{cur}>{NAV[lang][p]}</a>')
    return "\n      ".join(items)

def header_html(lang, active_page):
    return f'''<header class="site">
  <div class="wrap bar">
    <a href="index.html" class="mark">
      <img src="../assets/logo-mark.svg" alt="HIVE Global Advisory" width="36" height="36">
      <span class="wordmark"><b>HIVE</b><span>GLOBAL ADVISORY</span></span>
    </a>
    <input type="checkbox" id="nav-toggle">
    <label for="nav-toggle" class="nav-btn">Menu</label>
    <nav class="primary">
      {nav_html(lang, active_page)}
      <details class="lang-switch">
        <summary>{lang.upper()} <span class="chev">\u25be</span></summary>
        <div class="lang-menu">
          {lang_menu_html(lang, active_page)}
        </div>
      </details>
      <a href="contact-us.html" class="btn btn-solid">{CTA_LABEL[lang]}</a>
    </nav>
  </div>
</header>'''

def footer_html(lang):
    f = FOOT[lang]
    office_html = "\n        ".join(
        f'<div class="office"><span class="city">{name}</span><br>{addr}<br>{phone}</div>'
        for name, addr, phone, email in OFFICES[lang])
    services_links = "\n          ".join(
        f'<li><a href="services.html#{s["id"]}">{s["title"]}</a></li>' for s in SERVICES[lang])
    return f'''<footer class="site">
  <div class="wrap">
    <div class="grid">
      <div>
        <h4>{f["offices"]}</h4>
        {office_html}
      </div>
      <div>
        <h4>{f["services"]}</h4>
        <ul>
          {services_links}
        </ul>
      </div>
      <div>
        <h4>{f["company"]}</h4>
        <ul>
          <li><a href="about-us.html">{f["about"]}</a></li>
          <li><a href="contact-us.html">{f["contact"]}</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="privacy.html">{f["privacy"]}</a></li>
        </ul>
      </div>
    </div>
    <div class="bottom">
      <span>&copy; <span id="year">2026</span> HIVE Global Advisory. {f["rights"]}</span>
      <span>{" \u00b7 ".join(o[0] for o in OFFICES[lang])}</span>
    </div>
  </div>
</footer>
<script src="../js/main.js"></script>'''

def page_shell(lang, active_page, title, desc, hero_html, body_html):
    meta = LANGS[lang]
    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{meta["dir"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
{hreflang_tags(active_page)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>

{header_html(lang, active_page)}

{hero_html}

{body_html}

{footer_html(lang)}
</body>
</html>
'''
print("Helpers loaded OK")

# ---------------------------------------------------------------- page builders

def build_index(lang):
    h = HOME[lang]
    title = "HIVE Global Advisory" + (
        " \u2014 International legal, tax and financial advisory" if lang == "en"
        else " \u2014 Consulenza legale, fiscale e finanziaria internazionale")
    hero = f'''<section class="hero on-ink">
  {graticule_svg("graticule")}
  <div class="wrap">
    <span class="eyebrow">{h["eyebrow"]}</span>
    <h1>{h["h1"]}</h1>
    <p class="lede">{h["lede"]}</p>
    <div class="cta-row">
      <a href="contact-us.html" class="btn btn-solid">{CTA_LABEL[lang]}</a>
      <a href="services.html" class="btn btn-ghost">{h["cta_secondary"]}</a>
    </div>
  </div>
</section>
{ticker_html(lang)}'''
    body = f'''<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{h["services_eyebrow"]}</span>
      <h2>{h["services_h2"]}</h2>
      <p>{h["services_p"]}</p>
    </div>
    <div class="articles">
      {services_teaser_html(lang)}
    </div>
  </div>
</section>

<section style="padding-top:0;">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{h["why_eyebrow"]}</span>
      <h2>{h["why_h2"]}</h2>
    </div>
  </div>
  <div class="facts">
    {facts_html(h["facts"])}
  </div>
</section>

<section class="on-ink">
  <div class="wrap team-split">
    <div class="copy">
      <span class="eyebrow">{h["gp_eyebrow"]}</span>
      <h2>{h["gp_h2"]}</h2>
      <p class="lede-sm">{h["gp_p"]}</p>
    </div>
    <a href="global-presence.html" class="btn btn-ghost">{h["gp_cta"]}</a>
  </div>
</section>

<section>
  <div class="wrap team-split">
    <div class="copy">
      <span class="eyebrow">{h["team_eyebrow"]}</span>
      <h2>{h["team_h2"]}</h2>
      <p>{h["team_p"]}</p>
    </div>
    <a href="about-us.html" class="btn btn-ghost">{h["team_cta"]}</a>
  </div>
</section>

<section class="on-ink">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{h["faq_eyebrow"]}</span>
      <h2>{h["faq_h2"]}</h2>
    </div>
    <div class="faq-list">
      {faq_items_html(FAQS[lang][:3])}
    </div>
    <p style="margin-top:24px;"><a href="faq.html" class="btn btn-ghost">{h["faq_cta"]}</a></p>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>{h["cta_h2"]}</h2>
      <p style="margin:0;">{h["cta_p"]}</p>
    </div>
    <a href="contact-us.html" class="btn btn-solid">{h["cta_btn"]}</a>
  </div>
</section>'''
    return title, h["lede"], hero, body


def build_about(lang):
    a = ABOUT[lang]
    title = "HIVE Global Advisory \u2014 " + ("About us" if lang == "en" else "Chi siamo")
    hero = f'''<section class="page-hero on-ink motif">
  {graticule_svg("bg")}
  <div class="wrap">
    <span class="eyebrow">{a["eyebrow"]}</span>
    <h1 style="max-width:20ch;">{a["h1"]}</h1>
    <p class="lede lede-sm">{a["lede"]}</p>
  </div>
</section>'''
    team_cards = "\n      ".join(
        f'''<div class="article">
        <span class="ref">{code}</span>
        <h3>[Nome Cognome]</h3>
        <p>{role}<br>[{"Registration details" if lang=="en" else "Dati di iscrizione all\u2019albo"}]</p>
      </div>''' for code, role in TEAM[lang])
    body = f'''<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{a["values_eyebrow"]}</span>
      <h2>{a["values_h2"]}</h2>
    </div>
  </div>
  <div class="facts">
    {facts_html(a["values"])}
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{a["team_eyebrow"]}</span>
      <h2>{a["team_h2"]}</h2>
      <p>{a["team_p"]}</p>
    </div>
    <div class="articles">
      {team_cards}
    </div>
  </div>
</section>

<section class="on-ink cta-band">
  <div class="wrap">
    <div>
      <h2>{a["cta_h2"]}</h2>
      <p style="margin:0;">{a["cta_p"]}</p>
    </div>
    <a href="contact-us.html" class="btn btn-solid">{a["cta_btn"]}</a>
  </div>
</section>'''
    return title, a["lede"], hero, body


def build_global(lang):
    g = GLOBAL[lang]
    title = "HIVE Global Advisory \u2014 " + g["eyebrow"]
    hero = f'''<section class="page-hero on-ink motif">
  {graticule_svg("bg")}
  <div class="wrap">
    <span class="eyebrow">{g["eyebrow"]}</span>
    <h1 style="max-width:24ch;">{g["h1"]}</h1>
    <p class="lede lede-sm">{g["lede"]}</p>
  </div>
</section>'''
    region_cards = "\n      ".join(
        f'<div class="region-card"><h3>{name}</h3><p>{desc}</p></div>' for name, desc in g["regions"])
    body = f'''<section class="on-ink">
  <div class="globe-wrap">{globe_svg(lang)}</div>
  {ticker_html(lang)}
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{g["offices_eyebrow"]}</span>
      <h2>{g["offices_h2"]}</h2>
    </div>
    {offices_grid_html(lang)}
  </div>
</section>

<section style="padding-top:0;">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{g["network_eyebrow"]}</span>
      <h2>{g["network_h2"]}</h2>
      <p>{g["network_p"]}</p>
    </div>
    <div class="regions">
      {region_cards}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>{g["cta_h2"]}</h2>
      <p style="margin:0;">{g["cta_p"]}</p>
    </div>
    <a href="contact-us.html" class="btn btn-solid">{g["cta_btn"]}</a>
  </div>
</section>'''
    return title, g["lede"], hero, body


def build_services(lang):
    title = "HIVE Global Advisory \u2014 " + ("Services" if lang == "en" else "Servizi")
    eyebrow = "Services" if lang == "en" else "Aree di competenza"
    h1 = ("Integrated support across the lifecycle of international business" if lang == "en"
          else "Un supporto integrato lungo tutto il ciclo di vita del business internazionale")
    lede = ("From incorporation to tax planning, from financial advisory to extraordinary transactions."
            if lang == "en" else
            "Dalla costituzione societaria alla pianificazione fiscale, dalla consulenza finanziaria alle operazioni straordinarie.")
    cta_label = "Request a consultation on this topic" if lang == "en" else "Richiedi una consulenza su questo tema"
    hero = f'''<section class="page-hero on-ink motif">
  {graticule_svg("bg")}
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1 style="max-width:22ch;">{h1}</h1>
    <p class="lede lede-sm">{lede}</p>
  </div>
</section>'''
    blocks = []
    for i, s in enumerate(SERVICES[lang]):
        ink = " on-ink" if i % 2 == 1 else ""
        last_border = ' style="border-bottom:none;"' if i == len(SERVICES[lang]) - 1 else ""
        items_html = "\n        ".join(f"<li>{it}</li>" for it in s["items"])
        blocks.append(f'''<section id="{s["id"]}" class="practice{ink}"{last_border}>
  <div class="wrap grid">
    <div>
      <span class="ref">{s["ref"]}</span>
      <h2>{s["title"]}</h2>
      <p>{s["intro"]}</p>
      <a href="contact-us.html" class="btn btn-ghost">{cta_label}</a>
    </div>
    <ul>
        {items_html}
    </ul>
  </div>
</section>''')
    cta_h2 = "Can&rsquo;t find the area you need?" if lang == "en" else "Non trovi l'area che cerchi?"
    cta_p = "Write to us: we will put you in touch with the right professional." if lang == "en" else "Scrivici: ti mettiamo in contatto con il professionista giusto."
    body = "\n\n".join(blocks) + f'''

<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>{cta_h2}</h2>
      <p style="margin:0;">{cta_p}</p>
    </div>
    <a href="contact-us.html" class="btn btn-solid">{CTA_LABEL[lang]}</a>
  </div>
</section>'''
    extra_style = '''<style>
.practice{ padding: 88px 0; border-bottom: 1px solid var(--parchment-line); }
.practice .grid{ display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: start; }
@media (max-width: 760px){ .practice .grid{ grid-template-columns: 1fr; gap: 30px; } }
.practice .ref{ font-family: var(--font-mono); color: var(--brass); font-size: .85rem; display: block; margin-bottom: 14px; }
.practice.on-ink{ border-bottom-color: var(--ink-line); }
.practice ul{ list-style: none; margin: 0; padding: 0; }
.practice li{ font-size: .95rem; padding: 12px 0; border-top: 1px solid var(--parchment-line); }
.practice.on-ink li{ border-top-color: var(--ink-line); color: rgba(243,238,223,.85); }
.practice li:first-child{ border-top: none; }
</style>'''
    return title, lede, hero, body, extra_style


def build_contact(lang):
    c = CONTACT[lang]
    title = "HIVE Global Advisory \u2014 " + c["eyebrow"]
    hero = f'''<section class="page-hero on-ink motif">
  {graticule_svg("bg")}
  <div class="wrap">
    <span class="eyebrow">{c["eyebrow"]}</span>
    <h1 style="max-width:20ch;">{c["h1"]}</h1>
    <p class="lede lede-sm">{c["lede"]}</p>
  </div>
</section>'''
    area_options = "\n          ".join(f'<option>{s["title"]}</option>' for s in SERVICES[lang])
    other = "Other" if lang == "en" else "Altro"
    body = f'''<section>
  <div class="wrap">
    <!--
      Static site: this form does not send data until connected to a
      service (Netlify Forms, Formspree, your own backend...).
      See the project README.
    -->
    <form class="contact" action="#" method="POST">
      <div>
        <label for="nome">{c["f_first"]}</label>
        <input type="text" id="nome" name="first_name" required>
      </div>
      <div>
        <label for="cognome">{c["f_last"]}</label>
        <input type="text" id="cognome" name="last_name" required>
      </div>
      <div>
        <label for="email">{c["f_email"]}</label>
        <input type="email" id="email" name="email" required>
      </div>
      <div>
        <label for="telefono">{c["f_phone"]}</label>
        <input type="tel" id="telefono" name="phone">
      </div>
      <div>
        <label for="paese">{c["f_country"]}</label>
        <input type="text" id="paese" name="country">
      </div>
      <div>
        <label for="area">{c["f_area"]}</label>
        <select id="area" name="area">
          <option value="">{c["f_area_ph"]}</option>
          {area_options}
          <option>{other}</option>
        </select>
      </div>
      <div class="full">
        <label for="messaggio">{c["f_message"]}</label>
        <textarea id="messaggio" name="message" required></textarea>
      </div>
      <div class="full checkline">
        <input type="checkbox" id="privacy" name="privacy" required>
        <label for="privacy" style="text-transform:none; font-family:var(--font-body); letter-spacing:normal; margin:0;">{c["f_privacy"]}<a href="privacy.html" style="color:var(--ink); text-decoration:underline;">{c["f_privacy_link"]}</a>{c["f_privacy_end"]}</label>
      </div>
      <div class="full">
        <button type="submit" class="btn btn-solid">{c["f_submit"]}</button>
        <p class="form-note">{c["f_note"]}</p>
      </div>
    </form>
  </div>
</section>

<section style="padding-top:0;">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{c["offices_eyebrow"]}</span>
      <h2>{c["offices_h2"]}</h2>
    </div>
    {offices_grid_html(lang)}
  </div>
</section>'''
    extra_style = '''<style>
.offices-4{ display:grid; grid-template-columns:repeat(auto-fit, minmax(210px,1fr)); gap:1px; background:var(--parchment-line); border:1px solid var(--parchment-line); margin-top:20px; }
.checkline{ display:flex; align-items:flex-start; gap:10px; font-size:.85rem; color:var(--slate); }
.checkline input{ width:auto; margin-top:3px; }
</style>'''
    return title, c["lede"], hero, body, extra_style


def build_faq(lang):
    title = "HIVE Global Advisory \u2014 FAQ"
    eyebrow = "FAQ"
    h1 = "Frequently asked questions" if lang == "en" else "Domande frequenti"
    lede = ("Can&rsquo;t find your answer? " if lang == "en" else "Non trovi la risposta che cerchi? ")
    hero = f'''<section class="page-hero on-ink motif">
  {graticule_svg("bg")}
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1 style="max-width:20ch;">{h1}</h1>
  </div>
</section>'''
    contact_word = "contact us" if lang == "en" else "contattaci"
    body = f'''<section>
  <div class="wrap">
    <div class="faq-list">
      {faq_items_html(FAQS[lang])}
    </div>
    <p style="margin-top:28px; color:var(--slate);">{lede}<a href="contact-us.html" style="color:var(--ink); text-decoration:underline;">{contact_word}</a>.</p>
  </div>
</section>'''
    return title, h1, hero, body


def build_privacy(lang):
    p = PRIVACY[lang]
    title = "HIVE Global Advisory \u2014 " + p["h1"]
    hero = f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">{p["eyebrow"]}</span>
    <h1>{p["h1"]}</h1>
  </div>
</section>'''
    sections_html = "\n    ".join(f"<h2>{t}</h2>\n    <p>{d}</p>" for t, d in p["sections"])
    body = f'''<section style="padding-top:0;">
  <div class="wrap legal-body">
    <div class="legal-notice">{p["notice"]}</div>
    {sections_html}
  </div>
</section>'''
    return title, p["h1"], hero, body

print("Page builders loaded OK")

# ---------------------------------------------------------------- main loop

BUILDERS = {
    "index": build_index, "about-us": build_about, "global-presence": build_global,
    "services": build_services, "contact-us": build_contact, "faq": build_faq, "privacy": build_privacy,
}

for lang in LIVE:
    outdir = os.path.join(ROOT, lang)
    os.makedirs(outdir, exist_ok=True)
    for page in PAGES:
        result = BUILDERS[page](lang)
        if len(result) == 5:
            title, desc, hero, body, extra_style = result
        else:
            title, desc, hero, body = result
            extra_style = ""
        html = page_shell(lang, page, title, desc, hero, body)
        if extra_style:
            html = html.replace(
                '<link rel="stylesheet" href="../css/style.css">',
                '<link rel="stylesheet" href="../css/style.css">\n' + extra_style)
        with open(os.path.join(outdir, f"{page}.html"), "w", encoding="utf-8") as fh:
            fh.write(html)
    print(f"Generated /{lang}/: {len(PAGES)} pages")

# ---------------------------------------------------------------- pending-language stubs

PENDING_NOTE = {
    "de": "Dieser Sprachordner ist vorbereitet, der Inhalt wurde aber noch nicht \u00fcbersetzt.",
    "fr": "Ce dossier de langue est pr\u00eat, mais le contenu n'a pas encore \u00e9t\u00e9 traduit.",
    "es": "Esta carpeta de idioma est\u00e1 preparada, pero el contenido a\u00fan no se ha traducido.",
    "ar": "\u0645\u062c\u0644\u062f \u0627\u0644\u0644\u063a\u0629 \u0647\u0630\u0627 \u062c\u0627\u0647\u0632\u060c \u0644\u0643\u0646 \u0627\u0644\u0645\u062d\u062a\u0648\u0649 \u0644\u0645 \u064a\u062a\u0631\u062c\u0645 \u0628\u0639\u062f.",
    "ru": "\u042d\u0442\u0430 \u044f\u0437\u044b\u043a\u043e\u0432\u0430\u044f \u043f\u0430\u043f\u043a\u0430 \u0433\u043e\u0442\u043e\u0432\u0430, \u043d\u043e \u043a\u043e\u043d\u0442\u0435\u043d\u0442 \u0435\u0449\u0451 \u043d\u0435 \u043f\u0435\u0440\u0435\u0432\u0435\u0434\u0451\u043d.",
}
for code in LANGS:
    if code not in LIVE:
        outdir = os.path.join(ROOT, code)
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "README.md"), "w", encoding="utf-8") as fh:
            fh.write(f"# {LANGS[code]['native']}\n\n{PENDING_NOTE[code]}\n")

# ---------------------------------------------------------------- root language gateway

lang_cards = []
for code, meta in LANGS.items():
    if code in LIVE:
        lang_cards.append(f'<a class="gate-card" href="{code}/index.html" hreflang="{code}">{meta["native"]}</a>')
    else:
        lang_cards.append(f'<span class="gate-card soon">{meta["native"]} <em>{SOON_TAG["en"]}</em></span>')

root_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HIVE Global Advisory</title>
<meta name="description" content="International legal, tax and financial advisory. Choose your language.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<style>
  body{{ background:var(--ink); color:var(--parchment); min-height:100vh; display:flex; align-items:center; justify-content:center; }}
  .gate{{ text-align:center; padding:40px 24px; }}
  .gate img{{ width:84px; height:84px; margin-bottom:22px; }}
  .gate h1{{ color:var(--white); font-size:1.6rem; margin-bottom:8px; }}
  .gate p{{ color:rgba(243,238,223,.65); margin-bottom:34px; font-family:var(--font-mono); font-size:.78rem; letter-spacing:.08em; text-transform:uppercase; }}
  .gate-grid{{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; max-width:460px; }}
  .gate-card{{ font-family:var(--font-body); font-size:.95rem; text-decoration:none; color:var(--parchment); border:1px solid var(--brass); padding:12px 20px; min-width:130px; transition:background .15s ease; }}
  a.gate-card:hover{{ background:var(--ink-line); }}
  .gate-card.soon{{ border-color:var(--ink-line); color:rgba(243,238,223,.4); }}
  .gate-card.soon em{{ display:block; font-style:normal; font-family:var(--font-mono); font-size:.62rem; letter-spacing:.06em; text-transform:uppercase; margin-top:3px; }}
</style>
</head>
<body>
  <div class="gate">
    <img src="assets/logo-mark.svg" alt="HIVE Global Advisory">
    <h1>HIVE Global Advisory</h1>
    <p>Choose your language &middot; Scegli la lingua</p>
    <div class="gate-grid">
      {chr(10).join(lang_cards)}
    </div>
  </div>
  <script>
    (function(){{
      var supported = {LIVE!r};
      var pref = (navigator.language || "en").slice(0,2).toLowerCase();
      if (supported.indexOf(pref) !== -1) {{
        window.location.replace(pref + "/index.html");
      }}
    }})();
  </script>
</body>
</html>
'''
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
    fh.write(root_html)
print("Root language gateway written")
print("ALL DONE")

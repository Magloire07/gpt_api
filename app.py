from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import asyncio

def cliquer_login(page):
    # Tentative par data-testid
    try:
        print("Essai avec [data-testid='login-button']...")
        page.click("[data-testid='login-button']", timeout=3000)
        return True
    except:
        print("Échec avec data-testid.")

    # Tentative par texte exact en anglais
    try:
        print("Essai avec text='Log in'...")
        page.click("text='Log in'", timeout=3000)
        return True
    except:
        print("Échec avec texte 'Log in'.")

    # Tentative par texte en français
    try:
        print("Essai avec text='Se connecter'...")
        page.click("text='Se connecter'", timeout=3000)
        return True
    except:
        print("Échec avec texte 'Se connecter'.")

    print("Aucune méthode n'a fonctionné.")
    return False

def extraire_reponse_et_sauvegarder(page):
    # Sélecteur de tous les blocs markdown assistant
    selector = 'article[data-turn="assistant"] div.markdown'

    # Attendre que le contenu soit chargé
    page.wait_for_selector(selector, timeout=10000)

    # Utiliser JavaScript pour obtenir le texte du dernier bloc markdown assistant
    texte_complet = page.evaluate("""() => {
        const markdowns = document.querySelectorAll('article[data-turn="assistant"] div.markdown');
        if (markdowns.length === 0) return '';
        return markdowns[markdowns.length - 1].innerText;
    }""")

    print("Réponse extraite :\n")
    print(texte_complet)

    # Sauvegarder dans un fichier
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(texte_complet)

    print("\nRéponse enregistrée dans response.txt")



def ecrire_requete(page):
    # 🧠 Clique dans la zone pour la focus
    page.click('#prompt-textarea')
    texte=""
    while not texte:
        with open("request.txt", "r", encoding="utf-8") as f:
            texte = f.read()
    #vide le fichier pour la prochaine requête
    with open("request.txt", "w", encoding="utf-8") as f:
        f.write("")
    # ✍️ Tape le texte de la requête
    page.keyboard.type(texte)


with Stealth().use_sync(sync_playwright()) as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://chatgpt.com")

    while True:
        # ✍️ écrire la requête"
        ecrire_requete(page)
        # (facultatif) Soumettre avec Entrée
        page.keyboard.press("Enter")
        # Attendre un peu pour que la réponse arrive
        page.wait_for_timeout(5000)

        extraire_reponse_et_sauvegarder(page)


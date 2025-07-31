import time

def ask(request):
    """
    Envoie une requête à l'API et retourne la réponse.
    """
    with open("request.txt", "w", encoding="utf-8") as f:
        f.write(request)
            # ...code pour envoyer la requête...
    response = ""
    while not response:
        with open("response.txt", "r", encoding="utf-8") as f:
            response = f.read()
        time.sleep(5)  # Attendre 1 seconde avant de vérifier à nouveau pour liberer le verrouillage du fichier
    # vide le fichier pour la prochaine requête
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write("")
    return response
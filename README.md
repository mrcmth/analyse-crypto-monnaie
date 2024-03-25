# Day-Trading : Trade de crypto monnaie automatisé avec l'API de Coinbase

Ce code est un "robot" trader, avec une analyse précise des cours des cryptos monnaies, ce robot achète et revend en temps réel. 

Je vous montre comment se comporte le robot pas à pas.

## Installation

Ce robot utilise la plateforme d'échange Coinbase, donc j'utilise l'API que cette entreprise met à disposition des développeurs.
Pour ma part, j'utilise la version Python de l'API.

1. Installation de module python de Coinbase 

    ```
    pip3 install coinbase-advanced-py
    ```

2. Au début du code, importons les bibliothèques suivantes :

    ```
    import os
    from json import dumps
    from datetime import datetime, timedelta
    import random
    import time
    import logging
    ```

    os car je manipule des fichier txt pour stocker des données de prix sur certains laps de temps //
    json car l'api renvoie les données sur les cours, les crypto monnaies sous ce format //
    datetime pour l'évaluation de la fiabilité des données par rapport à l'heure actuelle //
    random pour générer les ordres clients //
    logging pour stocker les erreurs quand le code s'éxécute //

## Les fonctions importantes

Ce code comporte 10 fonctions :

9 de ces fonctions servent au bon fonctionnement de la fonction principale qui décide l'achat ou bien la vente de certaines cryptos, cette fonction s'appelle :
```
rateALERTE(c_fichier, c_name, price, client)
```

On retrouve donc donc parmi les 9 fonctions satéllites, une fonction pour l'achat, une pour la revente, ou bien une qui crée un ordre client aléatoire.

## Prséentation de la boucle infinie qui fait une veille 24h/24 - 7j/7

Examinons le contenu de cette boucle : 

```python
cryptos = crypto_trade("liste_crypto.txt")

while True:
    for c in cryptos:
        print(c)
        price = get_price(c)
        
        if price is not None:
            print(f"Prix de {c} est de {price} USDC")
            if not os.path.exists(f"crypto_hist/{c}.txt"):
                    with open(f"crypto_hist/{c}.txt", "w") as f:
                        pass 
            remove_l(f"crypto_hist/{c}.txt")
            with open(f"crypto_hist/{c}.txt", "a") as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{price}\n")

            rateALERTE(f"crypto_hist/{c}", c, price, client, cryptos)
            

    time.sleep(60)
```

Tout d'abord, on récupère une liste de crypto dans un fichier txt, j'ai listé 44 cryptos pour le trade.
```txt
["SHIB-USDC", "QI-USDC", "RPL-USDC", "MEDIA-USDC", "00-USDC", "CTX-USDC", "DNT-USDC", "VET-USDC", "BONK-USDC", "LSETH-USDC", "SEI-USDC", "AXS-USDC", "CRO-USDC", "APT-USDC", "NEAR-USDC", "IMX-USDC", "INJ-USDC","CBETH-USDC", "LDO-USDC", "TIA-USDC", "HBAR-USDC", "DOGE-USDC", "GST-USDC", "LTC-USDC", "XYO-USDC", "EGLD-USDC","ENJ-USDC", "AXL-USDC", "RENDER-USDC", "AVAX-USDC", "ATOM-USDC", "UNI-USDC", "ICP-USDC", "SOL-USDC", "ARB-USDC", "XRP-USDC","SYN-USDC", "STRK-USDC", "DAI-USDC", "ETC-USDC", "BCH-USDC", "MATIC-USDC"]
```
Ensuite la boucle WHILE, vient examiner chaque crypto, appel de la fonction get_price qui se sert de l'API coinbase pour avoir le prix courant de la crypto {c}.

Après vérification de l'obtention du prix, on note ce prix dans un fichier txt, dont le nom est celui de la crypto_PRIX.txt

Et nous appelons rateALERTE pour examiner ce prix.

Sans oublier le time sleep 60 qui vient répéter cette boucle toutes les minutes, ainsi ce code vient à envoyer environ **65 000 requêtes** à l'API par jours (prix, achat, revente, obtention d'id de la crypto, obtention de solde) !

## Étude de rateALERTE

Analysons certaines parties importantes de rateALERTE : (le code est visible en entier ci-joint)

1. Tout d'abord on analyse l'historique des prix sur une heure, par exemple : si il est 8h19, alors on analyse les prix de 7h19 à 8h19

```python
with open(c_fichier + ".txt", 'r') as f:

            for ligne in f:
                date_str, prix_str = ligne.split(',')
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                prix_float = float(prix_str)
            
                if heure_avant <= date <= heure_actuelle:
                    prix.append(prix_float)
```

Donc ouverture du fichier txt de la boucle, récupération du prix qui a été noté, si le prix < 1h, alors on le met dans la liste prix. Liste qui va servir à calculer les taux.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

# Day-Trading : Trade de crypto monnaie automatisé avec l'API REST de Coinbase

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
```texte
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

2. 2 études de marché possibles :
2.1 Première étude : alerte lors de la montée d'un prix :

Calcul du taux de croissance sur une heure et récupération de la tendance journalière : ces 2 composantes me servent à déterminer si il doit y avoir achat ou non : 

   ```python
                taux_al = ((price-prix[0])/prix[0])*100
                print("tendance 1h : ", taux_al)

                trend_day = float(client.get_product(c_name)['price_percentage_change_24h'])
                print("Tendance journaliere:", trend_day)
```
Ouverture du fichier c_alert (fichier qui fait pair avec celui des prix noté, mais la différence c'est que le nombre de lignes de ce nouveau fichier va servir de base pour l'achat. Explication un peu plus bas.
 ```python
              with open(c_alerte, 'r+') as f:
                    lines = f.readlines()
                    nombre_de_lignes = len(lines)
                    print("nombre lignes", nombre_de_lignes)
```

CAS 1 : le fichier est vide, 0 ligne ET on détecte une montée subite de plus de 4% (grâce taux_al) : 

 ```python
    if nombre_de_lignes == 0 and taux_al >= 4 :
                        if not os.path.exists(c_alerte):
                            with open(c_alerte, "w") as f:
                                pass 
                        remove_l(c_alerte)
                        print("if1")

                        cT = client.get_account("95680afb-3135-5376-88d6-b43319402bd7")
                        money = cT['account']['available_balance']['value']

                        with open("c_d.txt", 'r+') as fichier:
                                    ct = fichier.read()
                                    quote_disp = float(ct.strip())

                        if quote_disp > 0:

                            ligne_achat = f"{price},{price*1.026}\n"
                            f.write('\n')
                            f.write(str(ligne_achat))
                                    
                            quote_size = float(money)/quote_disp
                            aB = normalize(quote_size, "quote-size", client, c_name)   #arrondi le montant des cryptos dispo
                            print("ab : " + aB)
                            achatREAL(c_name, aB, client)
                            with open("c_d.txt", 'r+') as fichier:
                                    ct = fichier.read()
                                    quote_disp = float(ct.strip())
                                    new_quote = quote_disp - 1
                                    fichier.seek(0)
                                    fichier.write(str(new_quote))

                            print("l acaht s'est terminé et réussi")
```
C'est donc un moment opportunt pour acheter ! En dessous du premier if, on récupère l'argent disponibe "money" avec un appel à l'API, on récupère dans c_d.txt le nombre d'investissement encore possibles à réaliser. Je m'explique, ce fichier comporte un float, au démarrage du code j'ai mis 8, pour qu'il y ait seulement 8 investissements simultanés. Ainsi comme on va le voir, un acaht est possible que si quote_disp >0 et quant l'achat est terminé on fait -1 au float de c_d.txt. Cela me permet globalement que les investissements soit le l'ordre de 1/8eme de mon capital.

Donc comme quote_disp > 0 :
on calcule le quote_size, montant à investir (1/8eme), et on réalise l'achat avace achatREAL :

```python
def achatREAL(product_id, quote_size, client):

    client_order_id = order_client()

    response = client.market_order_buy(
        client_order_id=client_order_id,
        product_id=product_id,
        quote_size=quote_size
    )

    print(product_id)
    print(quote_size)
    
    print(response)

```
Simple appel à l'API pour un achat.

CAS 2: un investissement plus soft, car le marché sur 24h est haussier, le taux sur une heure dépasse +2.5% :

1er elif, toujours le même système pour l'achat et la gestion du nombre d'investissements :

```python
elif nombre_de_lignes == 0 and taux_al >= 2.5 and trend_day >= 2.5 :
                        if not os.path.exists(c_alerte):
                            with open(c_alerte, "w") as f:
                                pass 
                        remove_l(c_alerte)
                        print("if1")

                        cT = client.get_account("95680afb-3135-5376-88d6-b43319402bd7")
                        money = cT['account']['available_balance']['value']

                        with open("c_d.txt", 'r+') as fichier:
                                    ct = fichier.read()
                                    quote_disp = float(ct.strip())

                        if quote_disp > 0:

                            ligne_achat = f"{price},{price*1.0165}\n"
                            f.write('\n')
                            f.write(str(ligne_achat))
                                    
                            quote_size = float(money)/quote_disp
                            aB = normalize(quote_size, "quote-size", client, c_name)   #arrondi le montant des cryptos dispo
                            print("ab : " + aB)
                            achatREAL(c_name, aB, client)
                            with open("c_d.txt", 'r+') as fichier:
                                    ct = fichier.read()
                                    quote_disp = float(ct.strip())
                                    new_quote = quote_disp - 1
                                    fichier.seek(0)
                                    fichier.write(str(new_quote))

                            print("l acaht s'est terminé et réussi")

```

CAS 3: Pour la réalisation de ce cas, obligatoirment un des 2 précédents cas a été réalisé, ici on va surveiller quand le prix dépassera prix*1.065 pour le cas 2, ou bien prix*1.026 pour le cas 1 (marge plus grande pour la cas 1, car la montée est brusque donc plus de chance de faire 2,6 % de plus value)

Et dès que le prix est atteint, on revend, on fais +1 au fichier c_d.txt et on supprime donc nos fichier c_alerte et le fichier de prix. Et notre plus value est réalisée:
```python
elif nombre_de_lignes >= 1:
                        
                        d = lines[-1].strip()
                        print(d)
                        lim_price = float(d.split(',')[-1])
                        print(str(lim_price) + " et " + str(price))

                        prixdachat = float(d.split(',')[-2])


                        print("============")
                        print("| CRYPTO  : ", c_name, "       |")
                        print("|  PRIX ACHAT : ", prixdachat, "   |")
                        print("|  PRIX VENTE PREVUE : ", lim_price, "   |")
                        print("|  PRIX ACTUEL : ", price, "   |")
                        print("==========")


                        if lim_price < price:
                            por = client.get_account(uuid_crypto(c_name))
                            vB = normalize(por['account']['available_balance']['value'], "base_size", client, c_name)   #arrondi le montant des cryptos dispo
                            print("vb : " + vB)
                            venteREAL(c_name, vB, client)
                            os.remove("/home/marcm/cb/"+c_alerte)
                            os.remove("/home/marcm/cb/"+c_fichier+".txt")
                            with open("c_d.txt", 'r+') as fichier:
                                ct = fichier.read()
                                quote_disp = float(ct.strip())
                                new_quote = quote_disp + 1
                                fichier.seek(0)
                                fichier.write(str(new_quote))
```

lim_price est le prix récupéré dans le fichier txt c_alerte. Ce prix a était noté dans le fichier soit dans le cas 1 ou 2.

Accessoirement, j'utilise des fonctions comme normalize() qui réalise un appel à l'API pour déterminer la précision de vente. Actuellement l'API ne permet pas de vendre tout ce qu'on a : 
EXEMPLE : je veux vendre 1.1564868 bitcoin, pas possible car la précision pour la vente se limite à 4 décimales, dans ce cas normalize limite la vente à 4 décimales : donc je vend : 1.1564 btc

normalize :  quote_size pour précision pour l'achat, base_size précision pour la vente
```python
def normalize(number, t, client, c_name):

    if t == "base_size":
        b = client.get_product(c_name)['base_increment']
        print(b)
    else:
        b = client.get_product(c_name)['quote_increment']
        
    nbr_dec = len(b.split('.')[1]) if '.' in b else 0
    
    number_str = str(number)
    
    decimal_index = number_str.find('.')
    
    if decimal_index == -1:
        return str(number)
    
    result = number_str[:decimal_index + nbr_dec + 1]
    
    print(t + " " + str(result))
    return str(result)
```
## Gestion d'erreur, et débogage

Mon code utilise try / expect en effet, il peut arriver que le code rencontre des problèmes avec l'api, il est important qu'il ne s'arrête pas, donc les erreur sont notées dans un fichier error.log, j'utilise traceback pour connaitre le numéro de ligne de l'erreur. Mais désormais, les seules erreures que je rencontre sont indépendantes de ma volonté, cela provient de coinbase qui doit avoir des problèmes au niveau des serveurs.
```
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
```

## Appel à l'API REST Coinbase :

J'utilise donc une clé d'API que je stocke dans un json, l'appel des fonction de l'api passe systématiquement par client."   " 
```
client = RESTClient(key_file="cb_id.json")
```


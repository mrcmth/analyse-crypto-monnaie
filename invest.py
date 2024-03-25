from coinbase.rest import RESTClient
import os
import json
from datetime import datetime, timedelta
import random
import time
import logging
import requests
import ast

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def crypto_trade(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
            contenu = ast.literal_eval(fichier.read())
    return contenu

def get_price(crypto, retries=3):
    for attempt in range(retries):
        try:
            price = float(client.get_product(crypto)["price"])
            return price
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error (attempt {attempt+1}/{retries}) while getting price for {crypto}: {e}")
            time.sleep(2) 

    print(f"Failed to get price for {crypto} after {retries} attempts")
    return None

def selection_crypto(client):
    crypto_list = [
        "SHIB-USDC", "QI-USDC", "RPL-USDC", "MEDIA-USDC", "00-USDC", "CTX-USDC", "DNT-USDC", "VET-USDC", "BONK-USDC", "LSETH-USDC", "SEI-USDC", "AXS-USDC", "CRO-USDC", "APT-USDC", "NEAR-USDC", "IMX-USDC", "INJ-USDC",
        "CBETH-USDC", "LDO-USDC", "TIA-USDC", "HBAR-USDC", "DOGE-USDC", "GST-USDC", "LTC-USDC", "XYO-USDC", "EGLD-USDC",
        "ENJ-USDC", "AXL-USDC", "RENDER-USDC", "AVAX-USDC", "ATOM-USDC", "UNI-USDC", "ICP-USDC", "SOL-USDC", "ARB-USDC", "XRP-USDC",
        "SYN-USDC", "STRK-USDC", "DAI-USDC", "ETC-USDC", "BCH-USDC", "MATIC-USDC"
    ]

    c_eligible = []

    for el in crypto_list:
        z = float(client.get_product(el)['price_percentage_change_24h'])
        if 1 <= z <= 10 :
            c_eligible.append(el)

    if not c_eligible:
        print("Aucune crypto éligible trouvée pour le trade.")
        return None

    #crypto_choice = min(c_eligible)
    #print("Crypto choisie pour le trade : ", crypto_choice)
    return c_eligible

def order_client():
    return str(random.randint(10000000, 99999999))

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

def uuid_crypto(c_name):
    
    if "-USDC" in c_name:
        name = c_name.replace("-USDC", "")
    else:
        name = c_name


    data= client.get_accounts()
    uuid_crypto = None
    for account in data['accounts']:
        if account['name'] == f'Portefeuille en {name}':
            uuid_crypto = account['uuid']
            
            break
        
    return uuid_crypto

def remove_l(fichier):
    heure_actuelle = datetime.now()
    difference_max = timedelta(hours=4)
    
    lignes_restantes = []
    
    with open(fichier, 'r') as f:
        for ligne in f:
            date_str = ligne.split(',')[0]
            date_ligne = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            
            if heure_actuelle - date_ligne <= difference_max:
                lignes_restantes.append(ligne)
    
    with open(fichier, 'w') as f:
        for ligne in lignes_restantes:
            f.write(ligne)
               
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

def venteREAL(product_id, base_size, client):

    client_order_id = order_client()

    response = client.market_order_sell(
        client_order_id=client_order_id,
        product_id=product_id,
        base_size=base_size
    )
    
    print(response)

def rateALERTE(c_fichier, c_name, price, client, cryptos):
    try:
        prix = []
        heure_actuelle = datetime.now()
        heure_avant = heure_actuelle - timedelta(hours=1)

        with open(c_fichier + ".txt", 'r') as f:

            for ligne in f:
                date_str, prix_str = ligne.split(',')
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                prix_float = float(prix_str)
            
                if heure_avant <= date <= heure_actuelle:
                    prix.append(prix_float)

            if prix:

                c_alerte = c_fichier + "_PRIX.txt"

                if not os.path.exists(c_alerte):
                    with open(c_alerte, "w") as f:
                        pass 

            #==============TEST 1  D ETUDE DE TAUX ================

                taux_al = ((price-prix[0])/prix[0])*100
                print("tendance 1h : ", taux_al)

                trend_day = float(client.get_product(c_name)['price_percentage_change_24h'])
                print("Tendance journaliere:", trend_day)


                with open(c_alerte, 'r+') as f:
                    lines = f.readlines()
                    nombre_de_lignes = len(lines)
                    print("nombre lignes", nombre_de_lignes)
                    

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

                            #cryptos.remove(c_name)
                            #c_select = selection_crypto(client)

                            #if c_select is not None :
                                
                                #cryptos.append(c_select)

                                #with open("liste_crypto.txt", 'w') as fichier:
                                    #fichier.write(str(cryptos))
                            
                return taux_al
            else:
                return "Erreur pour la fonction rateALERTE prix < 1h."

    except Exception as e:
        logging.exception("Une erreur est survenue dans la fonction rateALERTE: %s", e)
     
client = RESTClient(key_file="cb_id.json")

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


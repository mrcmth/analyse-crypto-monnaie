# Trade de crypto monnaie automatisé

Ce code est un "robot" trader, avec une analyse précise des cours des cryptos monnaies, ce robot achète et revend en temps réel. 

En un seul code (analyse.py) je vous montre comment se comporte le robot pas à pas.

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

Ce code comporte 8 fonctions :

La fonction la plus importante, celle qui note les prix dans un fichier spécial quand un cours chute : 
```
rateALERTE(c_fichier, c_name, price, client)
```

## Exemple de code

Voici un exemple de code JavaScript qui affiche "Hello, world!" dans la console :

```javascript
console.log("Hello, world!");
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

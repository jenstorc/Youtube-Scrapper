# Youtube-Scrapper

But : Créer un script exécutable permettant de scraper une liste de vidéos youtube et stockant les données récupérées dans un fichier au format json

## Quelles informations obtenir ?
- Titre de la vidéo
- Nom du vidéaste
- Nombre de pouces bleu
- Description de la vidéo (format plain text)
- Liens exceptionnels de la description (s’il y en a, par exemple, des liens vers
- un timestamp vidéo ou un compte Twitter)
- id de la vidéo youtube
- Les n premiers commentaires (s’ils existent)

## Paramètres 
Entrée : Fichier JSON au format suivant (input.json)
Sortie : Fichier JSON dans un format que vous déterminerez (output.json)

## Utilisation en CLI
Le script sera lançable selon les commandes suivantes (strictement) sur une
machine Linux (Pas de window, mais ça vous le savez déjà) :
- python3.8 -m venv .venv
- source .venv/bin/activate
- pip install --upgrade pip
- python scrapper.py --input input.json --output output.json

## Technos
- Utilisation de Python 3.8+
- Utilisation de la lib de scraping - BeautifulSoup ou bien requests si vous
préférez le natif
- Utilisation des fonctions map/filter/reduce dès que possible (programmation fonctionnelle, vue au cours précédent)
- Bonne pratique de développement
    - Découpage de vos fonctions les plus grandes (visez la trentaine de ligne maximum)
    - Une fonction = une action
    - Un peu d’objet si nécessaire ?
- Tests unitaires de vos fonctions avec pytest =)
    - Ne pas hésiter à en écrire autant que vous avez de fonctions
    - NB: Plus vos fonctions sont atomiques, plus elles sont simples à tester =)

## Modalités d'évaluation
Le TP sera mis en public sur Github: Merci de ne PAS m’inviter sur votre repository mais bien de le laisser public
Le rendu sera fait par mail: Il devra mentionner l’url vers votre repo Githu

## Points d'attention

Le scraping est une des pratiques les plus fréquentes quand il s’agit de récupérer
de la donnée. Cependant certains sites rendent le scrapping plus difficile que
d’autres, c’est le cas de Youtube, vous allez devoir faire attention à ce que vous
arrivez à obtenir via BeautifulSoup (ou requests), il se peut que l’information que
vous cherchez ne soit pas forcément à l’endroit où vous l’attendez.
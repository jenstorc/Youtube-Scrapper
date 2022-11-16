import json # library to manage json file
import re # to get the number of likes
import requests
from bs4 import BeautifulSoup
import sys
import getopt

class VideoYoutube:
    id : str

    def __init__(self, id) -> None :
        self.id = id
        self.init_dict_res()

    # Initialisation du dictionnaire
    def init_dict_res(self) -> None :
        url : str = 'https://www.youtube.com/watch?v=' + str(self.id) #url ytb
        reponse : requests.models.Response = requests.get(url)
        soup : BeautifulSoup = BeautifulSoup(reponse.text, "html.parser")
        self.result : dict = {}
        data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
        data_json = json.loads(data)  

        self.set_title(soup)
        self.set_author(soup)
        self.set_nbLikes(data_json)
        description = self.set_description(data_json)
        self.set_links(description)

    # Ajout du titre dans le dictionnaire
    def set_title(self, soup) -> None :
        self.result["title"] : str = soup.find("meta", itemprop="name")['content']

    # Ajout du vidéaste dans le dictionnaire
    def set_author(self, soup) -> None :
        self.result["channel_name"] = soup.find("span", itemprop="author").next.next['content']  
    
    # Ajout du nombre de likes dans le dictionnaire
    def set_nbLikes(self, data_json) -> None :
        # number of likes 
        videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
        likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] # "No likes" or "###,### likes"  
        likes_str = likes_label.split(' ')[0].replace(',','')  
        
        if likes_str == 'No':
            #result["likes"] = '0' 
            self.result["nb_likes"] = 0
        else: 
            likes_str = likes_str.encode("ascii", "replace")
            likes_str = likes_str.decode(encoding="utf-8", errors="ignore")
            likes_str = likes_str.replace('?','')

            nb_like = ''
            i = 0
            car = likes_str[i]
            while i < len(likes_str) and car.isdigit():
                nb_like = str(nb_like) + str(car)
                i += 1
                car = likes_str[i]

            self.result["nb_likes"] = int(nb_like)

    # Ajout de la description dans le dictionnaire
    def set_description(self, data_json) -> str :
        dict_tmp = data_json['contents']["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["description"]["runs"]
        description = ''
        for i in range(len(dict_tmp)):
            if 'text' in dict_tmp[i].keys():
                description += dict_tmp[i]['text']
        
        self.result["description"] = description
        return description

    # Ajout des liens présents dans le dictionnaire
    def set_links(self, description) -> None :
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, description)      
        list_urls = [x[0] for x in url]

        #list_urls = get_urls(description) 
        if len(list_urls) != 0:
            self.result["links"] = list_urls

if __name__ == "__main__":
    try:
        # Récupérer les arguments de la ligne de commande
        options, args = getopt.getopt(sys.argv[1:], "", ['input=','output='])
        for opt, arg in options:
            # Vérifier qu'il existe bien --input et --output
            if opt in ['--input', '--output']:
                if opt in ('--input'):
                    # Vérifier qu'il s'agit bien de fichier json
                    if arg.endswith('.json'):
                        input = arg
                    else :
                        raise Exception("Le fichier d'input doit être de format .json")                    
                elif opt in ('--output'):
                    # Vérifier qu'il s'agit bien de fichier json
                    if arg.endswith('.json'):
                        output = arg
                    else :
                        raise Exception("Le fichier d'output doit être de format .json") 
            else :
                raise Exception("Vous devez saisir un fichier d'input et un fichier d'output comme ceci :\npython scrapper.py --input input.json --output output.json")

        input_file = open(input) # Ouverture du fichier json        
        data = json.load(input_file) # Considérer l'objet json comme un dictionnaire
        
        # Pour chaque élément du dictionnaire json (ie, pour chaque id de vidéo)
        final_result = {}
        for id_video in data['videos_id']:
            video_ytb = VideoYoutube(id_video) # Création de l'objet vidéo youtube
            final_result[id_video] = video_ytb.result # ajout du tableau résultat dans un dictionnaire regroupant toutes les informations de chaque vidéo

        input_file.close() # Fermeture du fichier json d'input

        # Ecriture des informations dans le fichier d'output
        with open(output, "w", encoding='utf8') as output_file:
            json.dump(final_result, output_file, ensure_ascii=False)

        output_file.close() # Fermeture du fichier json d'output
    except Exception as e:
        print(e)
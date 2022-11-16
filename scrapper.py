import json # library to manage json file
import re # to get the number of likes
import requests
from bs4 import BeautifulSoup
import sys
import getopt

class VideoYoutube:
    id : str
    #titre : str
    #nom_videaste : str
    #nb_pouce_bleu : int
    #description_video : str
    #list_n_premiers_com : list #list str
    #list_liens_exceptionnels : list # list str

    def __init__(self, id):
        self.id = id
        url : str = 'https://www.youtube.com/watch?v=' + str(id) #url ytb
        reponse : requests.models.Response = requests.get(url)
        self.soup : BeautifulSoup = BeautifulSoup(reponse.text, "html.parser")
        self.result : dict = {}
        data = re.search(r"var ytInitialData = ({.*?});", self.soup.prettify()).group(1)  
        self.data_json = json.loads(data)  
        self.dict_res()

    def dict_res(self):
        self.set_title()
        self.set_author()
        self.set_nbLikes()
        description = self.set_description()
        self.set_links(description)

    def set_title(self):
        self.result["title"] : str = self.soup.find("meta", itemprop="name")['content']
        #self.title = self.soup.find("meta", itemprop="name")['content']

    def set_author(self):
        self.result["channel_name"] = self.soup.find("span", itemprop="author").next.next['content']  
    
    def set_nbLikes(self):
        # number of likes 
        videoPrimaryInfoRenderer = self.data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
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

    def set_description(self):
        dict_tmp = self.data_json['contents']["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["description"]["runs"]
        description = ''
        for i in range(len(dict_tmp)):
            if 'text' in dict_tmp[i].keys():
                description += dict_tmp[i]['text']
        
        self.result["description"] = description
        return description

    def set_links(self, description):
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
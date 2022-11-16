import json # library to manage json file
import re # to get the number of likes
import requests
from bs4 import BeautifulSoup
import sys
import getopt
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        self.msg_erreur = None
        data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
        data_json = json.loads(data)  
        self.title = self.set_title(soup)
        self.videomaker = self.set_author(soup)
        self.nb_like = self.set_nbLikes(data_json)
        self.description = self.set_description(data_json)
        self.list_links = self.set_links() if self.description is not None else None
        

    # Ajout du titre dans le dictionnaire
    def set_title(self, soup) -> str :
        title = soup.find("meta", itemprop="name")
        if title is not None:
            self.result["title"] : str = title['content']
            return self.result["title"] 
        else : return None

    # Ajout du vidéaste dans le dictionnaire
    def set_author(self, soup) -> str :
        author = soup.find("span", itemprop="author")
        if author is not None :
            self.result["channel_name"] = soup.find("span", itemprop="author").next.next['content']  
            return self.result["channel_name"] 
        else : return None
    
    # Ajout du nombre de likes dans le dictionnaire
    def set_nbLikes(self, data_json) -> int :
        # Cas où la vidéo existe
        if 'videoPrimaryInfoRenderer' in data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0].keys():
            videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
            # Cas où les like sont possibles
            if 'accessibility' in videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText'].keys():
                likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] # "No likes" or "###,### likes"  
                likes_str = likes_label.split(' ')[0].replace(',','')  
                if likes_str == 'No': self.result["nb_likes"] = 0
                else: 
                    likes_str = likes_str.encode("ascii", "replace").decode(encoding="utf-8", errors="ignore").replace('?','')

                    nb_like = ''
                    i = 0
                    car = likes_str[i]
                    while i < len(likes_str) and car.isdigit():
                        nb_like = str(nb_like) + str(car)
                        i += 1
                        car = likes_str[i]

                    self.result["nb_likes"] = int(nb_like)
                return self.result["nb_likes"]
            # Cas où les likes sont bloqués (pas de like affiché)
            return None
        # Cas où la vidéo n'existe pas
        else : 
            self.msg_erreur = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['itemSectionRenderer']['contents'][0]['backgroundPromoRenderer']['title']['runs'][0]['text']
            return None

    # Ajout de la description dans le dictionnaire
    def set_description(self, data_json) -> str :
        
        if len(data_json['contents']["twoColumnWatchNextResults"]["results"]["results"]["contents"]) > 1:
            dict_tmp = data_json['contents']["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["description"]["runs"]
            description = ''
            for i in range(len(dict_tmp)):
                if 'text' in dict_tmp[i].keys():
                    description += dict_tmp[i]['text']
            self.result["description"] = description
            return description
        else : return None

    # Ajout des liens présents dans le dictionnaire
    def set_links(self) -> None :
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, self.description)      
        list_urls = [x[0] for x in url]

        #list_urls = get_urls(description) 
        if len(list_urls) != 0:
            self.result["links"] = list_urls
            return(self.result["links"])
        else :
            return None

    # Ajout des commentaires
    def set_comment(self, n : int) -> list :
        url : str = 'https://www.youtube.com/watch?v=' + str(self.id) #url ytb
        with Chrome() as driver:
            wait = WebDriverWait(driver,10)
            driver.get(url)

            for item in range(3): # Récupèrer les commentaires
                time.sleep(3)

            # On récupère le nombre de commentaires qu'on souhaite
            acc = 0
            list_comment = []
            for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
                if acc < n:
                    list_comment.append(comment.text)
                    acc += 1
                else : break

        # Retourner le résultat
        if len(list_comment) != 0 : 
            self.result["comments_list"] = list_comment.copy()
            return list_comment
        else :
            None

            
def check_input_data(data : dict):
    """ Vérifie qu'il s'agit d'un dictionnaire de chaînes de caractères

    Args:
        data (dict): dictionnaire de str

    Returns:
        str or None: élement du dictionnaire qui n'est pas une chaînes de caractères
    """
    for id_video in data:
        if not(isinstance(id_video, str)): return("Erreur : Il ne s'agit pas d'un dictionnaire d'ID de vidéo.")
        
        response = requests.get('https://www.youtube.com/watch?v=' + str(id_video))
        if response.status_code != 200: return("Erreur d'ID : le lien du site n'existe pas")    
    return None

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
        
        # TODO : vérifier que c'est bien un dictionnaire de str, et que les vidéos existent
        if check_input_data(data) is not None:
            raise Exception(check_input_data(data))
        
        
        # Pour chaque élément du dictionnaire json (ie, pour chaque id de vidéo)
        final_result = {}
        for id_video in data['videos_id']:
            video_ytb = VideoYoutube(id_video) # Création de l'objet vidéo youtube
            if video_ytb.msg_erreur is not None : raise Exception(video_ytb.msg_erreur)
            list_comments = video_ytb.set_comment(10) if video_ytb.msg_erreur is None else None
            final_result[id_video] = video_ytb.result # ajout du tableau résultat dans un dictionnaire regroupant toutes les informations de chaque vidéo

        input_file.close() # Fermeture du fichier json d'input

        # Ecriture des informations dans le fichier d'output
        with open(output, "w", encoding='utf8') as output_file:
            json.dump(final_result, output_file, ensure_ascii=False)

        output_file.close() # Fermeture du fichier json d'output
    except Exception as e:
        print(e)
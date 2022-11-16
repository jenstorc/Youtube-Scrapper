from scrapper import VideoYoutube
import validators

## Vérification avec un ID existant
id = "JhWZWXvN_yo"
video_ytb_1 = VideoYoutube(id)

#Vérification des types 
def test_type_titre(): 
    assert isinstance(video_ytb_1.title, str) # type du titre (str)

def test_type_description():
    assert isinstance(video_ytb_1.description, str) # type de la description (str)

def test_type_videomaker():
    assert isinstance(video_ytb_1.videomaker, str) # type du nom de l'auteur (str)

def test_type_nb_like():
    assert isinstance(video_ytb_1.nb_like, int) # type du nombre de likes (int)

def test_type_links():
    assert isinstance(video_ytb_1.list_links, list) # type de la liste de liens (list)

def test_type_each_url():
    assert all([validators.url(mesurls) for mesurls in video_ytb_1.list_links]) # type de chaque lien de la liste (list)

# ne fonctionne que si la page charge bien
#def test_type_comments():
#    assert isinstance(video_ytb_1.list_comments, list) # type du dictionnaire de résultat
#

def test_type_dict():
    assert isinstance(video_ytb_1.result, dict) # type du dictionnaire de résultat


# Vérification de la sortie
def test_titre():
    assert video_ytb_1.title == "ELISE LUCET EST SUB CHEZ MOI ?! (Débrief Cash Investigation)" # Vérifier que le titre concorde

def test_videomaker():
    assert video_ytb_1.videomaker == "ZeratoR" # Vérifier que le nom du vidéaste concorde

# Le nombre de j'aime augmente régulièrement
#def test_nb_like():
#    assert video_ytb_1.nb_like == 9552 # Vérifier que le nombre de likes concorde

def test_links():
    links = [
            "https://www.youtube.com/user/ZeratoRS",
            "https://www.twitch.tv/zerator",
            "https://www.twitch.tv/videos/1630581181",
            "http://www.ZeratoR.com/",
            "https://boutiquezerator.com/",
            "http://e.lga.to/ZeratoR",
            "https://www.facebook.com/ZeratoR",
            "https://twitter.com/ZeratoR",
            "https://www.instagram.com/zerator",
            "https://discord.gg/zerator",
            "https://www.tiktok.com/@ZeratoR",
            "https://www.mandatory.gg/",
            "https://twitter.com/MandatoryGG",
            "https://www.instagram.com/mandatory.gg/",
            "https://www.tiktok.com/@mandatory.gg",
            "https://discord.gg/3uHncKP",
            "https://www.twitch.tv/mandatory",
            "https://www.facebook.com/MandatoryGG/"
        ]
    assert video_ytb_1.list_links == links  # Vérifier que les liens des sites concorde

def test_keys_dict():
    key_list = ["title", "channel_name", "nb_likes", "description", "links"]
    assert all([name in video_ytb_1.result.keys() for name in key_list])  # Vérifier que le nom des clés concorde

## Test avec page youtube non existante
id = "ueueueueueu"
video_ytb_2 = VideoYoutube(id)
NoneType = type(None)

# Vérifier que le titre, la descrption, l'auteur, le nombre de likes et la liste de liens sont de même type que None
def test_type_titre():
    assert isinstance(video_ytb_2.title, NoneType)

def test_type_description():
    assert isinstance(video_ytb_2.description, NoneType)

def test_type_videomaker():
    assert isinstance(video_ytb_2.videomaker, NoneType)

def test_type_nb_like():
    assert isinstance(video_ytb_2.nb_like, NoneType)

def test_type_links():
    assert isinstance(video_ytb_2.list_links, NoneType)

def test_type_dict():
    assert isinstance(video_ytb_2.result, dict) # Vérifier que c'est bien un dictionnaire


# Vérification des types : vérifier qu'ils valent None
def test_titre():
    assert video_ytb_2.title == None

def test_description():
    assert video_ytb_2.description == None

def test_videomaker():
    assert video_ytb_2.videomaker == None

def test_nb_like():
    assert video_ytb_2.nb_like == None

def test_links():
    assert video_ytb_2.list_links == None

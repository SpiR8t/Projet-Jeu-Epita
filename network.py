import asyncio, json, requests,time, threading
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
from random import *
from queue import Queue

# Ajout des paramètres de la base de donnée Firebase
API_KEY = "AIzaSyCYI_3pSmQTPU2YtLcMlPCW0ch8qurqbEs"
PROJECT_ID = "projet-sup-epita"

# Déclaration globale datachannel et boucle réseau pour intercommunication des boucles
channel = None # Chanel à créer
network_loop = None # Loop réseau

# Queue globale pour les messages
incoming_messages = Queue() 

def start_network(is_host):
    # Creation d'un event pour arreter la connexion
    stop_event = asyncio.Event()
    # Configuration de la connection P2P
    config = RTCConfiguration(
        iceServers=[RTCIceServer(urls=["stun:stun.l.google.com:19302"])]
    )
    pc = RTCPeerConnection(config)

    if is_host:
        asyncio.run(start_host(stop_event,pc))
    else:
        start_client()

async def start_host(end_event, pc):
    channel = pc.createDataChannel("game_chanel")

    @channel.on("open")
    def on_open():
        # À faire quand on ouvre le datachannel
        print("🔔 DataChannel ouvert (offer). Tu peux envoyer des messages.")
        channel.send(input("Message pour le client : "))

    @channel.on("message")
    def on_message(message):
        # À faire quand on reçois un message
        print("← message reçu du client:", message)
        incoming_messages.put(message)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    game_code = find_code(generate_game_code())
    game_data = {
        "fields": {
            "offer": {"stringValue": json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})},
            "answer": {"nullValue": None}
        }
    }

    create_lobby(game_code,game_data)
    print("Code de partie : "+ game_code)
    print("\n-----------------------------------\n")

    answer = wait_for_response(game_code)
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))
    network_loop = asyncio.get_running_loop()
    await end_event.wait()

def start_client():
    pass


# ========== Gestion de la création de la partie =========

def generate_game_code():
    """ Génère aléatoirement un code de partie (5 lettres majuscules)"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    for _ in range(5):
        res += choice(alphabet)
    return res

def find_code(code):
    """ S"assure que le code de partie mis en paramètre n'existe pas encore, sinon, en génère un nouveau."""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    res = requests.get(url)
    if res.status_code == 404: # N'existe pas
        return code
    elif res.status_code == 200:
        find_code(generate_game_code())
    else:
        return res.text

def create_lobby(code,data):
    """ Ajoute à la base de donnée la partie avec l'offre sdp."""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies?documentId={code}&key={API_KEY}"
    res = requests.post(url, json=data)
    if res.status_code == 200:
        print(f"Lobby créé avec succès !")
    else:
        print("Erreur:", res.text)

def wait_for_response(code):
    """ Check en continue si la réponse a été rempli dans la db """
    global answer
    print("En attente de la réponse de l'autre joueur")
    searching_response = True
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    while searching_response:
        res = requests.get(url)
        if res.status_code == 200:
            doc = res.json()
            if doc["fields"]["answer"] != {"nullValue": None}:
                print("✅ reponse reçu")
                answer = json.loads(doc["fields"]["answer"]["stringValue"])
                searching_response = False
            else:
                time.sleep(5)
        else:
            print("Erreur:", res.text)
    return answer





def initiate_game():
    pass